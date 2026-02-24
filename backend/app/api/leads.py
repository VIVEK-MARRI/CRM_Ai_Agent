"""
Lead Scoring API Routes

Endpoints:
- POST /score-lead: Score a new lead
- GET /leads: List all leads with pagination
- GET /leads/{id}: Get single lead
- GET /analytics: Get analytics overview
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas import LeadInput, LeadResponse, LeadListResponse, AnalyticsResponse
from app.services.lead_service import LeadService
from app.core.logging import logger


router = APIRouter(prefix="/api", tags=["leads"])


@router.post("/score-lead", response_model=dict)
def score_lead(
    lead_data: LeadInput,
    db: Session = Depends(get_db)
):
    """
    Score a lead and store results.
    
    Request body:
    ```
    {
        "email": "john@example.com",
        "name": "John Doe",
        "company": "ACME Corp",
        "demo_requested": true,
        "registration": true,
        "enquiry_call_whatsapp": false,
        "enquiry_date": "2024-02-20T10:00:00",
        "pricing_compared": true,
        "lead_through_events": false,
        "lead_through_call": true,
        "lead_through_referral": false
    }
    ```
    
    Returns:
    ```
    {
        "id": 1,
        "email": "john@example.com",
        "score": 75.5,
        "intent_level": "High",
        "confidence": 85.0,
        "explanation": {
            "score": 75.5,
            "intent_level": "High",
            "feature_contributions": [
                {
                    "feature": "demo_requested",
                    "impact": 32.5,
                    "reason": "Lead requested a product demo"
                }
            ],
            "confidence": 85.0,
            "recommended_action": "Direct sales call within 24 hrs"
        },
        "action": {
            "action": "Direct sales call within 24 hrs",
            "urgency": "Immediate",
            "probability_label": "70-90%"
        }
    }
    ```
    """
    try:
        service = LeadService(db)
        result = service.score_lead(lead_data)
        logger.info(f"Lead scored successfully: {lead_data.email}")
        return result
    except Exception as e:
        logger.error(f"Error scoring lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leads", response_model=dict)
def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("score", regex="^(score|created_at)$"),
    intent_filter: str = Query(None, regex="^(High|Medium|Low)?$"),
    db: Session = Depends(get_db)
):
    """
    List leads with pagination and filtering.
    
    Query parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 20, max: 100)
    - sort_by: Sort by 'score' or 'created_at'
    - intent_filter: Filter by 'High', 'Medium', or 'Low' intent
    
    Returns:
    ```
    {
        "leads": [
            {
                "id": 1,
                "email": "john@example.com",
                "name": "John Doe",
                "score": 75.5,
                "intent_level": "High",
                "created_at": "2024-02-20T10:00:00"
            }
        ],
        "total": 100,
        "skip": 0,
        "limit": 20
    }
    ```
    """
    try:
        service = LeadService(db)
        leads, total = service.list_leads(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            intent_filter=intent_filter
        )
        
        logger.info(f"Listed {len(leads)} leads")
        
        return {
            "leads": leads,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Error listing leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leads/{lead_id}")
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single lead by ID.
    
    Returns:
    ```
    {
        "id": 1,
        "email": "john@example.com",
        "name": "John Doe",
        "score": 75.5,
        "intent_level": "High",
        "confidence": 85.0,
        "recommended_action": "Direct sales call within 24 hrs",
        "feature_contributions": [...]
    }
    ```
    """
    try:
        service = LeadService(db)
        lead = service.get_lead(lead_id)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        logger.info(f"Retrieved lead: {lead_id}")
        return lead
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    Get analytics overview.
    
    Returns:
    ```
    {
        "total_leads": 100,
        "average_score": 65.5,
        "high_intent_count": 25,
        "high_intent_percentage": 25.0,
        "medium_intent_count": 45,
        "medium_intent_percentage": 45.0,
        "low_intent_count": 30,
        "low_intent_percentage": 30.0,
        "average_confidence": 78.5,
        "conversion_forecast": 0.45,
        "source_breakdown": {
            "demo_requested": 35,
            "registration": 42,
            "referral": 18
        }
    }
    ```
    """
    try:
        service = LeadService(db)
        analytics = service.get_analytics()
        logger.info("Analytics retrieved")
        return analytics
    except Exception as e:
        logger.error(f"Error retrieving analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
