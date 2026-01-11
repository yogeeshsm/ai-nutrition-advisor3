import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

cursor.execute("SELECT id, name, date_of_birth FROM children WHERE name LIKE '%Arun%'")
results = cursor.fetchall()

print('\n🔍 Children named Arun:')
for row in results:
    print(f'   ID {row[0]}: {row[1]} (DOB: {row[2]})')

# Also get their growth data
if results:
    for row in results:
        child_id = row[0]
        cursor.execute("""
            SELECT weight_kg, height_cm, measurement_date 
            FROM growth_tracking 
            WHERE child_id = ? 
            ORDER BY measurement_date DESC 
            LIMIT 1
        """, (child_id,))
        growth = cursor.fetchone()
        if growth:
            print(f'      Latest: {growth[0]} kg, {growth[1]} cm ({growth[2]})')

conn.close()
