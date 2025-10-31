"""
Utility functions for the Nutrition Advisor app
Includes PDF export, translation, and helper functions
"""

from fpdf import FPDF
import io
from datetime import datetime

# Try to import googletrans, but make it optional
try:
    from googletrans import Translator
    TRANSLATION_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    TRANSLATION_AVAILABLE = False
    print("⚠️ Translation module not available. Language switching disabled.")

# Food category emojis
FOOD_EMOJIS = {
    'Grains': '🌾',
    'Pulses': '🫘',
    'Vegetables': '🥬',
    'Dairy': '🥛',
    'Protein': '🥚',
    'Fats': '🧈',
    'Sweetener': '🍯',
    'Fruits': '🍎',
    'Dry Fruits': '🌰',
    'Leafy Vegetables': '🥬',
    'Nutrition Rich': '💪',
}

def get_food_emoji(category):
    """Get emoji for food category"""
    return FOOD_EMOJIS.get(category, '🍽️')

class NutritionPDF(FPDF):
    """Custom PDF class for meal plans"""
    
    def header(self):
        """PDF header"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'AI Nutrition Advisor - Weekly Meal Plan', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'Generated on: {datetime.now().strftime("%d-%m-%Y %H:%M")}', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        """Add chapter title"""
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(255, 107, 107)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(2)
    
    def add_key_value(self, key, value):
        """Add key-value pair"""
        self.set_font('Arial', 'B', 10)
        self.cell(60, 6, key + ':', 0, 0)
        self.set_font('Arial', '', 10)
        self.cell(0, 6, str(value), 0, 1)

def export_to_pdf(meal_plan, num_children, budget):
    """Export meal plan to PDF"""
    
    pdf = NutritionPDF()
    pdf.add_page()
    
    # Summary section
    pdf.chapter_title('Summary')
    pdf.add_key_value('Number of Children', num_children)
    pdf.add_key_value('Weekly Budget', f'Rs. {budget:.2f}')
    pdf.add_key_value('Total Cost', f'Rs. {meal_plan["total_cost"]:.2f}')
    pdf.add_key_value('Budget Utilized', f'{(meal_plan["total_cost"]/budget*100):.1f}%')
    pdf.add_key_value('Nutrition Score', f'{meal_plan["nutrition_score"]}/100')
    pdf.ln(5)
    
    # Weekly nutrition
    pdf.chapter_title('Weekly Nutrition Summary (Per Child)')
    nutrition = meal_plan['weekly_nutrition']
    pdf.add_key_value('Total Calories', f'{nutrition["calories"]:.0f} kcal')
    pdf.add_key_value('Total Protein', f'{nutrition["protein"]:.1f} g')
    pdf.add_key_value('Total Carbohydrates', f'{nutrition["carbs"]:.1f} g')
    pdf.add_key_value('Total Fat', f'{nutrition["fat"]:.1f} g')
    pdf.add_key_value('Total Fiber', f'{nutrition["fiber"]:.1f} g')
    pdf.add_key_value('Total Iron', f'{nutrition["iron"]:.1f} mg')
    pdf.add_key_value('Total Calcium', f'{nutrition["calcium"]:.1f} mg')
    pdf.ln(5)
    
    # Daily requirements
    pdf.chapter_title('Daily Nutritional Requirements (Per Child)')
    requirements = meal_plan['daily_requirements']
    pdf.add_key_value('Calories', f'{requirements["calories"]:.0f} kcal')
    pdf.add_key_value('Protein', f'{requirements["protein"]:.1f} g')
    pdf.add_key_value('Carbohydrates', f'{requirements["carbs"]:.1f} g')
    pdf.add_key_value('Fat', f'{requirements["fat"]:.1f} g')
    pdf.add_key_value('Fiber', f'{requirements["fiber"]:.1f} g')
    pdf.add_key_value('Iron', f'{requirements["iron"]:.1f} mg')
    pdf.add_key_value('Calcium', f'{requirements["calcium"]:.1f} mg')
    pdf.ln(5)
    
    # Weekly meal plan
    pdf.add_page()
    pdf.chapter_title('7-Day Meal Plan')
    
    for day, day_plan in meal_plan['weekly_plan'].items():
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(78, 205, 196)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 8, day, 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
        for meal_type, meal_data in day_plan['meals'].items():
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f'{meal_type.capitalize()}:', 0, 1)
            
            pdf.set_font('Arial', '', 9)
            for item in meal_data['items']:
                ingredient_text = f"  - {item['ingredient']}: {item['quantity_per_child_g']:.0f}g per child"
                pdf.cell(0, 5, ingredient_text, 0, 1)
            
            pdf.set_font('Arial', 'I', 8)
            pdf.cell(0, 5, f"     Calories: {meal_data['nutrition']['calories']:.0f} kcal | "
                          f"Protein: {meal_data['nutrition']['protein']:.1f}g | "
                          f"Cost: Rs. {meal_data['cost']:.2f}", 0, 1)
            pdf.ln(2)
        
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(0, 5, f'Daily Total Cost: Rs. {day_plan["total_cost"]:.2f}', 0, 1)
        pdf.ln(5)
    
    # Shopping list
    pdf.add_page()
    pdf.chapter_title('Weekly Shopping List')
    
    # Aggregate ingredients
    shopping_list = {}
    for day, day_plan in meal_plan['weekly_plan'].items():
        for meal_type, meal_data in day_plan['meals'].items():
            for item in meal_data['items']:
                ingredient = item['ingredient']
                qty = item['total_quantity_g']
                cost = item['cost']
                
                if ingredient in shopping_list:
                    shopping_list[ingredient]['quantity'] += qty
                    shopping_list[ingredient]['cost'] += cost
                else:
                    shopping_list[ingredient] = {
                        'quantity': qty,
                        'cost': cost,
                        'category': item['category']
                    }
    
    # Group by category
    categories = {}
    for ingredient, data in shopping_list.items():
        category = data['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'name': ingredient,
            'quantity': data['quantity'],
            'cost': data['cost']
        })
    
    for category, items in sorted(categories.items()):
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 6, category, 0, 1)
        
        pdf.set_font('Arial', '', 9)
        for item in sorted(items, key=lambda x: x['name']):
            qty_kg = item['quantity'] / 1000
            if qty_kg >= 1:
                qty_str = f"{qty_kg:.2f} kg"
            else:
                qty_str = f"{item['quantity']:.0f} g"
            
            pdf.cell(0, 5, f"  - {item['name']}: {qty_str} (Rs. {item['cost']:.2f})", 0, 1)
        pdf.ln(2)
    
    # Generate PDF
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output

def translate_text(text, target_language='hi'):
    """
    Translate text to target language
    
    Args:
        text: Text to translate
        target_language: Target language code ('hi', 'te', 'ta', etc.)
    
    Returns:
        Translated text
    """
    if target_language == 'en':
        return text
    
    if not TRANSLATION_AVAILABLE:
        return text  # Return original text if translation not available
    
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def format_currency(amount, locale='en_IN'):
    """Format currency in Indian Rupees"""
    return f"₹{amount:,.2f}"

def calculate_per_meal_cost(total_cost, num_children, num_days=7, meals_per_day=4):
    """Calculate cost per meal"""
    total_meals = num_children * num_days * meals_per_day
    return total_cost / total_meals if total_meals > 0 else 0

def get_nutrition_color(percentage):
    """Get color based on nutrition achievement percentage"""
    if 90 <= percentage <= 110:
        return '#4CAF50'  # Green
    elif 70 <= percentage < 90 or 110 < percentage <= 130:
        return '#FFC107'  # Amber
    else:
        return '#F44336'  # Red

def get_nutrition_status(percentage):
    """Get status text based on nutrition achievement percentage"""
    if 90 <= percentage <= 110:
        return '✅ Optimal'
    elif 80 <= percentage < 90:
        return '⚠️ Slightly Low'
    elif 110 < percentage <= 120:
        return '⚠️ Slightly High'
    elif percentage < 80:
        return '❌ Low'
    else:
        return '❌ Too High'

def group_ingredients_by_meal_time(meal_plan):
    """Group ingredients by meal time across the week"""
    meal_groups = {
        'breakfast': {},
        'lunch': {},
        'snack': {},
        'dinner': {}
    }
    
    for day, day_plan in meal_plan['weekly_plan'].items():
        for meal_type, meal_data in day_plan['meals'].items():
            for item in meal_data['items']:
                ingredient = item['ingredient']
                if ingredient not in meal_groups[meal_type]:
                    meal_groups[meal_type][ingredient] = {
                        'count': 0,
                        'total_quantity': 0,
                        'category': item['category']
                    }
                meal_groups[meal_type][ingredient]['count'] += 1
                meal_groups[meal_type][ingredient]['total_quantity'] += item['total_quantity_g']
    
    return meal_groups

def suggest_alternatives(ingredient_name, ingredients_df):
    """Suggest alternative ingredients from same category"""
    try:
        ingredient = ingredients_df[ingredients_df['name'] == ingredient_name].iloc[0]
        category = ingredient['category']
        
        # Find similar ingredients in same category
        alternatives = ingredients_df[
            (ingredients_df['category'] == category) & 
            (ingredients_df['name'] != ingredient_name)
        ].head(3)
        
        return alternatives['name'].tolist()
    except:
        return []

def calculate_ghg_emissions(meal_plan, emission_factors=None):
    """
    Calculate estimated greenhouse gas emissions for meal plan
    (Optional feature for environmental awareness)
    """
    if emission_factors is None:
        # Default emission factors (kg CO2e per kg of food)
        emission_factors = {
            'Grains': 0.5,
            'Pulses': 0.9,
            'Vegetables': 0.4,
            'Dairy': 2.5,
            'Protein': 4.5,  # Eggs
            'Fats': 3.0,
            'Sweetener': 0.6,
            'Fruits': 0.5
        }
    
    total_emissions = 0
    
    for day, day_plan in meal_plan['weekly_plan'].items():
        for meal_type, meal_data in day_plan['meals'].items():
            for item in meal_data['items']:
                category = item['category']
                quantity_kg = item['total_quantity_g'] / 1000
                emission_factor = emission_factors.get(category, 1.0)
                total_emissions += quantity_kg * emission_factor
    
    return round(total_emissions, 2)

def validate_meal_plan(meal_plan, min_score=60):
    """
    Validate meal plan meets minimum criteria
    
    Returns:
        tuple: (is_valid, list of issues)
    """
    issues = []
    
    # Check nutrition score
    if meal_plan['nutrition_score'] < min_score:
        issues.append(f"Nutrition score ({meal_plan['nutrition_score']}) is below minimum ({min_score})")
    
    # Check if all days have meals
    if len(meal_plan['weekly_plan']) != 7:
        issues.append(f"Meal plan has only {len(meal_plan['weekly_plan'])} days instead of 7")
    
    # Check daily calorie minimum
    daily_calories = meal_plan['weekly_nutrition']['calories'] / 7
    if daily_calories < 800:  # Minimum threshold
        issues.append(f"Average daily calories ({daily_calories:.0f}) is too low")
    
    # Check protein minimum
    daily_protein = meal_plan['weekly_nutrition']['protein'] / 7
    if daily_protein < 15:  # Minimum threshold
        issues.append(f"Average daily protein ({daily_protein:.1f}g) is too low")
    
    is_valid = len(issues) == 0
    return is_valid, issues

def get_meal_variety_score(meal_plan):
    """
    Calculate variety score based on ingredient diversity
    Higher score = more variety
    """
    all_ingredients = set()
    
    for day, day_plan in meal_plan['weekly_plan'].items():
        for meal_type, meal_data in day_plan['meals'].items():
            for item in meal_data['items']:
                all_ingredients.add(item['ingredient'])
    
    # Score based on unique ingredients (max 100)
    variety_score = min(100, len(all_ingredients) * 5)
    return variety_score

def generate_recipe_suggestions(ingredients_list):
    """
    Generate simple recipe suggestions based on ingredients
    """
    recipes = {
        ('Rice', 'Dal'): 'Dal Rice - Cook dal with turmeric and serve with steamed rice',
        ('Wheat Flour', 'Vegetables'): 'Vegetable Roti - Make rotis and serve with vegetable sabzi',
        ('Poha', 'Onion', 'Potato'): 'Poha Upma - Sauté onions and potatoes, add poha and spices',
        ('Eggs', 'Onion', 'Tomato'): 'Egg Bhurji - Scrambled eggs with onions and tomatoes',
        ('Milk', 'Jaggery'): 'Sweet Milk - Warm milk with jaggery for energy',
        ('Rice', 'Curd'): 'Curd Rice - Mix cooked rice with fresh curd',
    }
    
    suggestions = []
    ingredients_set = set(ingredients_list)
    
    for recipe_ingredients, recipe in recipes.items():
        if set(recipe_ingredients).issubset(ingredients_set):
            suggestions.append(recipe)
    
    return suggestions[:5]  # Return top 5 suggestions
