"""
Debug script to see what features are being generated for predictions
"""

from malnutrition_predictor import get_predictor
import database as db
from datetime import datetime

def debug_prediction(child_id):
    """Show detailed feature preparation and prediction for a child"""
    
    predictor = get_predictor()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get child data
    cursor.execute("""
        SELECT c.*, g.weight_kg, g.height_cm, g.measurement_date
        FROM children c
        LEFT JOIN growth_tracking g ON c.id = g.child_id
        WHERE c.id = %s
        ORDER BY g.measurement_date DESC
        LIMIT 1
    """, (child_id,))
    
    child = cursor.fetchone()
    
    if not child:
        print(f"❌ Child ID {child_id} not found")
        return
    
    # Calculate age
    dob = child['date_of_birth']
    today = datetime.now().date()
    age_days = (today - dob).days
    age_months = age_days // 30
    
    print(f"\n{'='*80}")
    print(f"DEBUGGING PREDICTION FOR: {child['name']} (ID: {child_id})")
    print(f"{'='*80}")
    print(f"Age: {age_months} months")
    print(f"Gender: {child['gender']}")
    print(f"Weight: {child['weight_kg']} kg")
    print(f"Height: {child['height_cm']} cm")
    
    # Convert Decimal to float (MySQL returns Decimal objects)
    weight_kg = float(child['weight_kg'])
    height_cm = float(child['height_cm'])
    
    # Calculate Z-scores
    status = predictor.calculate_nutritional_status(
        age_months, 
        weight_kg, 
        height_cm, 
        child['gender']
    )
    
    print(f"\nZ-SCORES:")
    print(f"  WFA: {status['wfa_zscore']:.2f} ({'❌ UNDERWEIGHT' if status['is_underweight'] else '✅ Normal'})")
    print(f"  HFA: {status['hfa_zscore']:.2f} ({'❌ STUNTED' if status['is_stunted'] else '✅ Normal'})")
    print(f"  WFH: {status['wfh_zscore']:.2f} ({'❌ WASTED' if status['is_wasted'] else '✅ Normal'})")
    
    # Prepare child data dict
    child_data = {
        'age_months': age_months,
        'weight_kg': weight_kg,
        'height_cm': height_cm,
        'gender': child['gender'],
        'meals_per_day': 4,  # Default values
        'milk_intake_ml': 500,
        'protein_servings': 2,
        'vegetable_servings': 2,
        'illness_days_last_month': 0,
        'diarrhea_recent': False,
        'fever_recent': False
    }
    
    # Get growth history
    cursor.execute("""
        SELECT weight_kg as weight, height_cm as height, 
               FLOOR(DATEDIFF(measurement_date, %s) / 30) as age_months
        FROM growth_tracking
        WHERE child_id = %s
        ORDER BY measurement_date ASC
    """, (dob, child_id))
    
    growth_history = cursor.fetchall()
    
    # Prepare features
    features = predictor.prepare_features(child_data, growth_history)
    
    print(f"\nFEATURES ARRAY (used for ML prediction):")
    feature_names = [
        'age_months', 'weight_kg', 'height_cm', 'is_male',
        'wfa_zscore', 'hfa_zscore', 'wfh_zscore',
        'weight_velocity', 'height_velocity',
        'meals_per_day', 'milk_intake_ml', 'protein_servings', 'vegetable_servings',
        'illness_days', 'has_diarrhea', 'has_fever'
    ]
    
    for i, (name, value) in enumerate(zip(feature_names, features[0])):
        print(f"  {name:25s}: {value:10.3f}")
    
    # Get predictions
    result = predictor.predict_risk(child_data, growth_history)
    
    print(f"\nMODEL PREDICTIONS:")
    for condition, pred in result['predictions'].items():
        print(f"  {condition:12s}: {pred['risk_level']:8s} (prob: {pred['probability']:.1%})")
    
    print(f"\nOVERALL RISK: {result['overall_risk'].upper()}")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    print("\n" + "="*80)
    print("HEALTHY CHILD (Lakshmi Iyer - Should be LOW RISK)")
    print("="*80)
    debug_prediction(9)  # Lakshmi Iyer - healthy child
    
    print("\n\n" + "="*80)
    print("MALNOURISHED CHILD (Aditya Nair - Should be HIGH RISK)")
    print("="*80)
    debug_prediction(7)  # Aditya Nair - severely malnourished
