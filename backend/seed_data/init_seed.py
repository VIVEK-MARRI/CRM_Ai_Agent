"""
Database seed script.
Populates the database with sample leads for development/testing.

Usage:
    python -m seed_data.init_seed
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, init_db
from app.models.lead import Lead
from app.services.lead_service import LeadService
from app.models.schemas import LeadInput
from seed_data.leads import SEED_LEADS


def seed_database():
    """Populate database with seed data."""
    
    # Initialize tables
    init_db()
    print("✓ Database tables initialized")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Lead).delete()
        db.commit()
        print("✓ Existing leads cleared")
        
        # Seed leads
        service = LeadService(db)
        
        for i, lead_data in enumerate(SEED_LEADS, 1):
            # Convert to LeadInput schema
            lead_input = LeadInput(**lead_data)
            
            # Score the lead
            result = service.score_lead(lead_input)
            
            print(f"  [{i}/{len(SEED_LEADS)}] Seeded: {lead_data['email']} "
                  f"(Score: {result['score']:.1f})")
        
        print(f"\n✓ Successfully seeded {len(SEED_LEADS)} leads")
        
    except Exception as e:
        print(f"✗ Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
