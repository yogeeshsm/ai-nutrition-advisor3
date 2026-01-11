import database

df = database.get_all_ingredients()
print(f'Total ingredients: {len(df)}')
print('\nBy category:')
cat_counts = df.groupby('category')['name'].count().sort_values(ascending=False)
print(cat_counts)

print('\n\nDetailed list by category:')
for cat in sorted(df['category'].unique()):
    print(f'\n{cat} ({len(df[df["category"]==cat])} items):')
    items = df[df['category']==cat][['name', 'calories_per_100g', 'cost_per_kg']].values
    for item in items:
        print(f'  - {item[0]}: {item[1]} cal, ₹{item[2]}/kg')
