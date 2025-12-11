"""Check Lakshmi Iyer's data in database"""
import database as db
from datetime import datetime

conn = db.get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT c.*, g.weight_kg, g.height_cm, g.measurement_date
    FROM children c
    JOIN growth_tracking g ON c.id = g.child_id
    WHERE c.id = 9
    ORDER BY g.measurement_date DESC
    LIMIT 1
""")

child = cursor.fetchone()

dob = child['date_of_birth']
today = datetime.now().date()
if isinstance(dob, datetime):
    dob = dob.date()

age_days = (today - dob).days
age_months = age_days / 30.44

print(f"\n=== CHILD ID 9 DATABASE VALUES ===")
print(f"Name: {child['name']}")
print(f"DOB: {dob}")
print(f"Age: {int(age_months)} months ({age_months:.2f} exact)")
print(f"Gender: {child['gender']}")
print(f"Weight: {float(child['weight_kg'])} kg")
print(f"Height: {float(child['height_cm'])} cm")
print(f"Measurement Date: {child['measurement_date']}")

cursor.close()
conn.close()
