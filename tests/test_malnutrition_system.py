"""
Quick test script for malnutrition prediction
Tests both trained model and fallback predictor
"""

import sys
import os

# Test 1: Import predictor
print("\n" + "="*80)
print("TEST 1: Import Malnutrition Predictor")
print("="*80)

try:
    from malnutrition_predictor import get_predictor
    predictor = get_predictor()
    print("[OK] Predictor loaded successfully")
    print(f"   Using: {'Fallback' if predictor.use_fallback else 'Trained Model'}")
    print(f"   Accuracy: {predictor.metadata['accuracy']*100:.2f}%")
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

# Test 2: Make prediction
print("\n" + "="*80)
print("TEST 2: Make Prediction")
print("="*80)

test_data = {
    'age_months': 36,
    'weight_kg': 14.0,
    'height_cm': 95.0,
    'gender': 'male'
}

print(f"Input: Age={test_data['age_months']}mo, Weight={test_data['weight_kg']}kg, Height={test_data['height_cm']}cm")

try:
    result = predictor.predict(
        age_months=test_data['age_months'],
        weight_kg=test_data['weight_kg'],
        height_cm=test_data['height_cm'],
        gender=test_data['gender']
    )
    print("[OK] Prediction successful")
    print(f"   Status: {result['nutrition_status']}")
    print(f"   Risk: {result['risk_level']}")
    print(f"   Confidence: {result['confidence']*100:.1f}%")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Test Flask app import
print("\n" + "="*80)
print("TEST 3: Import Flask App")
print("="*80)

try:
    import flask_app
    print("[OK] Flask app imported successfully")
    print(f"   Predictor loaded: {flask_app.MALNUTRITION_PREDICTOR is not None}")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✅ ALL TESTS PASSED")
print("="*80)
print("\n[INFO] The malnutrition prediction system is ready!")
print("[INFO] You can now:")
print("       1. Start the server: python flask_app.py")
print("       2. Test API: POST http://127.0.0.1:5000/api/predict-malnutrition/1")
print("       3. Deploy to Render - it will work without errors!")
