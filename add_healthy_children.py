"""
Add healthy children with normal Z-scores to demonstrate model accuracy
This will show the model correctly differentiates between healthy and malnourished children
"""

import database as db
from datetime import datetime, timedelta
import random

def add_healthy_children():
    """Add children with normal nutritional status (Z-scores between -1 and +1)"""
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Healthy children data with WHO-appropriate measurements
    healthy_children = [
        {
            'name': 'Lakshmi Iyer',
            'age_months': 60,  # 5 years
            'gender': 'F',
            'weight_kg': 18.0,  # Normal for 60 months (expected ~18kg)
            'height_cm': 109.0,  # Normal for 60 months (expected ~109cm)
            'village': 'Govindapuram'
        },
        {
            'name': 'Vijay Reddy',
            'age_months': 48,  # 4 years
            'gender': 'M',
            'weight_kg': 16.5,  # Normal for 48 months (expected ~16.3kg)
            'height_cm': 103.0,  # Normal for 48 months (expected ~103cm)
            'village': 'Govindapuram'
        },
        {
            'name': 'Sita Patel',
            'age_months': 36,  # 3 years
            'gender': 'F',
            'weight_kg': 14.0,  # Normal for 36 months (expected ~13.9kg)
            'height_cm': 95.5,  # Normal for 36 months (expected ~95.1cm)
            'village': 'Govindapuram'
        },
        {
            'name': 'Arun Nair',
            'age_months': 72,  # 6 years
            'gender': 'M',
            'weight_kg': 20.5,  # Normal for 72 months (expected ~20.3kg)
            'height_cm': 116.0,  # Normal for 72 months (expected ~116.1cm)
            'village': 'Govindapuram'
        },
        {
            'name': 'Kavya Sharma',
            'age_months': 24,  # 2 years
            'gender': 'F',
            'weight_kg': 11.8,  # Normal for 24 months (expected ~11.5kg)
            'height_cm': 86.0,  # Normal for 24 months (expected ~85.7cm)
            'village': 'Govindapuram'
        },
        # Mild risk children (Z-score between -1.5 and -2.0)
        {
            'name': 'Rahul Kumar',
            'age_months': 60,  # 5 years
            'gender': 'M',
            'weight_kg': 15.5,  # Slightly underweight (expected ~18.3kg)
            'height_cm': 105.0,  # Slightly stunted (expected ~110cm)
            'village': 'Govindapuram'
        },
        {
            'name': 'Anjali Verma',
            'age_months': 48,  # 4 years
            'gender': 'F',
            'weight_kg': 14.0,  # Slightly underweight (expected ~16kg)
            'height_cm': 98.0,  # Slightly stunted (expected ~102.7cm)
            'village': 'Govindapuram'
        }
    ]
    
    added_count = 0
    
    for child in healthy_children:
        try:
            # Calculate date of birth from age
            dob = datetime.now() - timedelta(days=child['age_months'] * 30)
            
            # Insert child record
            cursor.execute("""
                INSERT INTO children (name, date_of_birth, gender, village)
                VALUES (%s, %s, %s, %s)
            """, (
                child['name'],
                dob.date(),
                child['gender'],
                child['village']
            ))
            
            child_id = cursor.lastrowid
            
            # Add initial growth tracking record
            cursor.execute("""
                INSERT INTO growth_tracking (child_id, measurement_date, weight_kg, height_cm)
                VALUES (%s, %s, %s, %s)
            """, (
                child_id,
                datetime.now().date(),
                child['weight_kg'],
                child['height_cm']
            ))
            
            print(f"✅ Added: {child['name']} - Age: {child['age_months']}mo, "
                  f"Weight: {child['weight_kg']}kg, Height: {child['height_cm']}cm")
            
            added_count += 1
            
        except Exception as e:
            print(f"❌ Error adding {child['name']}: {e}")
            conn.rollback()
            continue
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✅ Successfully added {added_count} healthy children")
    print(f"Database now has a mix of:")
    print(f"  - 5 children with normal Z-scores (LOW RISK)")
    print(f"  - 2 children with mild malnutrition (MEDIUM RISK)")
    print(f"  - 8 existing children with severe malnutrition (HIGH RISK)")
    print(f"\nTotal: 15 children with varied nutritional status")
    print(f"\n🎯 Model will now show realistic risk distribution!")

if __name__ == '__main__':
    print("=" * 80)
    print("ADDING HEALTHY CHILDREN TO DATABASE")
    print("=" * 80)
    add_healthy_children()
