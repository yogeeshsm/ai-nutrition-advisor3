"""
Add missing ingredients to the database
"""
import sqlite3

# Ingredients to add with nutritional data (per 100g)
ingredients_to_add = [
    {
        'name': 'Soya Chunks',
        'category': 'Protein',
        'cost_per_kg': 120.0,
        'protein_per_100g': 52.0,
        'carbs_per_100g': 33.0,
        'fat_per_100g': 0.5,
        'calories_per_100g': 345,
        'fiber_per_100g': 13.0,
        'iron_per_100g': 20.0,
        'calcium_per_100g': 350.0
    },
    {
        'name': 'Fenugreek Leaves (Methi)',
        'category': 'Vegetables',
        'cost_per_kg': 60.0,
        'protein_per_100g': 4.4,
        'carbs_per_100g': 6.0,
        'fat_per_100g': 0.9,
        'calories_per_100g': 49,
        'fiber_per_100g': 24.6,
        'iron_per_100g': 33.5,
        'calcium_per_100g': 395.0
    },
    {
        'name': 'Sesame Seeds (Til)',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 200.0,
        'protein_per_100g': 17.7,
        'carbs_per_100g': 23.4,
        'fat_per_100g': 49.7,
        'calories_per_100g': 573,
        'fiber_per_100g': 11.8,
        'iron_per_100g': 14.6,
        'calcium_per_100g': 975.0
    },
    {
        'name': 'Chia Seeds',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 400.0,
        'protein_per_100g': 16.5,
        'carbs_per_100g': 42.1,
        'fat_per_100g': 30.7,
        'calories_per_100g': 486,
        'fiber_per_100g': 34.4,
        'iron_per_100g': 7.7,
        'calcium_per_100g': 631.0
    },
    {
        'name': 'Poha (Flattened Rice)',
        'category': 'Grains',
        'cost_per_kg': 60.0,
        'protein_per_100g': 6.6,
        'carbs_per_100g': 76.9,
        'fat_per_100g': 1.2,
        'calories_per_100g': 346,
        'fiber_per_100g': 2.2,
        'iron_per_100g': 20.0,
        'calcium_per_100g': 21.0
    },
    {
        'name': 'Pumpkin Seeds',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 500.0,
        'protein_per_100g': 30.2,
        'carbs_per_100g': 10.7,
        'fat_per_100g': 49.0,
        'calories_per_100g': 559,
        'fiber_per_100g': 6.0,
        'iron_per_100g': 8.8,
        'calcium_per_100g': 46.0
    },
    {
        'name': 'Curry Leaves',
        'category': 'Vegetables',
        'cost_per_kg': 40.0,
        'protein_per_100g': 6.1,
        'carbs_per_100g': 18.7,
        'fat_per_100g': 1.0,
        'calories_per_100g': 108,
        'fiber_per_100g': 6.4,
        'iron_per_100g': 1.0,
        'calcium_per_100g': 830.0
    },
    {
        'name': 'Rajma (Kidney Beans)',
        'category': 'Protein',
        'cost_per_kg': 100.0,
        'protein_per_100g': 22.9,
        'carbs_per_100g': 60.0,
        'fat_per_100g': 0.8,
        'calories_per_100g': 333,
        'fiber_per_100g': 24.9,
        'iron_per_100g': 8.2,
        'calcium_per_100g': 143.0
    },
    {
        'name': 'Moong Dal',
        'category': 'Protein',
        'cost_per_kg': 80.0,
        'protein_per_100g': 24.0,
        'carbs_per_100g': 59.0,
        'fat_per_100g': 1.2,
        'calories_per_100g': 347,
        'fiber_per_100g': 16.3,
        'iron_per_100g': 6.7,
        'calcium_per_100g': 124.0
    },
    {
        'name': 'Masoor Dal',
        'category': 'Protein',
        'cost_per_kg': 90.0,
        'protein_per_100g': 25.8,
        'carbs_per_100g': 60.1,
        'fat_per_100g': 1.1,
        'calories_per_100g': 352,
        'fiber_per_100g': 30.5,
        'iron_per_100g': 7.5,
        'calcium_per_100g': 69.0
    },
    {
        'name': 'Flax Seeds (Alsi)',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 300.0,
        'protein_per_100g': 18.3,
        'carbs_per_100g': 28.9,
        'fat_per_100g': 42.2,
        'calories_per_100g': 534,
        'fiber_per_100g': 27.3,
        'iron_per_100g': 5.7,
        'calcium_per_100g': 255.0
    },
    {
        'name': 'Mint Leaves (Pudina)',
        'category': 'Vegetables',
        'cost_per_kg': 50.0,
        'protein_per_100g': 3.8,
        'carbs_per_100g': 14.9,
        'fat_per_100g': 0.9,
        'calories_per_100g': 70,
        'fiber_per_100g': 8.0,
        'iron_per_100g': 5.1,
        'calcium_per_100g': 243.0
    },
    {
        'name': 'Almonds',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 600.0,
        'protein_per_100g': 21.2,
        'carbs_per_100g': 21.6,
        'fat_per_100g': 49.9,
        'calories_per_100g': 579,
        'fiber_per_100g': 12.5,
        'iron_per_100g': 3.7,
        'calcium_per_100g': 269.0
    },
    {
        'name': 'Peanuts',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 150.0,
        'protein_per_100g': 25.8,
        'carbs_per_100g': 16.1,
        'fat_per_100g': 49.2,
        'calories_per_100g': 567,
        'fiber_per_100g': 8.5,
        'iron_per_100g': 4.6,
        'calcium_per_100g': 92.0
    },
    {
        'name': 'Groundnuts',
        'category': 'Seeds/Nuts',
        'cost_per_kg': 140.0,
        'protein_per_100g': 26.0,
        'carbs_per_100g': 16.0,
        'fat_per_100g': 49.0,
        'calories_per_100g': 570,
        'fiber_per_100g': 8.5,
        'iron_per_100g': 4.5,
        'calcium_per_100g': 90.0
    }
]

def add_ingredients():
    """Add ingredients to database"""
    conn = sqlite3.connect('nutrition_advisor.db')
    cursor = conn.cursor()
    
    added_count = 0
    skipped_count = 0
    
    for ing in ingredients_to_add:
        # Check if ingredient already exists
        cursor.execute("SELECT id FROM ingredients WHERE LOWER(name) = LOWER(?)", (ing['name'],))
        exists = cursor.fetchone()
        
        if exists:
            print(f"⚠️  '{ing['name']}' already exists, skipping...")
            skipped_count += 1
            continue
        
        # Insert ingredient
        try:
            cursor.execute("""
                INSERT INTO ingredients (
                    name, category, cost_per_kg, protein_per_100g, carbs_per_100g,
                    fat_per_100g, calories_per_100g, fiber_per_100g, iron_per_100g,
                    calcium_per_100g
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ing['name'], ing['category'], ing['cost_per_kg'], ing['protein_per_100g'],
                ing['carbs_per_100g'], ing['fat_per_100g'], ing['calories_per_100g'],
                ing['fiber_per_100g'], ing['iron_per_100g'], ing['calcium_per_100g']
            ))
            print(f"✅ Added '{ing['name']}' ({ing['category']})")
            added_count += 1
        except Exception as e:
            print(f"❌ Error adding '{ing['name']}': {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Added {added_count} new ingredients")
    print(f"⚠️  Skipped {skipped_count} existing ingredients")
    print(f"{'='*60}")
    
    # Verify total count
    conn = sqlite3.connect('nutrition_advisor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    total = cursor.fetchone()[0]
    conn.close()
    
    print(f"📊 Total ingredients in database: {total}")
    print("\n✅ All ingredients are now available for ML recommendations!")

if __name__ == "__main__":
    print("Adding missing ingredients to database...")
    print(f"{'='*60}\n")
    add_ingredients()
