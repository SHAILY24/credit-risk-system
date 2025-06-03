#!/usr/bin/env python
"""
Comprehensive test script for Credit Risk Assessment System Backend
"""
import sys
import json
import traceback
from typing import Dict, Any

def test_imports():
    """Test if all modules can be imported"""
    print("=" * 60)
    print("1. Testing Module Imports")
    print("-" * 60)
    
    modules_to_test = [
        ("app.config", "settings"),
        ("app.database", "Base, get_db, init_db, test_connection"),
        ("app.models", "User, APIKey, Prediction, AuditLog"),
        ("app.schemas", "CreditApplication, PredictionRequest, PredictionResponse"),
        ("app.auth", "get_password_hash, verify_password, create_access_token"),
        ("app.ml_model", "model_service"),
        ("app.main", "app"),
    ]
    
    for module_name, components in modules_to_test:
        try:
            exec(f"from {module_name} import {components}")
            print(f"✓ {module_name:<20} imported successfully")
        except Exception as e:
            print(f"✗ {module_name:<20} failed: {str(e)[:50]}")
            return False
    
    print("\n✅ All modules imported successfully")
    return True

def test_config():
    """Test configuration loading"""
    print("\n" + "=" * 60)
    print("2. Testing Configuration")
    print("-" * 60)
    
    try:
        from app.config import settings
        
        config_items = [
            ("App Name", settings.app_name),
            ("App Version", settings.app_version),
            ("Debug Mode", settings.debug),
            ("Log Level", settings.log_level),
            ("Model Path", settings.model_path),
            ("API Prefix", settings.api_prefix),
        ]
        
        for name, value in config_items:
            print(f"  {name:<20}: {value}")
        
        print("\n✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return False

def test_model_loading():
    """Test if the ML model loads correctly"""
    print("\n" + "=" * 60)
    print("3. Testing Model Loading")
    print("-" * 60)
    
    try:
        from app.ml_model import model_service
        
        if model_service.model is not None:
            print(f"✓ Model loaded: {type(model_service.model).__name__}")
            print(f"✓ Preprocessor loaded: {type(model_service.preprocessor).__name__}")
            print(f"✓ Model metadata: {model_service.model_metadata}")
            
            # Check feature names
            if model_service.feature_names:
                print(f"✓ Feature names: {len(model_service.feature_names)} features")
            
            print("\n✅ Model loaded successfully")
            return True
        else:
            print("✗ Model not loaded")
            return False
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        traceback.print_exc()
        return False

def test_sample_prediction():
    """Test a sample prediction"""
    print("\n" + "=" * 60)
    print("4. Testing Sample Prediction")
    print("-" * 60)
    
    try:
        from app.ml_model import model_service
        from app.schemas import CreditApplication
        
        # Create a low-risk application
        low_risk_app = CreditApplication(
            checking_account_status='A13',  # >= 200 DM
            credit_history='A32',  # existing paid
            savings_account='A64',  # >= 1000 DM
            duration_months=12,
            credit_amount=2000,
            purpose='A43',
            age=45,
            personal_status_sex='A93',
            other_debtors='A101',
            employment_since='A75',  # >= 7 years
            job='A173',
            property='A121',
            installment_rate=1,
            residence_since=4,
            existing_credits=1,
            num_dependents=1,
            other_installment_plans='A143',
            housing='A152',
            telephone='A192',
            foreign_worker='A201'
        )
        
        # Create a high-risk application
        high_risk_app = CreditApplication(
            checking_account_status='A11',  # < 0 DM
            credit_history='A34',  # critical account
            savings_account='A61',  # < 100 DM
            duration_months=48,
            credit_amount=15000,
            purpose='A43',
            age=22,
            personal_status_sex='A93',
            other_debtors='A101',
            employment_since='A71',  # unemployed
            job='A171',
            property='A124',
            installment_rate=4,
            residence_since=1,
            existing_credits=3,
            num_dependents=2,
            other_installment_plans='A141',
            housing='A151',
            telephone='A191',
            foreign_worker='A201'
        )
        
        print("Testing Low-Risk Application:")
        result1 = model_service.predict(low_risk_app)
        print(f"  Risk category: {result1['risk_category']}")
        print(f"  Default probability: {result1['default_probability']:.2%}")
        print(f"  Recommendation: {result1['recommendation']}")
        print(f"  Processing time: {result1['processing_time_ms']:.2f}ms")
        
        print("\nTesting High-Risk Application:")
        result2 = model_service.predict(high_risk_app)
        print(f"  Risk category: {result2['risk_category']}")
        print(f"  Default probability: {result2['default_probability']:.2%}")
        print(f"  Recommendation: {result2['recommendation']}")
        print(f"  Processing time: {result2['processing_time_ms']:.2f}ms")
        
        print("\nTesting Prediction with Explanation:")
        result3 = model_service.explain_prediction(high_risk_app)
        if 'explanation' in result3:
            print(f"  Top risk factors: {result3['explanation']['top_risk_factors']}")
        
        print("\n✅ Predictions working correctly")
        return True
    except Exception as e:
        print(f"✗ Prediction failed: {e}")
        traceback.print_exc()
        return False

def test_fastapi_endpoints():
    """Test FastAPI application and endpoints"""
    print("\n" + "=" * 60)
    print("5. Testing FastAPI Application")
    print("-" * 60)
    
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        # Create test client
        client = TestClient(app)
        
        # Test health endpoint
        print("Testing /health endpoint:")
        response = client.get("/health")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            health = response.json()
            print(f"  System status: {health['status']}")
            print(f"  Version: {health['version']}")
            print(f"  Model loaded: {health['model_loaded']}")
        
        # Test routes
        routes = [route.path for route in app.routes]
        key_endpoints = {
            '/health': 'System health check',
            '/login': 'User authentication',
            '/register': 'User registration',
            '/predict': 'Credit risk prediction',
            '/batch-predict': 'Batch predictions',
            '/api-keys': 'API key management',
            '/stats': 'System statistics',
            '/model/metrics': 'Model performance metrics',
            '/model/feature-importance': 'Feature importance',
        }
        
        print("\nRegistered Endpoints:")
        for endpoint, description in key_endpoints.items():
            if endpoint in routes:
                print(f"  ✓ {endpoint:<30} - {description}")
            else:
                print(f"  ✗ {endpoint:<30} - Missing!")
        
        print(f"\nTotal routes: {len(routes)}")
        print("\n✅ FastAPI application initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ FastAPI initialization failed: {e}")
        traceback.print_exc()
        return False

def test_database_models():
    """Test database models"""
    print("\n" + "=" * 60)
    print("6. Testing Database Models")
    print("-" * 60)
    
    try:
        from app.models import User, APIKey, Prediction, AuditLog
        from app.database import Base
        
        # Check table names
        tables = [
            (User, "users"),
            (APIKey, "api_keys"),
            (Prediction, "predictions"),
            (AuditLog, "audit_logs"),
        ]
        
        for model, expected_table in tables:
            actual_table = model.__tablename__
            if actual_table == expected_table:
                print(f"✓ {model.__name__:<15} -> {actual_table}")
            else:
                print(f"✗ {model.__name__:<15} -> Expected: {expected_table}, Got: {actual_table}")
        
        print("\n✅ Database models configured correctly")
        return True
        
    except Exception as e:
        print(f"✗ Database models failed: {e}")
        return False

def test_authentication():
    """Test authentication functions"""
    print("\n" + "=" * 60)
    print("7. Testing Authentication")
    print("-" * 60)
    
    try:
        from app.auth import get_password_hash, verify_password, create_access_token, generate_api_key
        
        # Test password hashing
        password = "test_password_123"
        hashed = get_password_hash(password)
        print(f"✓ Password hashed: {hashed[:20]}...")
        
        # Test password verification
        is_valid = verify_password(password, hashed)
        print(f"✓ Password verification: {is_valid}")
        
        # Test token creation
        token = create_access_token(data={"sub": "testuser"})
        print(f"✓ JWT token created: {token[:20]}...")
        
        # Test API key generation
        api_key = generate_api_key()
        print(f"✓ API key generated: {api_key[:20]}...")
        
        print("\n✅ Authentication functions working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False

def main():
    print("=" * 60)
    print("CREDIT RISK ASSESSMENT SYSTEM - BACKEND TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Model Loading", test_model_loading),
        ("Sample Prediction", test_sample_prediction),
        ("FastAPI Endpoints", test_fastapi_endpoints),
        ("Database Models", test_database_models),
        ("Authentication", test_authentication),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25}: {status}")
    
    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())