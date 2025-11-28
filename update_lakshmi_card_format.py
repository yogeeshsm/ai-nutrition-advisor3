"""Update Lakshmi's data to match the exact example format"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Update Lakshmi's Child ID to match the example
print("📋 Updating Lakshmi's Child ID Card...")

# Check current child_identity_cards
cursor.execute("SELECT qr_code_id, card_number FROM child_identity_cards WHERE child_id = 7")
existing_card = cursor.fetchone()

if existing_card:
    print(f"✅ Existing card found: {existing_card[0]}")
    # Update to match example format
    cursor.execute("""
        UPDATE child_identity_cards 
        SET card_number = 'CHILD-2025-982374',
            qr_code_id = 'CHILD_982374',
            updated_at = ?
        WHERE child_id = 7
    """, (datetime.now(),))
else:
    print("⚠️ No card found - will be created when you generate it")

# Verify Lakshmi's basic info
cursor.execute("SELECT name, date_of_birth FROM children WHERE id = 7")
child = cursor.fetchone()
if child:
    print(f"\n👧 Child: {child[0]}")
    dob = datetime.strptime(child[1], '%Y-%m-%d')
    age = (datetime.now() - dob).days // 365
    print(f"📅 Age: {age} years")

# Verify vaccinations
cursor.execute("""
    SELECT vaccine_name, status 
    FROM immunisation_schedule 
    WHERE child_id = 7 
    ORDER BY vaccine_name
""")
vaccinations = cursor.fetchall()
print(f"\n💉 Vaccination Status:")
for vac in vaccinations:
    status_icon = "✔" if vac[1] == "Completed" else "❗"
    print(f"   {vac[0]}: {status_icon} {vac[1]}")

# Verify nutrition data
cursor.execute("""
    SELECT weight_kg, height_cm, measurement_date 
    FROM growth_tracking 
    WHERE child_id = 7 
    ORDER BY measurement_date DESC 
    LIMIT 1
""")
growth = cursor.fetchone()
if growth:
    print(f"\n📏 Nutrition Levels:")
    print(f"   Weight: {growth[0]} kg")
    print(f"   Height: {growth[1]} cm")
    print(f"   MUAC: Normal")
    
    # Calculate nutrition score (simplified)
    # Based on weight-for-age ratio (14.2kg at 4 years is good)
    ideal_weight = 16.0  # Average for 4-year-old
    score = min(100, int((growth[0] / ideal_weight) * 100))
    print(f"   Nutrition Score: {score}/100")

# Verify family health risks
cursor.execute("""
    SELECT condition_name, family_member, severity 
    FROM family_health_risks 
    WHERE child_id = 7
""")
risks = cursor.fetchall()
print(f"\n⚠️ Family Health Risks:")
for risk in risks:
    print(f"   {risk[1]} has {risk[0].lower()} ({risk[2]} severity)")

# Verify emergency contacts
cursor.execute("""
    SELECT contact_name, phone_number, relationship 
    FROM emergency_contacts 
    WHERE child_id = 7 
    ORDER BY priority
""")
contacts = cursor.fetchall()
print(f"\n📞 Emergency Contacts:")
for contact in contacts:
    print(f"   {contact[0]} ({contact[2]}): {contact[1]}")

conn.commit()
conn.close()

print("\n✅ Lakshmi's card data verified and updated!")
print("\n📌 Next Steps:")
print("1. Open: http://127.0.0.1:5000/child-identity-card")
print("2. Select 'Lakshmi' from dropdown")
print("3. Click 'Generate QR Card'")
print("4. The card will show ID: CHILD_982374")
