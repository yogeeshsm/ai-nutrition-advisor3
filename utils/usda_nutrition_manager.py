"""
USDA Nutrition Data Fetcher with Smart Caching
Replaces hardcoded nutrition values with real USDA API data
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from usda_api import get_usda_api

class NutritionDataManager:
    """Manages nutrition data with USDA API integration and local caching"""
    
    def __init__(self, db_path="nutrition_advisor.db"):
        self.db_path = db_path
        self.usda_api = get_usda_api()
        self._ensure_cache_table()
    
    def _ensure_cache_table(self):
        """Create cache table for storing USDA nutrition data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usda_nutrition_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL UNIQUE,
                fdc_id INTEGER,
                calories_per_100g REAL,
                protein_per_100g REAL,
                carbs_per_100g REAL,
                fat_per_100g REAL,
                fiber_per_100g REAL,
                iron_per_100g REAL,
                calcium_per_100g REAL,
                vitamin_a_per_100g REAL,
                vitamin_c_per_100g REAL,
                sodium_per_100g REAL,
                data_source TEXT DEFAULT 'USDA',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_verified INTEGER DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ USDA nutrition cache table initialized")
    
    def get_nutrition_data(self, food_name: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Get nutrition data for a food item
        
        Args:
            food_name: Name of the food item
            use_cache: Whether to use cached data (default: True)
            
        Returns:
            Dictionary with nutrition data or None if not found
        """
        # Check cache first
        if use_cache:
            cached_data = self._get_from_cache(food_name)
            if cached_data:
                print(f"✅ Using cached USDA data for: {food_name}")
                return cached_data
        
        # Fetch from USDA API
        if self.usda_api:
            print(f"🔍 Fetching USDA data for: {food_name}")
            nutrition = self._fetch_from_usda(food_name)
            if nutrition:
                # Save to cache
                self._save_to_cache(food_name, nutrition)
                return nutrition
        
        print(f"⚠️ No USDA data found for: {food_name}")
        return None
    
    def _get_from_cache(self, food_name: str) -> Optional[Dict]:
        """Retrieve nutrition data from cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data exists and is not too old (refresh after 30 days)
        cursor.execute("""
            SELECT * FROM usda_nutrition_cache 
            WHERE LOWER(food_name) = LOWER(?)
            AND datetime(last_updated) > datetime('now', '-30 days')
        """, (food_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'fdc_id': row[2],
                'calories': row[3],
                'protein': row[4],
                'carbs': row[5],
                'fat': row[6],
                'fiber': row[7],
                'iron': row[8],
                'calcium': row[9],
                'vitamin_a': row[10],
                'vitamin_c': row[11],
                'sodium': row[12],
                'data_source': row[13],
                'is_verified': row[15] == 1
            }
        
        return None
    
    def _fetch_from_usda(self, food_name: str) -> Optional[Dict]:
        """Fetch nutrition data from USDA API"""
        try:
            # Search for the food
            search_results = self.usda_api.search_foods(food_name, page_size=3)
            
            if not search_results:
                return None
            
            # Try to get the best match (first result is usually best)
            for result in search_results:
                fdc_id = result.get('fdc_id')
                summary = self.usda_api.get_nutrition_summary(fdc_id)
                
                if summary:
                    return {
                        'fdc_id': fdc_id,
                        'calories': summary.get('calories', 0),
                        'protein': summary.get('protein', 0),
                        'carbs': summary.get('carbs', 0),
                        'fat': summary.get('fat', 0),
                        'fiber': summary.get('fiber', 0),
                        'iron': summary.get('iron', 0),
                        'calcium': summary.get('calcium', 0),
                        'vitamin_a': summary.get('vitamin_a', 0),
                        'vitamin_c': summary.get('vitamin_c', 0),
                        'sodium': summary.get('sodium', 0),
                        'data_source': 'USDA FoodData Central',
                        'is_verified': True
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Error fetching USDA data for {food_name}: {e}")
            return None
    
    def _save_to_cache(self, food_name: str, nutrition: Dict):
        """Save nutrition data to cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO usda_nutrition_cache 
            (food_name, fdc_id, calories_per_100g, protein_per_100g, carbs_per_100g,
             fat_per_100g, fiber_per_100g, iron_per_100g, calcium_per_100g,
             vitamin_a_per_100g, vitamin_c_per_100g, sodium_per_100g,
             data_source, is_verified, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            food_name,
            nutrition.get('fdc_id'),
            nutrition.get('calories', 0),
            nutrition.get('protein', 0),
            nutrition.get('carbs', 0),
            nutrition.get('fat', 0),
            nutrition.get('fiber', 0),
            nutrition.get('iron', 0),
            nutrition.get('calcium', 0),
            nutrition.get('vitamin_a', 0),
            nutrition.get('vitamin_c', 0),
            nutrition.get('sodium', 0),
            nutrition.get('data_source', 'USDA'),
            1 if nutrition.get('is_verified', False) else 0
        ))
        
        conn.commit()
        conn.close()
        print(f"💾 Cached USDA data for: {food_name}")
    
    def update_ingredient_with_usda_data(self, ingredient_name: str) -> bool:
        """
        Update an ingredient in the database with USDA nutrition data
        
        Returns:
            True if updated successfully, False otherwise
        """
        nutrition = self.get_nutrition_data(ingredient_name)
        
        if not nutrition:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE ingredients SET
                calories_per_100g = ?,
                protein_per_100g = ?,
                carbs_per_100g = ?,
                fat_per_100g = ?,
                fiber_per_100g = ?,
                iron_per_100g = ?,
                calcium_per_100g = ?
            WHERE LOWER(name) = LOWER(?)
        """, (
            nutrition['calories'],
            nutrition['protein'],
            nutrition['carbs'],
            nutrition['fat'],
            nutrition['fiber'],
            nutrition['iron'],
            nutrition['calcium'],
            ingredient_name
        ))
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if updated:
            print(f"✅ Updated {ingredient_name} with USDA data")
        
        return updated
    
    def bulk_update_ingredients(self, food_mapping: Dict[str, str] = None):
        """
        Bulk update all ingredients with USDA data
        
        Args:
            food_mapping: Optional dict mapping ingredient names to USDA search terms
                         e.g., {"Rice": "rice white cooked", "Moong Dal": "mung beans"}
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all ingredients
        cursor.execute("SELECT name FROM ingredients")
        ingredients = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        updated_count = 0
        failed_count = 0
        
        print(f"\n🔄 Starting bulk USDA data update for {len(ingredients)} ingredients...")
        
        for ingredient in ingredients:
            # Use mapped name if available
            search_term = food_mapping.get(ingredient, ingredient) if food_mapping else ingredient
            
            try:
                if self.update_ingredient_with_usda_data(search_term):
                    updated_count += 1
                else:
                    failed_count += 1
                    print(f"⚠️ Could not find USDA data for: {ingredient}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Error updating {ingredient}: {e}")
        
        print(f"\n📊 Bulk Update Complete:")
        print(f"   ✅ Successfully updated: {updated_count}")
        print(f"   ⚠️ Failed to update: {failed_count}")
        
        return updated_count, failed_count
    
    def get_cache_stats(self) -> Dict:
        """Get statistics about the nutrition cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM usda_nutrition_cache")
        total_cached = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM usda_nutrition_cache 
            WHERE datetime(last_updated) > datetime('now', '-7 days')
        """)
        recent_cached = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usda_nutrition_cache WHERE is_verified = 1")
        verified_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_items': total_cached,
            'recent_updates': recent_cached,
            'verified_items': verified_count
        }


# Indian food mapping for better USDA matches
INDIAN_FOOD_USDA_MAPPING = {
    # Grains
    "Rice": "rice white cooked",
    "Wheat Flour (Atta)": "wheat flour whole grain",
    "Jowar (Sorghum)": "sorghum grain",
    "Ragi (Finger Millet)": "millet cooked",
    "Poha (Flattened Rice)": "rice white cooked",
    
    # Pulses
    "Moong Dal": "mung beans mature seeds cooked",
    "Toor Dal": "pigeon peas mature seeds cooked",
    "Chana Dal": "chickpeas bengal gram mature seeds cooked",
    "Masoor Dal": "lentils mature seeds cooked",
    "Rajma (Kidney Beans)": "kidney beans mature seeds cooked",
    "Chickpeas (Kabuli Chana)": "chickpeas garbanzo beans bengal gram mature seeds cooked",
    
    # Vegetables
    "Potato": "potatoes flesh and skin raw",
    "Onion": "onions raw",
    "Tomato": "tomatoes red ripe raw",
    "Carrot": "carrots raw",
    "Spinach (Palak)": "spinach raw",
    "Pumpkin": "pumpkin raw",
    "Cabbage": "cabbage raw",
    "Cauliflower": "cauliflower raw",
    "Green Beans": "beans snap green raw",
    "Brinjal (Eggplant)": "eggplant raw",
    
    # Dairy
    "Milk": "milk whole 3.25% milkfat",
    "Curd (Yogurt)": "yogurt plain whole milk",
    "Eggs": "egg whole raw fresh",
    "Paneer": "cheese paneer",
    
    # Fruits
    "Banana": "bananas raw",
    "Apple": "apples raw with skin",
    "Papaya": "papayas raw",
    "Mango": "mangos raw",
    "Orange": "oranges raw",
    "Guava": "guavas common raw",
    "Pomegranate": "pomegranates raw",
    "Watermelon": "watermelon raw",
    "Grapes": "grapes raw",
    
    # Nuts
    "Almonds": "nuts almonds",
    "Cashews": "nuts cashew nuts raw",
    "Peanuts": "peanuts all types raw",
    "Walnuts": "nuts walnuts english",
    
    # Others
    "Cooking Oil": "oil vegetable",
    "Ghee": "butter ghee",
    "Jaggery (Gur)": "sugars brown",
    "Honey": "honey"
}


# Helper function
def get_nutrition_manager():
    """Get singleton instance of NutritionDataManager"""
    if not hasattr(get_nutrition_manager, '_instance'):
        get_nutrition_manager._instance = NutritionDataManager()
    return get_nutrition_manager._instance


# Command-line tool for updating nutrition data
if __name__ == "__main__":
    print("🚀 USDA Nutrition Data Update Tool\n")
    
    manager = get_nutrition_manager()
    
    # Show cache stats
    stats = manager.get_cache_stats()
    print(f"📊 Current Cache Stats:")
    print(f"   Total cached items: {stats['total_items']}")
    print(f"   Recent updates (7 days): {stats['recent_updates']}")
    print(f"   Verified items: {stats['verified_items']}\n")
    
    # Ask user what to do
    print("Options:")
    print("1. Update all ingredients with USDA data")
    print("2. Update specific ingredient")
    print("3. Show cache stats")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        print("\n⚠️ This will update ALL ingredients. Continue? (y/n)")
        confirm = input().strip().lower()
        if confirm == 'y':
            manager.bulk_update_ingredients(INDIAN_FOOD_USDA_MAPPING)
    elif choice == "2":
        ingredient = input("Enter ingredient name: ").strip()
        manager.update_ingredient_with_usda_data(ingredient)
    elif choice == "3":
        stats = manager.get_cache_stats()
        print(f"\n📊 Cache Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
