import database as db
import json
from datetime import datetime

conn = db.get_connection()
cursor = conn.cursor(dictionary=True)

query = """
SELECT c.id, c.name, c.date_of_birth, c.gender, g.weight_kg, g.height_cm,
       TIMESTAMPDIFF(MONTH, c.date_of_birth, NOW()) as age_months
FROM children c
JOIN growth_tracking g ON c.id = g.child_id
WHERE g.id = (SELECT MAX(id) FROM growth_tracking WHERE child_id = c.id)
ORDER BY c.name
"""

cursor.execute(query)
children = cursor.fetchall()

print("\n" + "="*80)
print("CHILDREN DATA WITH Z-SCORES")
print("="*80)

from malnutrition_predictor import get_predictor
predictor = get_predictor()

for child in children:
    age_months = child['age_months']
    weight_kg = float(child['weight_kg'])
    height_cm = float(child['height_cm'])
    gender = child['gender']
    
    # Calculate nutritional status
    status = predictor.calculate_nutritional_status(age_months, weight_kg, height_cm, gender)
    
    print(f"\n{child['name']} (ID: {child['id']})")
    print(f"  Age: {age_months} months ({age_months//12}y {age_months%12}m)")
    print(f"  Gender: {gender}")
    print(f"  Weight: {weight_kg} kg")
    print(f"  Height: {height_cm} cm")
    print(f"  Z-Scores:")
    print(f"    WFA (Weight-for-Age): {status['wfa_zscore']:.2f} {'❌ UNDERWEIGHT' if status['is_underweight'] else '✅ Normal'}")
    print(f"    HFA (Height-for-Age): {status['hfa_zscore']:.2f} {'❌ STUNTED' if status['is_stunted'] else '✅ Normal'}")
    print(f"    WFH (Weight-for-Height): {status['wfh_zscore']:.2f} {'❌ WASTED' if status['is_wasted'] else '✅ Normal'}")
    
    # Show WHO thresholds
    if status['wfa_zscore'] < -2.0:
        print(f"      → Severely underweight (< -2 SD)")
    if status['hfa_zscore'] < -2.0:
        print(f"      → Severely stunted (< -2 SD)")
    if status['wfh_zscore'] < -2.0:
        print(f"      → Severely wasted (< -2 SD)")

conn.close()
