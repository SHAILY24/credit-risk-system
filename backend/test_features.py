#!/usr/bin/env python3
"""
Test script to verify feature creation works correctly
"""
import pandas as pd
from app.ml_model import model_service
from app.schemas import CreditApplication

def test_feature_creation():
    """Test feature creation without prediction"""
    try:
        # Create a sample application
        sample_app = CreditApplication(
            checking_account_status='A13',
            credit_history='A32',
            savings_account='A64',
            duration_months=12,
            credit_amount=2000,
            purpose='A43',
            age=45,
            personal_status_sex='A93',
            other_debtors='A101',
            employment_since='A75',
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
        
        # Create features
        df = model_service.create_features(sample_app)
        
        print("Feature Creation Test Results:")
        print("=" * 50)
        print(f"Total features created: {len(df.columns)}")
        print("\nEngineered features:")
        
        engineered_features = [
            'loan_intensity_ratio',
            'financial_stability_score', 
            'age_credit_ratio',
            'employment_stability',
            'high_credit_flag',
            'long_duration_flag'
        ]
        
        for feature in engineered_features:
            if feature in df.columns:
                value = df[feature].iloc[0]
                print(f"✓ {feature}: {value}")
            else:
                print(f"✗ {feature}: MISSING")
        
        print("\nPreprocessor Test:")
        try:
            # Test preprocessing step
            X_processed = model_service.preprocessor.transform(df)
            print(f"✓ Preprocessing successful. Shape: {X_processed.shape}")
            return True
        except Exception as e:
            print(f"✗ Preprocessing failed: {e}")
            return False
            
    except Exception as e:
        print(f"Feature creation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_feature_creation()
    if success:
        print("\n🎉 Feature creation and preprocessing working correctly!")
    else:
        print("\n❌ Feature creation or preprocessing failed!")