"""
SQLAlchemy ORM models for the Lead Scoring Agent.
Defines the database schema for leads and scoring data.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, Index
from app.db.database import Base


class Lead(Base):
    """
    Lead model representing a potential customer.
    
    Fields:
    - id: Unique identifier
    - email: Lead email address
    - name: Lead name
    - company: Company name
    - demo_requested: Whether lead requested a demo
    - registration: Whether lead completed registration
    - enquiry_call_whatsapp: Whether lead inquired via call/WhatsApp
    - enquiry_date: Date of enquiry
    - pricing_compared: Whether lead compared pricing
    - lead_through_events: Whether lead came from events
    - lead_through_call: Whether lead came through direct call
    - lead_through_referral: Whether lead was referred
    - score: Calculated lead score (0-100)
    - intent_level: Categorized intent (High/Medium/Low)
    - confidence: Confidence percentage of the score
    - recommended_action: Recommended next action
    - created_at: Record creation timestamp
    - updated_at: Record last update timestamp
    """
    
    __tablename__ = "leads"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Lead Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    
    # Input Features
    demo_requested = Column(Boolean, default=False)
    registration = Column(Boolean, default=False)
    enquiry_call_whatsapp = Column(Boolean, default=False)
    enquiry_date = Column(DateTime, nullable=True)
    pricing_compared = Column(Boolean, default=False)
    lead_through_events = Column(Boolean, default=False)
    lead_through_call = Column(Boolean, default=False)
    lead_through_referral = Column(Boolean, default=False)
    
    # Scoring Results
    score = Column(Float, default=0.0, index=True)
    intent_level = Column(String(50), default="Low")  # High, Medium, Low
    confidence = Column(Float, default=0.0)
    recommended_action = Column(Text, nullable=True)
    
    # Feature Contributions (stored as JSON string, can be parsed)
    feature_contributions = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_score', 'score'),
        Index('idx_intent_level', 'intent_level'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Lead(id={self.id}, email={self.email}, score={self.score})>"
