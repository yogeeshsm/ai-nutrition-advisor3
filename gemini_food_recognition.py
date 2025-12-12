"""
Food Image Recognition using Gemini Vision API
No training required - works immediately!
Analyzes food images and provides detailed nutritional information
"""

import base64
import json
from datetime import datetime
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[WARNING] google-generativeai not installed")

# Indian food nutrition database (comprehensive)
INDIAN_FOOD_DATABASE = {
    'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28.2, 'fat': 0.3, 'fiber': 0.4, 'iron': 0.2, 'calcium': 10},
    'ragi': {'calories': 336, 'protein': 7.3, 'carbs': 72.0, 'fat': 1.3, 'fiber': 3.6, 'iron': 3.9, 'calcium': 344},
    'dal': {'calories': 116, 'protein': 9.0, 'carbs': 20.1, 'fat': 0.4, 'fiber': 7.9, 'iron': 3.3, 'calcium': 27},
    'egg': {'calories': 155, 'protein': 13.0, 'carbs': 1.1, 'fat': 11.0, 'fiber': 0, 'iron': 1.8, 'calcium': 50},
    'banana': {'calories': 89, 'protein': 1.1, 'carbs': 22.8, 'fat': 0.3, 'fiber': 2.6, 'iron': 0.3, 'calcium': 5},
    'chapati': {'calories': 297, 'protein': 11.0, 'carbs': 45.0, 'fat': 8.0, 'fiber': 4.9, 'iron': 4.0, 'calcium': 48},
    'chicken': {'calories': 165, 'protein': 31.0, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'iron': 0.9, 'calcium': 11},
    'fish': {'calories': 206, 'protein': 22.0, 'carbs': 0, 'fat': 13.0, 'fiber': 0, 'iron': 1.0, 'calcium': 35},
    'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5.0, 'fat': 1.0, 'fiber': 0, 'iron': 0, 'calcium': 125},
    'curd': {'calories': 98, 'protein': 11.0, 'carbs': 3.0, 'fat': 4.0, 'fiber': 0, 'iron': 0.1, 'calcium': 121},
    'paneer': {'calories': 265, 'protein': 18.3, 'carbs': 1.2, 'fat': 20.8, 'fiber': 0, 'iron': 0.2, 'calcium': 208},
    'vegetables': {'calories': 65, 'protein': 3.0, 'carbs': 13.0, 'fat': 0.5, 'fiber': 3.0, 'iron': 1.5, 'calcium': 40},
    'sambar': {'calories': 88, 'protein': 3.5, 'carbs': 12.0, 'fat': 3.0, 'fiber': 2.5, 'iron': 1.2, 'calcium': 35},
    'idli': {'calories': 132, 'protein': 3.5, 'carbs': 25.0, 'fat': 2.0, 'fiber': 1.5, 'iron': 0.5, 'calcium': 20},
    'dosa': {'calories': 168, 'protein': 4.0, 'carbs': 28.0, 'fat': 4.0, 'fiber': 2.0, 'iron': 0.8, 'calcium': 25},
    'upma': {'calories': 175, 'protein': 4.5, 'carbs': 30.0, 'fat': 4.5, 'fiber': 2.0, 'iron': 1.0, 'calcium': 30},
}


class GeminiFoodRecognizer:
    """Food recognition using Gemini Vision API - no training needed!"""
    
    def __init__(self):
        """Initialize Gemini Vision API"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not GEMINI_AVAILABLE:
            print("[ERROR] Gemini API not available - install google-generativeai")
            self.model = None
            return
        
        if not self.api_key:
            print("[WARNING] GEMINI_API_KEY not found in environment")
            self.model = None
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("[OK] Gemini Vision API initialized for food recognition")
        except Exception as e:
            print(f"[ERROR] Failed to initialize Gemini: {e}")
            self.model = None
    
    def analyze_image(self, image_data):
        """
        Analyze food image using Gemini Vision
        
        Args:
            image_data: bytes or PIL Image
        
        Returns:
            dict with food name, portion size, and confidence
        """
        if not self.model:
            return {
                'success': False,
                'error': 'Gemini Vision API not available',
                'message': 'Please set GEMINI_API_KEY in .env file'
            }
        
        try:
            # Convert bytes to PIL Image if needed
            if isinstance(image_data, bytes):
                img = Image.open(io.BytesIO(image_data))
            else:
                img = image_data
            
            # Prepare image part with mime type to avoid "image media type is required" error
            fmt = img.format if hasattr(img, 'format') and img.format else 'JPEG'
            mime_type = f"image/{fmt.lower()}"
            if fmt.upper() == 'JPEG':
                mime_type = 'image/jpeg'
            elif fmt.upper() == 'JPG':
                mime_type = 'image/jpeg'
                
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=fmt)
            image_bytes = img_byte_arr.getvalue()
            
            image_part = {
                "mime_type": mime_type,
                "data": image_bytes
            }
            
            # Prepare prompt for food recognition
            prompt = """Analyze this food image and provide ONLY a JSON response with this exact structure:
{
    "food_items": [
        {
            "name": "food_name_in_english",
            "local_name": "local_name_if_applicable",
            "portion_size": "small/medium/large",
            "estimated_weight_grams": number,
            "confidence": number_between_0_and_1
        }
    ],
    "meal_type": "breakfast/lunch/dinner/snack",
    "cuisine": "indian/western/chinese/etc"
}

Guidelines:
- Identify ALL visible food items
- Use common names (rice, dal, chicken, etc.)
- Estimate portion size accurately
- Weight in grams (small: 50-100g, medium: 100-200g, large: 200-300g)
- Confidence: 0.0 to 1.0

Return ONLY the JSON, no additional text."""

            # Send to Gemini
            response = self.model.generate_content([prompt, image_part])
            
            # Parse response
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            # Parse JSON
            result = json.loads(result_text)
            
            return {
                'success': True,
                'result': result,
                'raw_response': response.text
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': 'Failed to parse Gemini response',
                'details': str(e),
                'raw_response': response.text if 'response' in locals() else None
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'Failed to analyze image',
                'details': str(e)
            }
    
    def calculate_nutrition(self, food_name, weight_grams):
        """
        Calculate nutrition for given food and weight
        
        Args:
            food_name: Name of food item
            weight_grams: Weight in grams
        
        Returns:
            dict with nutritional values
        """
        # Normalize food name
        food_key = food_name.lower().replace(' ', '_')
        
        # Find matching nutrition data
        nutrition_per_100g = None
        for key, data in INDIAN_FOOD_DATABASE.items():
            if key in food_key or food_key in key:
                nutrition_per_100g = data
                break
        
        # Use generic values if not found
        if not nutrition_per_100g:
            nutrition_per_100g = INDIAN_FOOD_DATABASE['vegetables']
        
        # Calculate for given weight
        multiplier = weight_grams / 100.0
        
        return {
            'calories': round(nutrition_per_100g['calories'] * multiplier, 1),
            'protein': round(nutrition_per_100g['protein'] * multiplier, 1),
            'carbs': round(nutrition_per_100g['carbs'] * multiplier, 1),
            'fat': round(nutrition_per_100g['fat'] * multiplier, 1),
            'fiber': round(nutrition_per_100g['fiber'] * multiplier, 1),
            'iron': round(nutrition_per_100g['iron'] * multiplier, 1),
            'calcium': round(nutrition_per_100g['calcium'] * multiplier, 1),
            'weight_grams': weight_grams
        }
    
    def assess_nutrition(self, total_nutrition):
        """
        Assess if meal meets nutritional requirements for children
        Based on WHO/ICMR guidelines for children aged 1-6 years
        """
        # Daily requirements (approximate for 3-year-old)
        daily_requirements = {
            'calories': 1200,
            'protein': 20,
            'iron': 10,
            'calcium': 600
        }
        
        # Calculate percentage of daily requirements
        percentages = {
            'calories': round((total_nutrition['calories'] / daily_requirements['calories']) * 100, 1),
            'protein': round((total_nutrition['protein'] / daily_requirements['protein']) * 100, 1),
            'iron': round((total_nutrition['iron'] / daily_requirements['iron']) * 100, 1),
            'calcium': round((total_nutrition['calcium'] / daily_requirements['calcium']) * 100, 1)
        }
        
        # Generate recommendations
        recommendations = []
        
        if percentages['calories'] < 20:
            recommendations.append({
                'type': 'warning',
                'message': 'Low calorie content for a meal',
                'suggestion': 'Add rice, roti, or other carbohydrates'
            })
        elif percentages['calories'] > 50:
            recommendations.append({
                'type': 'info',
                'message': 'High calorie content',
                'suggestion': 'Good for main meals'
            })
        
        if percentages['protein'] < 25:
            recommendations.append({
                'type': 'warning',
                'message': 'Add more protein',
                'suggestion': 'Include dal, egg, paneer, or chicken'
            })
        else:
            recommendations.append({
                'type': 'success',
                'message': 'Good protein content',
                'suggestion': 'Well balanced'
            })
        
        if percentages['iron'] < 15:
            recommendations.append({
                'type': 'warning',
                'message': 'Low iron content',
                'suggestion': 'Add ragi, green vegetables, or eggs'
            })
        
        if percentages['calcium'] < 15:
            recommendations.append({
                'type': 'warning',
                'message': 'Low calcium content',
                'suggestion': 'Include milk, curd, or cheese'
            })
        
        if not any(r['type'] == 'warning' for r in recommendations):
            recommendations.append({
                'type': 'success',
                'message': 'Well-balanced meal!',
                'suggestion': 'Keep up the good nutrition'
            })
        
        return {
            'daily_percentages': percentages,
            'recommendations': recommendations,
            'meets_requirements': not any(r['type'] == 'warning' for r in recommendations)
        }


def analyze_food_image(image_data):
    """
    Main function to analyze food image
    
    Args:
        image_data: Image bytes or PIL Image
    
    Returns:
        Complete analysis with food items, nutrition, and recommendations
    """
    try:
        recognizer = GeminiFoodRecognizer()
        
        # Analyze image with Gemini
        gemini_result = recognizer.analyze_image(image_data)
        
        if not gemini_result['success']:
            return gemini_result
        
        # Extract food items
        food_items = gemini_result['result'].get('food_items', [])
        
        if not food_items:
            return {
                'success': False,
                'error': 'No food items detected in image',
                'message': 'Please upload a clear image of food'
            }
        
        # Calculate nutrition for each item
        items_with_nutrition = []
        total_nutrition = {
            'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
            'fiber': 0, 'iron': 0, 'calcium': 0, 'weight_grams': 0
        }
        
        for item in food_items:
            nutrition = recognizer.calculate_nutrition(
                item['name'],
                item['estimated_weight_grams']
            )
            
            items_with_nutrition.append({
                'name': item['name'],
                'local_name': item.get('local_name', ''),
                'portion_size': item['portion_size'],
                'weight_grams': item['estimated_weight_grams'],
                'confidence': round(item['confidence'] * 100, 1),
                'nutrition': nutrition
            })
            
            # Add to total
            for key in total_nutrition:
                total_nutrition[key] += nutrition[key]
        
        # Assess overall nutrition
        assessment = recognizer.assess_nutrition(total_nutrition)
        
        # Build final result
        return {
            'success': True,
            'food_items': items_with_nutrition,
            'total_nutrition': total_nutrition,
            'meal_type': gemini_result['result'].get('meal_type', 'meal'),
            'cuisine': gemini_result['result'].get('cuisine', 'mixed'),
            'nutritional_assessment': assessment,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': 'Failed to analyze food image',
            'details': str(e),
            'timestamp': datetime.now().isoformat()
        }


# Test function
if __name__ == '__main__':
    print("\n" + "="*80)
    print("   🍲 GEMINI FOOD RECOGNITION SYSTEM")
    print("="*80)
    print("\n✨ Features:")
    print("   ✓ No training required")
    print("   ✓ Works with any food image")
    print("   ✓ Identifies multiple food items")
    print("   ✓ Estimates portion sizes")
    print("   ✓ Calculates nutrition")
    print("   ✓ Provides recommendations")
    print("\n📊 Supported Foods:", len(INDIAN_FOOD_DATABASE))
    print("🤖 Powered by: Gemini 1.5 Flash Vision")
    print("="*80 + "\n")
    
    recognizer = GeminiFoodRecognizer()
    if recognizer.model:
        print("✅ System ready! Upload images via web interface.")
    else:
        print("❌ Gemini API not configured. Add GEMINI_API_KEY to .env")
