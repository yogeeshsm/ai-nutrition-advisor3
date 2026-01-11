"""
Create realistic example child 'Lakshmi' for demonstration
Shows exactly what the app should display per the user's request
"""

import sqlite3
from datetime import datetime, timedelta

def create_example_child_lakshmi():
    """Create detailed example child matching user's example"""
    conn = sqlite3.connect("nutrition_advisor.db")
    cursor = conn.cursor()
    
    print("🧒 Creating Example Child: LAKSHMI\n")
    print("="*60)
    
    # Check if child already exists
    cursor.execute("SELECT id FROM children WHERE name = 'Lakshmi' AND date_of_birth = '2020-11-15'")
    existing = cursor.fetchone()
    
    if existing:
        child_id = existing[0]
        print(f"✅ Lakshmi already exists (ID: {child_id})")
    else:
        # Insert Lakshmi
        cursor.execute("""
            INSERT INTO children 
            (name, date_of_birth, gender, parent_name, phone_number, 
             village, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'Lakshmi',
            '2020-11-15',  # 4 years old
            'Female',
            'Ravi (Father) / Sunita (Mother)',
            '9876543210',
            'Hubballi',
            'House No. 45, Main Road, Hubballi, Karnataka'
        ))
        
        child_id = cursor.lastrowid
        print(f"✅ Created Child: Lakshmi (ID: {child_id})")
    
    # Add/Update Vaccination Data
    print("\n💉 Setting up Vaccinations:")
    
    # Delete existing vaccinations for clean state
    cursor.execute("DELETE FROM immunisation_schedule WHERE child_id = ?", (child_id,))
    
    vaccinations = [
        ('BCG', '2020-11-20', '2020-11-20', 'Completed'),  # Given
        ('OPV 1', '2020-12-20', '2020-12-20', 'Completed'),  # Given
        ('OPV 2', '2021-01-20', '2021-01-20', 'Completed'),  # Given
        ('OPV 3', '2021-02-20', '2021-02-20', 'Completed'),  # Given
        ('DPT 1', '2020-12-20', '2020-12-20', 'Completed'),  # Given
        ('DPT 2', '2021-01-20', '2021-01-20', 'Completed'),  # Given
        ('DPT 3', '2021-02-20', '2021-02-20', 'Completed'),  # Given
        ('MR (Measles-Rubella)', '2021-10-20', None, 'Pending'),  # NOT Given yet
        ('JE (Japanese Encephalitis)', '2024-06-15', None, 'Pending'),
        ('Booster DPT', '2025-11-20', None, 'Pending'),
    ]
    
    for vaccine_name, due_date, given_date, status in vaccinations:
        cursor.execute("""
            INSERT INTO immunisation_schedule 
            (child_id, vaccine_name, due_date, administered_date, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (child_id, vaccine_name, due_date, given_date, status, 'Standard childhood vaccination'))
        
        if given_date:
            print(f"   ✔ {vaccine_name} - Completed")
        else:
            print(f"   ❗ {vaccine_name} - Pending (Due: {due_date})")
    
    # Add/Update Growth Tracking (Nutrition Data)
    print("\n📏 Setting up Nutrition & Growth Data:")
    
    cursor.execute("DELETE FROM growth_tracking WHERE child_id = ?", (child_id,))
    
    # Add multiple measurements to show history
    measurements = [
        ('2021-02-15', 5.2, 56),      # 3 months
        ('2021-05-15', 6.8, 63),      # 6 months
        ('2021-08-15', 8.5, 70),      # 9 months
        ('2021-11-15', 10.2, 77),     # 12 months
        ('2022-02-15', 11.5, 83),     # 15 months
        ('2022-05-15', 12.8, 90),     # 18 months
        ('2022-11-15', 13.5, 95),     # 2 years
        ('2023-11-15', 14.0, 96),     # 3 years
        ('2024-11-15', 14.2, 97),     # Latest: 4 years - CURRENT
    ]
    
    for measurement_date, weight, height in measurements:
        cursor.execute("""
            INSERT INTO growth_tracking 
            (child_id, measurement_date, weight_kg, height_cm)
            VALUES (?, ?, ?, ?)
        """, (child_id, measurement_date, weight, height))
        
        # Mark latest as current
        if measurement_date == '2024-11-15':
            print(f"   📊 Current: Weight {weight}kg | Height {height}cm | MUAC: Normal")
        else:
            print(f"   📈 {measurement_date}: Weight {weight}kg | Height {height}cm")
    
    # Add/Update Emergency Contacts
    print("\n🚨 Setting up Emergency Contacts:")
    
    cursor.execute("DELETE FROM emergency_contacts WHERE child_id = ?", (child_id,))
    
    emergency_contacts = [
        ('Ravi (Father)', '9876543210', 'Phone', 'Father', 1),
        ('Sunita (Mother)', '9876543211', 'Phone', 'Mother', 2),
        ('Aunt (Rajini)', '9829345234', 'Phone', 'Aunt', 3),
        ('Health Center', '080-26667644', 'Phone', 'Healthcare', 4),
    ]
    
    for name, phone, contact_type, relationship, priority in emergency_contacts:
        cursor.execute("""
            INSERT INTO emergency_contacts 
            (child_id, contact_name, phone_number, contact_type, relationship, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (child_id, name, phone, contact_type, relationship, priority))
        
        print(f"   📞 {name}: {phone}")
    
    # Add/Update Family Health Risks
    print("\n⚠️  Setting up Family Health Risks:")
    
    cursor.execute("DELETE FROM family_health_risks WHERE child_id = ?", (child_id,))
    
    health_risks = [
        ('Anemia', 'High', 'Mother', 'Sunita has iron deficiency anemia. Monitor Lakshmi\'s iron levels and ensure iron-rich diet'),
        ('Hypertension', 'Medium', 'Father', 'Ravi has high BP. Monitor Lakshmi\'s blood pressure regularly, low sodium diet'),
    ]
    
    for condition, severity, family_member, precautions in health_risks:
        cursor.execute("""
            INSERT INTO family_health_risks 
            (child_id, condition_name, severity, family_member, description, precautions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (child_id, condition, severity, family_member, '', precautions))
        
        print(f"   🔴 {condition} ({severity}) - {family_member}")
        print(f"      → {precautions}\n")
    
    conn.commit()
    conn.close()
    
    print("="*60)
    print("\n✨ Example child 'LAKSHMI' created successfully!\n")
    print("📊 LAKSHMI'S PROFILE:")
    print("   • Name: Lakshmi")
    print("   • Age: 4 years")
    print("   • Child ID: CHILD-2025-{:05d}".format(child_id))
    print("   • Location: Hubballi, Karnataka")
    print("   • Current Weight: 14.2 kg")
    print("   • Current Height: 97 cm")
    print("   • Nutrition Score: 78/100")
    print("   • Vaccinations: 7/10 Completed (1 Pending)")
    print("   • Health Risks: Mother (Anemia), Father (Hypertension)")
    print("\n🎯 Next Steps:")
    print("   1. Open http://127.0.0.1:5000/child-identity-card")
    print("   2. Select 'Lakshmi' from dropdown")
    print("   3. Click 'Generate QR Card'")
    print("   4. Test ASHA workflow at http://127.0.0.1:5000/child-identity-scanner")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print("\n")
    create_example_child_lakshmi()
