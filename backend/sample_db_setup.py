"""
Script to create sample legal issues for testing document generation.
Add this to your existing init_db.py or run it separately.
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.database import LegalIssue
from datetime import datetime

def create_sample_legal_issues():
    """Create sample legal issues for testing."""
    
    db = SessionLocal()
    
    try:
        # Check if sample issues already exist
        existing_issue = db.query(LegalIssue).filter(LegalIssue.id == 1).first()
        if existing_issue:
            print("Sample legal issues already exist.")
            return
        
        sample_issues = [
            {
                "id": 1,
                "user_email": "john.doe@email.com",
                "description": "My landlord refuses to fix the broken heating system in my apartment. It's been 3 weeks and winter is coming.",
                "category": "tenant_rights",
                "urgency": "high",
                "location": "New York, NY",
                #"status": "open",
                # "created_at": datetime.now()
            },
            {
                "id": 2,
                "user_email": "jane.smith@email.com",
                "description": "I purchased a defective laptop that stopped working after 2 weeks. The store refuses to honor the warranty.",
                "category": "consumer_protection",
                "urgency": "medium",
                "location": "Los Angeles, CA",
                # "status": "open",
                # "created_at": datetime.now()
            },
            {
                "id": 3,
                "user_email": "bob.wilson@email.com",
                "description": "Debt collector keeps calling me about a debt I don't recognize. They won't provide validation.",
                "category": "debt_collection",
                "urgency": "high",
                "location": "Chicago, IL",
                # "status": "open",
                # "created_at": datetime.now()
            },
            {
                "id": 4,
                "user_email": "mary.johnson@email.com",
                "description": "My employer fired me after I reported workplace harassment. I believe this is retaliation.",
                "category": "employment",
                "urgency": "high",
                "location": "Houston, TX",
                # "status": "open",
                # "created_at": datetime.now()
            },
            {
                "id": 5,
                "user_email": "david.brown@email.com",
                "description": "Insurance company denied my claim for a covered medical procedure without proper explanation.",
                "category": "healthcare",
                "urgency": "medium",
                "location": "Miami, FL",
                # "status": "open",
                # "created_at": datetime.now()
            }
        ]
        
        for issue_data in sample_issues:
            issue = LegalIssue(**issue_data)
            db.add(issue)
        
        db.commit()
        print(f"Created {len(sample_issues)} sample legal issues.")
        
    except Exception as e:
        print(f"Error creating sample issues: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_legal_issues()