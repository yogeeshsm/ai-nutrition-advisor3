"""
Quick test script to update ingredients with USDA data
"""

from usda_nutrition_manager import get_nutrition_manager, INDIAN_FOOD_USDA_MAPPING

def main():
    print("🚀 USDA Nutrition Data Update Tool\n")
    
    manager = get_nutrition_manager()
    
    # Show cache stats
    stats = manager.get_cache_stats()
    print(f"📊 Current Cache Stats:")
    print(f"   Total cached items: {stats['total_items']}")
    print(f"   Recent updates (7 days): {stats['recent_updates']}")
    print(f"   Verified items: {stats['verified_items']}\n")
    
    # Test with a few ingredients first
    print("Testing with sample ingredients...\n")
    test_ingredients = ["Rice", "Banana", "Milk", "Eggs", "Almonds"]
    
    for ingredient in test_ingredients:
        search_term = INDIAN_FOOD_USDA_MAPPING.get(ingredient, ingredient)
        print(f"\n📝 Testing: {ingredient} (searching for: {search_term})")
        
        data = manager.get_nutrition_data(search_term)
        if data:
            print(f"   ✅ Calories: {data['calories']} kcal")
            print(f"   ✅ Protein: {data['protein']}g")
            print(f"   ✅ Carbs: {data['carbs']}g")
            print(f"   ✅ Data source: {data['data_source']}")
        else:
            print(f"   ❌ No data found")
    
    print("\n" + "="*60)
    print("Would you like to update ALL ingredients? (y/n)")
    choice = input().strip().lower()
    
    if choice == 'y':
        print("\n🔄 Starting bulk update...")
        updated, failed = manager.bulk_update_ingredients(INDIAN_FOOD_USDA_MAPPING)
        
        print(f"\n✅ Update complete!")
        print(f"   Updated: {updated} ingredients")
        print(f"   Failed: {failed} ingredients")
    else:
        print("\n✅ Test complete! Run this script again to update all ingredients.")

if __name__ == "__main__":
    main()
