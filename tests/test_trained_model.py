from malnutrition_predictor_csv import get_predictor

p = get_predictor()
result = p.predict(59, 18.0, 109.0)

print(f"\n=== TESTING TRAINED MODEL ===")
print(f"Lakshmi Iyer (59 months, 18kg, 109cm)")
print(f"  Status: {result['nutrition_status']}")
print(f"  Risk: {result['risk_level']}")
print(f"  Confidence: {result['confidence']*100:.1f}%")
print(f"\nProbabilities:")
for status, prob in result['probabilities'].items():
    print(f"  {status}: {prob*100:.1f}%")
