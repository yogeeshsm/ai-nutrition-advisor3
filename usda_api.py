"""
USDA FoodData Central API Integration
Provides accurate nutrition information for foods
"""

import requests
import json
from typing import Dict, List, Optional

class USDAFoodAPI:
    """Wrapper for USDA FoodData Central API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
    
    def search_foods(self, query: str, page_size: int = 10) -> List[Dict]:
        """
        Search for foods by name
        
        Args:
            query: Food name to search
            page_size: Number of results to return
            
        Returns:
            List of food items with basic info
        """
        url = f"{self.base_url}/foods/search"
        params = {
            'api_key': self.api_key,
            'query': query,
            'pageSize': page_size,
            'dataType': ['Foundation', 'SR Legacy']  # Most reliable data
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for food in data.get('foods', []):
                results.append({
                    'fdc_id': food.get('fdcId'),
                    'name': food.get('description'),
                    'brand': food.get('brandOwner', ''),
                    'category': food.get('foodCategory', '')
                })
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching foods: {e}")
            return []
    
    def get_food_details(self, fdc_id: int) -> Optional[Dict]:
        """
        Get detailed nutrition information for a specific food
        
        Args:
            fdc_id: USDA Food Data Central ID
            
        Returns:
            Dictionary with detailed nutrition data
        """
        url = f"{self.base_url}/food/{fdc_id}"
        params = {'api_key': self.api_key}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract nutrition information
            nutrients = {}
            for nutrient in data.get('foodNutrients', []):
                name = nutrient.get('nutrient', {}).get('name')
                value = nutrient.get('amount', 0)
                unit = nutrient.get('nutrient', {}).get('unitName', '')
                
                nutrients[name] = {
                    'value': value,
                    'unit': unit
                }
            
            return {
                'fdc_id': data.get('fdcId'),
                'name': data.get('description'),
                'category': data.get('foodCategory', ''),
                'nutrients': nutrients,
                'portions': self._extract_portions(data)
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting food details: {e}")
            return None
    
    def _extract_portions(self, data: Dict) -> List[Dict]:
        """Extract portion/serving size information"""
        portions = []
        for portion in data.get('foodPortions', []):
            portions.append({
                'description': portion.get('portionDescription', ''),
                'gram_weight': portion.get('gramWeight', 100)
            })
        return portions
    
    def get_nutrition_summary(self, fdc_id: int) -> Optional[Dict]:
        """
        Get simplified nutrition summary (macros + key vitamins/minerals)
        
        Returns:
            Dictionary with key nutrition values per 100g
        """
        details = self.get_food_details(fdc_id)
        if not details:
            return None
        
        nutrients = details.get('nutrients', {})
        
        # Extract key nutrients
        summary = {
            'name': details.get('name'),
            'protein': self._get_nutrient_value(nutrients, 'Protein'),
            'carbs': self._get_nutrient_value(nutrients, 'Carbohydrate, by difference'),
            'fat': self._get_nutrient_value(nutrients, 'Total lipid (fat)'),
            'calories': self._get_nutrient_value(nutrients, 'Energy'),
            'fiber': self._get_nutrient_value(nutrients, 'Fiber, total dietary'),
            'iron': self._get_nutrient_value(nutrients, 'Iron, Fe'),
            'calcium': self._get_nutrient_value(nutrients, 'Calcium, Ca'),
            'vitamin_a': self._get_nutrient_value(nutrients, 'Vitamin A, RAE'),
            'vitamin_c': self._get_nutrient_value(nutrients, 'Vitamin C, total ascorbic acid'),
            'sodium': self._get_nutrient_value(nutrients, 'Sodium, Na')
        }
        
        return summary
    
    def _get_nutrient_value(self, nutrients: Dict, nutrient_name: str) -> float:
        """Helper to extract nutrient value"""
        for name, data in nutrients.items():
            if nutrient_name.lower() in name.lower():
                return data.get('value', 0)
        return 0.0
    
    def compare_foods(self, food_names: List[str]) -> Dict:
        """
        Compare nutrition across multiple foods
        
        Args:
            food_names: List of food names to compare
            
        Returns:
            Comparison data for all foods
        """
        results = {}
        
        for food_name in food_names:
            # Search for the food
            search_results = self.search_foods(food_name, page_size=1)
            if search_results:
                fdc_id = search_results[0]['fdc_id']
                summary = self.get_nutrition_summary(fdc_id)
                if summary:
                    results[food_name] = summary
        
        return results
    
    def suggest_alternatives(self, food_name: str, criteria: str = 'protein') -> List[Dict]:
        """
        Suggest nutritionally similar alternatives
        
        Args:
            food_name: Original food name
            criteria: Nutrient to match (protein, fiber, calcium, etc.)
            
        Returns:
            List of alternative foods
        """
        # Search for similar foods
        search_results = self.search_foods(food_name, page_size=5)
        
        alternatives = []
        for result in search_results[1:]:  # Skip first (original)
            fdc_id = result['fdc_id']
            summary = self.get_nutrition_summary(fdc_id)
            if summary:
                alternatives.append({
                    'name': summary['name'],
                    'nutrition': summary
                })
        
        return alternatives


# Helper function to initialize API
def get_usda_api(api_key: Optional[str] = None) -> Optional[USDAFoodAPI]:
    """
    Initialize USDA API with key from environment or parameter
    
    Usage:
        api = get_usda_api()
        if api:
            results = api.search_foods("rice")
    """
    import os
    
    if api_key is None:
        api_key = os.environ.get('USDA_API_KEY')
    
    if not api_key:
        print("⚠️ USDA API key not found. Set USDA_API_KEY environment variable.")
        return None
    
    return USDAFoodAPI(api_key)


# Example usage
if __name__ == "__main__":
    # Test the API
    api_key = "DEMO_KEY"  # Replace with your actual key
    api = USDAFoodAPI(api_key)
    
    # Search for foods
    print("Searching for 'banana'...")
    results = api.search_foods("banana")
    for result in results[:3]:
        print(f"  - {result['name']} (ID: {result['fdc_id']})")
    
    # Get detailed nutrition
    if results:
        print(f"\nDetailed nutrition for {results[0]['name']}:")
        details = api.get_nutrition_summary(results[0]['fdc_id'])
        if details:
            print(f"  Protein: {details['protein']}g")
            print(f"  Carbs: {details['carbs']}g")
            print(f"  Calories: {details['calories']} kcal")
