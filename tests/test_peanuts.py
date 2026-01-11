import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Search for peanuts
cursor.execute("SELECT name, category, protein_per_100g, iron_per_100g FROM ingredients WHERE LOWER(name) LIKE LOWER('%peanut%')")
results = cursor.fetchall()

print("Found ingredients containing 'peanut':")
for r in results:
    print(f"  ✓ {r[0]} ({r[1]}) - Protein: {r[2]}g, Iron: {r[3]}mg")

conn.close()
