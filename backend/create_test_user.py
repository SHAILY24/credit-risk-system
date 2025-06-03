#!/usr/bin/env python
"""
Create test user and sample data for the Credit Risk Assessment System
"""
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import User, APIKey, Prediction, AuditLog, Base
from app.auth import get_password_hash, generate_api_key
from app.config import settings

def create_test_database():
    """Create test database and tables"""
    # Use SQLite for testing
    test_db_url = "sqlite:///test_credit_risk.db"
    engine = create_engine(test_db_url, echo=False)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal(), engine

def create_test_users(db):
    """Create test users"""
    users = [
        {
            "username": "testuser",
            "email": "testuser@shaily.dev",
            "password": "Test@123456",
            "is_admin": False
        },
        {
            "username": "admin",
            "email": "admin@shaily.dev",
            "password": "Admin@123456",
            "is_admin": True
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user exists
        existing = db.query(User).filter(
            (User.username == user_data["username"]) | 
            (User.email == user_data["email"])
        ).first()
        
        if not existing:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                is_admin=user_data["is_admin"],
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(user)
            created_users.append(user_data)
            print(f"✅ Created user: {user_data['username']}")
        else:
            print(f"ℹ️  User already exists: {user_data['username']}")
    
    db.commit()
    return created_users

def create_test_api_keys(db):
    """Create test API keys"""
    # Get test user
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        print("❌ Test user not found")
        return []
    
    api_keys = []
    for i in range(2):
        key = generate_api_key()
        api_key = APIKey(
            key=key,
            name=f"Test API Key {i+1}",
            user_id=user.id,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(api_key)
        api_keys.append(key)
        print(f"✅ Created API key: {key[:20]}...")
    
    db.commit()
    return api_keys

def create_sample_predictions(db):
    """Create sample prediction records"""
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        print("❌ Test user not found")
        return
    
    sample_predictions = [
        {
            "probability": 0.15,
            "prediction": 0,
            "risk_category": "Low",
            "recommendation": "Approve with standard terms",
            "confidence": 0.85,
            "loan_amount": 5000
        },
        {
            "probability": 0.45,
            "prediction": 0,
            "risk_category": "Medium",
            "recommendation": "Approve with additional verification",
            "confidence": 0.55,
            "loan_amount": 10000
        },
        {
            "probability": 0.85,
            "prediction": 1,
            "risk_category": "High",
            "recommendation": "Reject application",
            "confidence": 0.85,
            "loan_amount": 20000
        }
    ]
    
    for pred_data in sample_predictions:
        prediction = Prediction(
            user_id=user.id,
            input_data={"sample": "data"},
            probability=pred_data["probability"],
            prediction=pred_data["prediction"],
            risk_category=pred_data["risk_category"],
            recommendation=pred_data["recommendation"],
            confidence=pred_data["confidence"],
            loan_amount=pred_data["loan_amount"],
            expected_loss=pred_data["loan_amount"] * pred_data["probability"] * 0.7,
            model_version="1.0.0",
            processing_time_ms=10.5,
            created_at=datetime.utcnow()
        )
        db.add(prediction)
    
    db.commit()
    print(f"✅ Created {len(sample_predictions)} sample predictions")

def main():
    print("=" * 60)
    print("CREDIT RISK ASSESSMENT SYSTEM - TEST DATA SETUP")
    print("=" * 60)
    
    try:
        # Create database and tables
        print("\n📊 Setting up test database...")
        db, engine = create_test_database()
        print("✅ Database created: test_credit_risk.db")
        
        # Create test users
        print("\n👤 Creating test users...")
        users = create_test_users(db)
        
        # Create API keys
        print("\n🔑 Creating API keys...")
        api_keys = create_test_api_keys(db)
        
        # # Create sample predictions
        # print("\n📈 Creating sample predictions...")
        # create_sample_predictions(db)
        
        # Print credentials
        print("\n" + "=" * 60)
        print("TEST CREDENTIALS")
        print("=" * 60)
        print("\n📱 Regular User:")
        print("  Username: testuser")
        print("  Password: Test@123456")
        print("  Email: testuser@shaily.dev")
        
        print("\n👨‍💼 Admin User:")
        print("  Username: admin")
        print("  Password: Admin@123456")
        print("  Email: admin@shaily.dev")
        
        if api_keys:
            print("\n🔑 API Keys:")
            for i, key in enumerate(api_keys):
                print(f"  Key {i+1}: {key}")
        
        print("\n" + "=" * 60)
        print("✅ Test data setup complete!")
        print("=" * 60)
        
        # Close database
        db.close()
        
        # Update .env to use SQLite
        print("\n📝 Updating .env to use SQLite database...")
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        with open(env_path, 'w') as f:
            for line in lines:
                if line.startswith('DATABASE_URL='):
                    f.write(f'DATABASE_URL=sqlite:///{os.path.abspath("test_credit_risk.db")}\n')
                else:
                    f.write(line)
        
        print("✅ Updated .env file to use SQLite database")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())