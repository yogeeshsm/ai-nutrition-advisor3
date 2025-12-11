"""Test if predictor loads correctly"""
from malnutrition_predictor import get_predictor

print("\n=== Testing Predictor Direct Import ===")

# Get predictor
predictor = get_predictor()

# Test with Lakshmi (healthy child)
result = predictor.predict(
    age_months=59,
    weight_kg=18.0,
    height_cm=109.0
)

print(f"\n✅ Lakshmi Test:")
print(f"   Status: {result['nutrition_status']}")
print(f"   Risk: {result['risk_level']}")
print(f"   Confidence: {result['confidence']*100:.1f}%")

# Test with a malnourished child
result2 = predictor.predict(
    age_months=24,
    weight_kg=8.5,
    height_cm=78.0
)

print(f"\n✅ Malnourished Child Test:")
print(f"   Status: {result2['nutrition_status']}")
print(f"   Risk: {result2['risk_level']}")
print(f"   Confidence: {result2['confidence']*100:.1f}%")
