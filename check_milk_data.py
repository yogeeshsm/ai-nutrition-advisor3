import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Get USDA milk data
cursor.execute('''SELECT food_name, calories_per_100g, protein_per_100g, 
                  carbs_per_100g, fat_per_100g, calcium_per_100g 
                  FROM usda_nutrition_cache 
                  WHERE food_name LIKE "%milk%"''')

rows = cursor.fetchall()

print("\n=== USDA Verified Milk Data (per 100g/100ml) ===\n")
for row in rows:
    print(f"Food: {row[0]}")
    print(f"  Calories: {row[1]} kcal per 100ml")
    print(f"  Protein: {row[2]}g per 100ml")
    print(f"  Carbs: {row[3]}g per 100ml")
    print(f"  Fat: {row[4]}g per 100ml")
    print(f"  Calcium: {row[5]}mg per 100ml")
    print(f"\nFor 1 Liter (1000ml):")
    print(f"  Calories: {row[1] * 10} kcal")
    print(f"  Protein: {row[2] * 10}g")
    print(f"  Carbs: {row[3] * 10}g")
    print(f"  Fat: {row[4] * 10}g")
    print(f"  Calcium: {row[5] * 10}mg")
    print("-" * 50)

conn.close()
