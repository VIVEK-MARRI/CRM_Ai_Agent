"""
Explanation Engine - Generates human-readable explanations for scores.

Transforms raw scoring data into:
- Feature-level contributions
- Intent level classification
- Confidence scoring
- Structured JSON output

Design: Service layer above scoring engine
"""

from typing import Dict, Any, List
import yaml
from app.core.config import settings
from app.core.logging import logger


class ExplanationEngine:
    """
    Generates detailed, human-readable explanations for lead scores.
    
    Provides:
    - Feature contribution breakdown
    - Intent classification
    - Confidence scoring
    - Structured JSON explanation
    """
    
    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = settings.config_path
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.intent_thresholds = self.config.get('intent_thresholds', {})
        self.score_colors = self.config.get('score_colors', {})
        logger.info("Explanation engine initialized")
    
    def explain_score(
        self,
        score: float,
        contributions: List[Dict[str, Any]],
        lead_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate structured explanation for a score.
        
        Args:
            score: Final lead score (0-100)
            contributions: List of feature contributions
            lead_data: Original lead data (optional)
            
        Returns:
            Structured explanation with score, intent, contributions, confidence
        """
        
        # Determine intent level
        intent_level = self._determine_intent_level(score)
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            score=score,
            contributions=contributions,
            lead_data=lead_data
        )
        
        # Format feature contributions
        formatted_contributions = [
            {
                'feature': c['feature'],
                'impact': round(c['impact'], 1),
                'reason': c['reason']
            }
            for c in contributions[:5]  # Top 5 features
        ]
        
        # Build explanation
        explanation = {
            'score': round(score, 1),
            'intent_level': intent_level,
            'feature_contributions': formatted_contributions,
            'confidence': round(confidence, 1),
            'color': self._get_score_color(score),
            'summary': self._generate_summary(score, intent_level, contributions)
        }
        
        logger.debug(f"Explanation generated for score {score}")
        
        return explanation
    
    def _determine_intent_level(self, score: float) -> str:
        """
        Classify intent level based on score.
        
        Args:
            score: Lead score
            
        Returns:
            Intent level: "High", "Medium", or "Low"
        """
        high_threshold = self.intent_thresholds.get('high', 80)
        medium_threshold = self.intent_thresholds.get('medium', 60)
        
        if score >= high_threshold:
            return "High"
        elif score >= medium_threshold:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_confidence(
        self,
        score: float,
        contributions: List[Dict[str, Any]],
        lead_data: Dict[str, Any] = None
    ) -> float:
        """
        Calculate confidence percentage for the score.
        
        Factors:
        - Data completeness (how many features provided)
        - Signal recency (how recent is the enquiry)
        - Signal diversity (how many different signals)
        
        Args:
            score: Lead score
            contributions: Feature contributions
            lead_data: Original lead data
            
        Returns:
            Confidence percentage (0-100)
        """
        
        confidence_factors = self.config.get('confidence_factors', [])
        total_weight = sum(f.get('weight', 0) for f in confidence_factors)
        
        # Data completeness score
        data_completeness = 0.6  # Default baseline
        if lead_data:
            filled_fields = sum(1 for v in lead_data.values() if v)
            total_fields = len(lead_data)
            if total_fields > 0:
                data_completeness = filled_fields / total_fields
        
        # Signal recency score
        signal_recency = 0.8  # Default baseline
        if lead_data and 'enquiry_date' in lead_data and lead_data['enquiry_date']:
            from datetime import datetime, timedelta
            days_since = (datetime.utcnow() - lead_data['enquiry_date']).days
            signal_recency = max(0, 1 - (days_since / 30))  # Decay over 30 days
        
        # Signal diversity (number of contributing features)
        signal_diversity = min(1.0, len(contributions) / 5)  # Max 5 signals
        
        # Weighted confidence
        confidence = (
            data_completeness * 0.3 +
            signal_recency * 0.4 +
            signal_diversity * 0.3
        )
        
        return max(0, min(100, confidence * 100))
    
    def _get_score_color(self, score: float) -> Dict[str, Any]:
        """Get color and label for score."""
        for intent_type, config in self.score_colors.items():
            if config['min'] <= score <= config['max']:
                return {
                    'color': config['color'],
                    'label': config['label']
                }
        return {'color': '#6b7280', 'label': 'Unknown'}
    
    def _generate_summary(
        self,
        score: float,
        intent_level: str,
        contributions: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable summary."""
        
        if not contributions:
            return f"Lead has a {score:.0f} score with {intent_level} intent."
        
        top_feature = contributions[0]['feature']
        
        summaries = {
            'High': f"Strong lead candidate (Score: {score:.0f}). "
                   f"Driven by {top_feature}. Recommend immediate action.",
            'Medium': f"Promising lead (Score: {score:.0f}). "
                     f"Main interest: {top_feature}. Nurture further.",
            'Low': f"Early-stage lead (Score: {score:.0f}). "
                  f"Limited engagement signals. Consider drip campaigns."
        }
        
        return summaries.get(intent_level, "Lead assessment complete")


def get_explanation_engine() -> ExplanationEngine:
    """Get or create singleton explanation engine."""
    return ExplanationEngine()
