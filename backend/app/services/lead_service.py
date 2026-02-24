"""
Lead Service - Manages lead operations.

Orchestrates:
- CRUD operations on leads
- Caching with Redis
- Scoring pipeline
- Database persistence

Layered architecture: API -> Service -> Engines + DB
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import json

from app.models.lead import Lead as LeadModel
from app.models.schemas import LeadInput, ScoreExplanation, FeatureContribution
from app.engines.scoring_engine import get_scoring_engine
from app.engines.explanation_engine import get_explanation_engine
from app.engines.next_action_engine import get_action_engine
from app.core.logging import logger


class LeadService:
    """
    Service for lead management.
    
    Responsibilities:
    - Create/read/update leads
    - Scoring pipeline orchestration
    - Result caching
    - Analytics aggregation
    """
    
    def __init__(self, db: Session, cache=None):
        """Initialize service with database session and optional cache."""
        self.db = db
        self.cache = cache
        self.scoring_engine = get_scoring_engine()
        self.explanation_engine = get_explanation_engine()
        self.action_engine = get_action_engine()
    
    def score_lead(self, lead_data: LeadInput) -> Dict[str, Any]:
        """
        Score a lead and store results.
        
        Pipeline:
        1. Check if lead exists (update) or create new
        2. Execute scoring engine
        3. Generate explanation
        4. Get recommended action
        5. Persist to database
        6. Cache result
        
        Args:
            lead_data: Lead input schema
            
        Returns:
            Scored lead with explanation and recommendation
        """
        
        logger.info(f"Scoring lead: {lead_data.email}")
        
        # Convert Pydantic model to dict for engines
        lead_dict = lead_data.model_dump()
        
        # Execute scoring engine
        scoring_result = self.scoring_engine.score(lead_dict)
        score = scoring_result['score']
        contributions = scoring_result['contributions']
        
        logger.debug(f"Raw score calculated: {score}")
        
        # Generate explanation
        explanation = self.explanation_engine.explain_score(
            score=score,
            contributions=contributions,
            lead_data=lead_dict
        )
        
        # Get next action
        action = self.action_engine.get_action(score)
        
        # Check if lead exists
        existing_lead = self.db.query(LeadModel).filter(
            LeadModel.email == lead_data.email
        ).first()
        
        if existing_lead:
            # Update existing lead
            for key, value in lead_dict.items():
                setattr(existing_lead, key, value)
            existing_lead.score = score
            existing_lead.intent_level = explanation['intent_level']
            existing_lead.confidence = explanation['confidence']
            existing_lead.recommended_action = action['action']
            existing_lead.feature_contributions = json.dumps(contributions)
            existing_lead.updated_at = datetime.utcnow()
            lead_model = existing_lead
            logger.info(f"Lead updated: {lead_data.email}")
        else:
            # Create new lead
            lead_model = LeadModel(
                email=lead_data.email,
                name=lead_data.name,
                company=lead_data.company,
                demo_requested=lead_data.demo_requested,
                registration=lead_data.registration,
                enquiry_call_whatsapp=lead_data.enquiry_call_whatsapp,
                enquiry_date=lead_data.enquiry_date,
                pricing_compared=lead_data.pricing_compared,
                lead_through_events=lead_data.lead_through_events,
                lead_through_call=lead_data.lead_through_call,
                lead_through_referral=lead_data.lead_through_referral,
                score=score,
                intent_level=explanation['intent_level'],
                confidence=explanation['confidence'],
                recommended_action=action['action'],
                feature_contributions=json.dumps(contributions),
            )
            self.db.add(lead_model)
            logger.info(f"Lead created: {lead_data.email}")
        
        # Commit to database
        self.db.commit()
        self.db.refresh(lead_model)
        
        # Build response with explanation
        response = {
            'id': lead_model.id,
            'email': lead_model.email,
            'name': lead_model.name,
            'company': lead_model.company,
            'demo_requested': lead_model.demo_requested,
            'registration': lead_model.registration,
            'enquiry_call_whatsapp': lead_model.enquiry_call_whatsapp,
            'enquiry_date': lead_model.enquiry_date,
            'pricing_compared': lead_model.pricing_compared,
            'lead_through_events': lead_model.lead_through_events,
            'lead_through_call': lead_model.lead_through_call,
            'lead_through_referral': lead_model.lead_through_referral,
            'score': lead_model.score,
            'intent_level': lead_model.intent_level,
            'confidence': lead_model.confidence,
            'recommended_action': lead_model.recommended_action,
            'created_at': lead_model.created_at,
            'updated_at': lead_model.updated_at,
            'explanation': ScoreExplanation(
                score=explanation['score'],
                intent_level=explanation['intent_level'],
                feature_contributions=[
                    FeatureContribution(
                        feature=c['feature'],
                        impact=c['impact'],
                        reason=c['reason']
                    )
                    for c in explanation['feature_contributions']
                ],
                confidence=explanation['confidence'],
                recommended_action=action['action']
            ),
            'action': action,
        }
        
        logger.info(f"Lead scoring complete: {lead_data.email}, Score: {score}")
        
        return response
    
    def get_lead(self, lead_id: int) -> Optional[Dict[str, Any]]:
        """Get a single lead by ID."""
        lead = self.db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        
        if not lead:
            return None
        
        # Parse feature contributions
        contributions = []
        if lead.feature_contributions:
            contributions = json.loads(lead.feature_contributions)
        
        return {
            'id': lead.id,
            'email': lead.email,
            'name': lead.name,
            'company': lead.company,
            'score': lead.score,
            'intent_level': lead.intent_level,
            'confidence': lead.confidence,
            'recommended_action': lead.recommended_action,
            'created_at': lead.created_at,
            'updated_at': lead.updated_at,
            'feature_contributions': contributions,
        }
    
    def list_leads(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = 'score',
        intent_filter: Optional[str] = None
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        List leads with pagination and filtering.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            sort_by: Field to sort by (score, created_at)
            intent_filter: Filter by intent level (High, Medium, Low)
            
        Returns:
            Tuple of (leads list, total count)
        """
        
        query = self.db.query(LeadModel)
        
        # Filter by intent if specified
        if intent_filter:
            query = query.filter(LeadModel.intent_level == intent_filter)
        
        # Get total count
        total = query.count()
        
        # Sort
        if sort_by == 'score':
            query = query.order_by(desc(LeadModel.score))
        elif sort_by == 'created_at':
            query = query.order_by(desc(LeadModel.created_at))
        
        # Paginate
        leads = query.offset(skip).limit(limit).all()
        
        return [
            {
                'id': lead.id,
                'email': lead.email,
                'name': lead.name,
                'company': lead.company,
                'score': lead.score,
                'intent_level': lead.intent_level,
                'confidence': lead.confidence,
                'recommended_action': lead.recommended_action,
                'created_at': lead.created_at,
            }
            for lead in leads
        ], total
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get analytics overview.
        
        Returns:
            Dictionary with key metrics
        """
        
        total = self.db.query(func.count(LeadModel.id)).scalar() or 0
        
        if total == 0:
            logger.warning("No leads found for analytics")
            return {
                'total_leads': 0,
                'average_score': 0,
                'high_intent_count': 0,
                'high_intent_percentage': 0,
                'medium_intent_count': 0,
                'medium_intent_percentage': 0,
                'low_intent_count': 0,
                'low_intent_percentage': 0,
                'average_confidence': 0,
                'conversion_forecast': 0,
                'source_breakdown': {},
            }
        
        # Calculate metrics
        avg_score = self.db.query(
            func.avg(LeadModel.score)
        ).scalar() or 0
        
        avg_confidence = self.db.query(
            func.avg(LeadModel.confidence)
        ).scalar() or 0
        
        # Intent distribution
        high_intent = self.db.query(
            func.count(LeadModel.id)
        ).filter(LeadModel.intent_level == 'High').scalar() or 0
        
        medium_intent = self.db.query(
            func.count(LeadModel.id)
        ).filter(LeadModel.intent_level == 'Medium').scalar() or 0
        
        low_intent = self.db.query(
            func.count(LeadModel.id)
        ).filter(LeadModel.intent_level == 'Low').scalar() or 0
        
        # Source breakdown
        demo_source = self.db.query(
            func.count(LeadModel.id)
        ).filter(LeadModel.demo_requested == True).scalar() or 0
        
        registration_source = self.db.query(
            func.count(LeadModel.id)
        ).filter(LeadModel.registration == True).scalar() or 0
        
        referral_source = self.db.query(
            func.count(LeadModel.id)
        ).filter(LeadModel.lead_through_referral == True).scalar() or 0
        
        # Conversion forecast (average conversion probability based on distribution)
        high_prob = 0.75 * high_intent
        medium_prob = 0.55 * medium_intent
        low_prob = 0.30 * low_intent
        conversion_forecast = (high_prob + medium_prob + low_prob) / total if total > 0 else 0
        
        return {
            'total_leads': total,
            'average_score': round(float(avg_score), 2),
            'high_intent_count': high_intent,
            'high_intent_percentage': round((high_intent / total) * 100, 1) if total > 0 else 0,
            'medium_intent_count': medium_intent,
            'medium_intent_percentage': round((medium_intent / total) * 100, 1) if total > 0 else 0,
            'low_intent_count': low_intent,
            'low_intent_percentage': round((low_intent / total) * 100, 1) if total > 0 else 0,
            'average_confidence': round(float(avg_confidence), 2),
            'conversion_forecast': round(conversion_forecast, 2),
            'source_breakdown': {
                'demo_requested': demo_source,
                'registration': registration_source,
                'referral': referral_source,
            }
        }
