"""Quick test to verify model predictions"""

from malnutrition_predictor import get_predictor

predictor = get_predictor()

# Healthy child data (Lakshmi Iyer) - actual database values
healthy_child = {
    'age_months': 59,  # Actual age in database
    'weight_kg': 18.0,
    'height_cm': 109.0,
    'gender': 'F',
    'meals_per_day': 4,
    'milk_intake_ml': 500,
    'protein_servings': 2,
    'vegetable_servings': 2,
    'illness_days_last_month': 0,
    'diarrhea_recent': False,
    'fever_recent': False
}

result = predictor.predict_risk(healthy_child, [])

print("Healthy Child (Lakshmi Iyer):")
print(f"  Underweight: {result['predictions']['underweight']['risk_level']} ({result['predictions']['underweight']['probability']:.1%})")
print(f"  Stunting: {result['predictions']['stunting']['risk_level']} ({result['predictions']['stunting']['probability']:.1%})")
print(f"  Overall: {result['overall_risk'].upper()}")

# Malnourished child (Aditya Nair)
malnourished_child = {
    'age_months': 56,
    'weight_kg': 9.5,
    'height_cm': 75.0,
    'gender': 'M',
    'meals_per_day': 4,
    'milk_intake_ml': 500,
    'protein_servings': 2,
    'vegetable_servings': 2,
    'illness_days_last_month': 0,
    'diarrhea_recent': False,
    'fever_recent': False
}

result2 = predictor.predict_risk(malnourished_child, [])

print("\nMalnourished Child (Aditya Nair):")
print(f"  Underweight: {result2['predictions']['underweight']['risk_level']} ({result2['predictions']['underweight']['probability']:.1%})")
print(f"  Stunting: {result2['predictions']['stunting']['risk_level']} ({result2['predictions']['stunting']['probability']:.1%})")
print(f"  Overall: {result2['overall_risk'].upper()}")
