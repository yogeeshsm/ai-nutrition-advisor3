"""
Add test children to database for Child Identity Card feature
This script populates sample children with vaccination and nutrition data
"""

import sqlite3
from datetime import datetime, timedelta
import random

def add_test_children():
    """Add sample children with complete health data"""
    conn = sqlite3.connect("nutrition_advisor.db")
    cursor = conn.cursor()
    
    # Sample children data (Indian names and villages)
    children_data = [
        {
            'name': 'Aarav Singh',
            'date_of_birth': '2023-03-15',
            'gender': 'Male',
            'parent_name': 'Rajesh Singh (Father) / Priya Singh (Mother)',
            'phone_number': '9876543210',
            'village': 'Hubballi',
            'address': 'House No. 45, Main Road, Hubballi',
            'nutrition_status': 'Normal'
        },
        {
            'name': 'Anaya Patel',
            'date_of_birth': '2023-07-22',
            'gender': 'Female',
            'parent_name': 'Vikram Patel (Father) / Divya Patel (Mother)',
            'phone_number': '9876543211',
            'village': 'Belgaum',
            'address': 'Belgaum Town, Near Market',
            'nutrition_status': 'Normal'
        },
        {
            'name': 'Arjun Kumar',
            'date_of_birth': '2023-01-10',
            'gender': 'Male',
            'parent_name': 'Suresh Kumar (Father) / Lakshmi Kumar (Mother)',
            'phone_number': '9876543212',
            'village': 'Ramanagara',
            'address': 'Ramanagara Village, Near Health Center',
            'nutrition_status': 'Underweight'
        },
        {
            'name': 'Diya Sharma',
            'date_of_birth': '2023-05-08',
            'gender': 'Female',
            'parent_name': 'Amit Sharma (Father) / Neha Sharma (Mother)',
            'phone_number': '9876543213',
            'village': 'Bangalore',
            'address': 'Bangalore City, Whitefield Area',
            'nutrition_status': 'Normal'
        },
        {
            'name': 'Rohan Gupta',
            'date_of_birth': '2023-11-30',
            'gender': 'Male',
            'parent_name': 'Anil Gupta (Father) / Pooja Gupta (Mother)',
            'phone_number': '9876543214',
            'village': 'Mysore',
            'address': 'Mysore City, Residential Area',
            'nutrition_status': 'Normal'
        }
    ]
    
    print("📝 Adding test children to database...\n")
    
    for child_data in children_data:
        try:
            # Check if child already exists
            cursor.execute("SELECT id FROM children WHERE name = ? AND date_of_birth = ?", 
                         (child_data['name'], child_data['date_of_birth']))
            
            if cursor.fetchone():
                print(f"⏭️  {child_data['name']} already exists, skipping...")
                continue
            
            # Insert child
            cursor.execute("""
                INSERT INTO children 
                (name, date_of_birth, gender, parent_name, phone_number, 
                 village, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                child_data['name'],
                child_data['date_of_birth'],
                child_data['gender'],
                child_data['parent_name'],
                child_data['phone_number'],
                child_data['village'],
                child_data['address']
            ))
            
            child_id = cursor.lastrowid
            print(f"✅ Added: {child_data['name']} (ID: {child_id})")
            
            # Add sample emergency contacts
            add_emergency_contacts(cursor, child_id, child_data)
            
            # Add sample health risks if needed
            if random.random() > 0.7:  # 30% chance
                try:
                    add_family_health_risks(cursor, child_id)
                except Exception as e:
                    print(f"   ⚠️  Skipping health risks: {e}")
        
        except Exception as e:
            print(f"❌ Error adding {child_data['name']}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✨ Sample data added successfully!")
    print("\n🎯 Now you can:")
    print("   1. Open http://127.0.0.1:5000/child-identity-card")
    print("   2. Select a child from the dropdown")
    print("   3. Click 'Generate QR Card'")
    print("   4. Test the QR scanner at http://127.0.0.1:5000/child-identity-scanner")


def add_sample_vaccinations(cursor, child_id):
    """Add sample vaccinations for a child"""
    vaccines = [
        ('BCG', '2023-03-20', '2023-03-20'),
        ('OPV 1', '2023-04-20', '2023-04-20'),
        ('Pentavalent 1', '2023-04-20', '2023-04-20'),
        ('PCV 1', '2023-04-20', '2023-04-20'),
        ('Rotavirus 1', '2023-04-20', '2023-04-20'),
        ('OPV 2', '2023-05-20', '2023-05-20'),
        ('Pentavalent 2', '2023-05-20', '2023-05-20'),
        ('PCV 2', '2023-05-20', '2023-05-20'),
        ('Rotavirus 2', '2023-05-20', '2023-05-20'),
        ('OPV 3', '2023-06-20', '2023-06-20'),
        ('Pentavalent 3', '2023-06-20', '2023-06-20'),
        ('DPT Booster 1', '2025-12-15', None),  # Pending
    ]
    
    for vaccine_name, scheduled_date, date_given in vaccines:
        cursor.execute("""
            INSERT INTO vaccinations 
            (child_id, vaccine_name, scheduled_date, date_given)
            VALUES (?, ?, ?, ?)
        """, (child_id, vaccine_name, scheduled_date, date_given))


def add_sample_growth_data(cursor, child_id, dob):
    """Add sample growth tracking data"""
    base_date = datetime.strptime(dob, '%Y-%m-%d')
    
    # Add measurements every month
    for i in range(0, 10, 3):
        measurement_date = base_date + timedelta(days=30*i)
        weight = 3.5 + (i * 0.8)  # Approximate weight gain
        height = 50 + (i * 1.5)   # Approximate height gain
        
        cursor.execute("""
            INSERT INTO growth_tracking 
            (child_id, measurement_date, weight_kg, height_cm)
            VALUES (?, ?, ?, ?)
        """, (child_id, measurement_date.strftime('%Y-%m-%d'), weight, height))


def add_emergency_contacts(cursor, child_id, child_data):
    """Add emergency contacts"""
    contacts = [
        ('Mother (from parent_name)', '9876543210', 'Mother', 1),
        ('Father (from parent_name)', '9876543211', 'Father', 2),
        ('Nearest Health Center', '9876543212', 'Healthcare', 3),
    ]
    
    for contact_name, phone, relation, priority in contacts:
        cursor.execute("""
            INSERT INTO emergency_contacts 
            (child_id, contact_name, phone_number, contact_type, relationship, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (child_id, contact_name, phone, 'Phone', relation, priority))


def add_family_health_risks(cursor, child_id):
    """Add sample family health risks"""
    risks = [
        ('Diabetes', 'High', 'Grandfather', 'Monitor blood sugar levels regularly'),
        ('Asthma', 'Medium', 'Aunt', 'Avoid dust and allergens'),
        ('Hypertension', 'Medium', 'Grandmother', 'Low sodium diet'),
    ]
    
    selected_risks = random.sample(risks, random.randint(1, 2))
    
    for condition, severity, family_member, precautions in selected_risks:
        cursor.execute("""
            INSERT INTO family_health_risks 
            (child_id, condition_name, severity, family_member, precautions)
            VALUES (?, ?, ?, ?, ?)
        """, (child_id, condition, severity, family_member, precautions))


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧒 CHILD IDENTITY CARD - TEST DATA GENERATOR")
    print("="*60 + "\n")
    
    add_test_children()
    
    print("\n" + "="*60)
    print("✨ Ready to test Child Identity Card feature!")
    print("="*60 + "\n")
