"""
Pydantic models for API request/response validation.
Defines input and output schemas for the Lead Scoring Agent.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


class LeadInput(BaseModel):
    """Input schema for lead scoring request."""
    
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    demo_requested: bool = False
    registration: bool = False
    enquiry_call_whatsapp: bool = False
    enquiry_date: Optional[datetime] = None
    pricing_compared: bool = False
    lead_through_events: bool = False
    lead_through_call: bool = False
    lead_through_referral: bool = False


class FeatureContribution(BaseModel):
    """Feature contribution in the explanation."""
    
    feature: str
    impact: float = Field(..., ge=0, le=100)
    reason: str


class ScoreExplanation(BaseModel):
    """Structured explanation for a lead score."""
    
    score: float = Field(..., ge=0, le=100)
    intent_level: str  # High, Medium, Low
    feature_contributions: List[FeatureContribution]
    confidence: float = Field(..., ge=0, le=100)
    recommended_action: str


class LeadResponse(BaseModel):
    """Response schema for a lead."""
    
    id: int
    email: str
    name: str
    company: Optional[str]
    demo_requested: bool
    registration: bool
    enquiry_call_whatsapp: bool
    enquiry_date: Optional[datetime]
    pricing_compared: bool
    lead_through_events: bool
    lead_through_call: bool
    lead_through_referral: bool
    score: float
    intent_level: str
    confidence: float
    recommended_action: str
    created_at: datetime
    updated_at: datetime
    explanation: ScoreExplanation
    
    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Response for list of leads."""
    
    id: int
    email: str
    name: str
    company: Optional[str]
    score: float
    intent_level: str
    confidence: float
    recommended_action: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalyticsResponse(BaseModel):
    """Analytics overview response."""
    
    total_leads: int
    average_score: float
    high_intent_count: int
    high_intent_percentage: float
    medium_intent_count: int
    medium_intent_percentage: float
    low_intent_count: int
    low_intent_percentage: float
    average_confidence: float
    conversion_forecast: float
    source_breakdown: dict
