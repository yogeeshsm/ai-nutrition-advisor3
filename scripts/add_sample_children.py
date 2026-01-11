"""
Add sample children data for testing ML Recommendations
Run this script to populate the database with sample children
"""

import sqlite3
from datetime import datetime, timedelta

def add_sample_children():
    """Add sample children with growth measurements for ML testing"""
    
    conn = sqlite3.connect('nutrition_advisor.db')
    cursor = conn.cursor()
    
    # Sample children data
    children_data = [
        {
            'name': 'Ravi Kumar',
            'dob': '2020-03-15',
            'gender': 'M',
            'parent': 'Ramesh Kumar',
            'phone': '9876543210',
            'village': 'Hubballi',
            'weight': 12.5,
            'height': 85.0
        },
        {
            'name': 'Priya Sharma',
            'dob': '2019-08-22',
            'gender': 'F',
            'parent': 'Suresh Sharma',
            'phone': '9876543211',
            'village': 'Dharwad',
            'weight': 14.2,
            'height': 92.5
        },
        {
            'name': 'Arjun Patil',
            'dob': '2021-01-10',
            'gender': 'M',
            'parent': 'Vijay Patil',
            'phone': '9876543212',
            'village': 'Belgaum',
            'weight': 10.8,
            'height': 78.0
        },
        {
            'name': 'Ananya Reddy',
            'dob': '2020-06-18',
            'gender': 'F',
            'parent': 'Krishna Reddy',
            'phone': '9876543213',
            'village': 'Hubballi',
            'weight': 13.0,
            'height': 88.5
        },
        {
            'name': 'Karan Singh',
            'dob': '2019-11-05',
            'gender': 'M',
            'parent': 'Amarjit Singh',
            'phone': '9876543214',
            'village': 'Mysore',
            'weight': 15.5,
            'height': 95.0
        },
        {
            'name': 'Meera Joshi',
            'dob': '2020-09-12',
            'gender': 'F',
            'parent': 'Prakash Joshi',
            'phone': '9876543215',
            'village': 'Dharwad',
            'weight': 12.0,
            'height': 82.0
        },
        {
            'name': 'Aditya Nair',
            'dob': '2021-04-20',
            'gender': 'M',
            'parent': 'Rajesh Nair',
            'phone': '9876543216',
            'village': 'Belgaum',
            'weight': 9.5,
            'height': 75.0
        },
        {
            'name': 'Diya Verma',
            'dob': '2019-12-08',
            'gender': 'F',
            'parent': 'Ajay Verma',
            'phone': '9876543217',
            'village': 'Hubballi',
            'weight': 14.8,
            'height': 93.0
        }
    ]
    
    print("Adding sample children to database...")
    
    for child_data in children_data:
        # Insert child
        cursor.execute("""
            INSERT INTO children (name, date_of_birth, gender, parent_name, phone_number, address, village, health_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            child_data['name'],
            child_data['dob'],
            child_data['gender'],
            child_data['parent'],
            child_data['phone'],
            f"{child_data['village']}, Karnataka",
            child_data['village'],
            'Healthy'
        ))
        
        child_id = cursor.lastrowid
        
        # Add growth measurement
        height_m = child_data['height'] / 100
        bmi = round(child_data['weight'] / (height_m ** 2), 2)
        
        cursor.execute("""
            INSERT INTO growth_tracking (child_id, measurement_date, weight_kg, height_cm, bmi, head_circumference_cm, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            child_id,
            datetime.now().strftime('%Y-%m-%d'),
            child_data['weight'],
            child_data['height'],
            bmi,
            None,
            'Initial measurement'
        ))
        
        print(f"✓ Added: {child_data['name']} (ID: {child_id})")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Successfully added {len(children_data)} children with growth measurements!")
    print("\nYou can now:")
    print("1. Visit http://127.0.0.1:5000/ml-recommendations")
    print("2. Select a child from the dropdown")
    print("3. Explore ML-powered recommendations!")

if __name__ == "__main__":
    try:
        add_sample_children()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("1. Database file exists (nutrition_advisor.db)")
        print("2. Server has been run at least once to create tables")
        print("3. No duplicate children exist")
