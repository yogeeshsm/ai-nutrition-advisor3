import sqlite3

conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()

# Check children count
cursor.execute('SELECT COUNT(*) FROM children')
total_children = cursor.fetchone()[0]
print(f'\n✓ Total children in database: {total_children}')

if total_children > 0:
    # Show sample children
    cursor.execute('SELECT id, name, date_of_birth, gender FROM children LIMIT 5')
    print('\n✓ Sample children:')
    for row in cursor.fetchall():
        print(f'   ID {row[0]}: {row[1]} ({row[2]}, {row[3]})')
    
    # Check growth tracking
    cursor.execute('SELECT COUNT(*) FROM growth_tracking')
    growth_count = cursor.fetchone()[0]
    print(f'\n✓ Growth tracking records: {growth_count}')
    
    # Check meal plans
    cursor.execute('SELECT COUNT(*) FROM meal_plans')
    meal_count = cursor.fetchone()[0]
    print(f'✓ Meal plans: {meal_count}')
    
else:
    print('\n❌ NO CHILDREN IN DATABASE!')
    print('   ML Recommendations need children data to work.')

conn.close()
