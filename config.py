"""
Configuration file for AI Nutrition Advisor
Modify these settings to customize the application
"""

# Application Settings
APP_CONFIG = {
    'app_name': 'AI Nutrition Advisor',
    'version': '1.0.0',
    'page_icon': '🍽️',
    'layout': 'wide',
}

# Database Settings
DATABASE_CONFIG = {
    'database_path': 'nutrition_advisor.db',
    'backup_enabled': True,
    'backup_frequency': 'weekly'
}

# Optimization Settings
OPTIMIZATION_CONFIG = {
    'max_quantity_per_ingredient': 200,  # grams per meal
    'min_calorie_percentage': 0.80,      # 80% of target
    'max_calorie_percentage': 1.30,      # 130% of target
    'protein_weight': 2.0,               # Weight in optimization
    'fiber_weight': 1.0,
    'iron_weight': 0.5,
    'calcium_weight': 0.01,
    'solver_time_limit': 30,             # seconds
}

# Meal Distribution (percentage of daily intake)
MEAL_DISTRIBUTION = {
    'breakfast': 0.25,
    'lunch': 0.40,
    'snack': 0.10,
    'dinner': 0.25
}

# Nutritional Requirements (ICMR Guidelines)
NUTRITIONAL_REQUIREMENTS = {
    "1-3 years": {
        'calories': 1060,
        'protein': 16.7,
        'carbs': 130,
        'fat': 27,
        'fiber': 19,
        'iron': 9,
        'calcium': 600
    },
    "3-6 years": {
        'calories': 1350,
        'protein': 20.1,
        'carbs': 130,
        'fat': 25,
        'fiber': 25,
        'iron': 10,
        'calcium': 600
    },
    "6-10 years": {
        'calories': 1690,
        'protein': 29.5,
        'carbs': 130,
        'fat': 30,
        'fiber': 31,
        'iron': 13,
        'calcium': 800
    }
}

# Budget Recommendations (per child per day in INR)
BUDGET_RECOMMENDATIONS = {
    'minimum': 25,
    'recommended': 35,
    'optimal': 50,
    'comfortable': 75
}

# UI Settings
UI_CONFIG = {
    'primary_color': '#FF6B6B',
    'secondary_color': '#4ECDC4',
    'accent_color': '#FFE66D',
    'show_emojis': True,
    'default_num_children': 20,
    'default_age_group': '3-6 years',
    'default_budget': 2000,
}

# Language Settings
LANGUAGE_CONFIG = {
    'default_language': 'en',
    'available_languages': {
        'en': 'English',
        'hi': 'Hindi (हिंदी)',
        'te': 'Telugu (తెలుగు)',
        'ta': 'Tamil (தமிழ்)'
    },
    'translation_enabled': True
}

# Export Settings
EXPORT_CONFIG = {
    'pdf_font': 'Arial',
    'pdf_font_size': 10,
    'include_shopping_list': True,
    'include_nutrition_breakdown': True,
    'include_recipe_suggestions': False,
    'csv_separator': ',',
    'date_format': '%Y-%m-%d'
}

# Analytics Settings
ANALYTICS_CONFIG = {
    'track_meal_plans': True,
    'show_recent_plans_limit': 10,
    'show_top_combinations_limit': 10,
    'enable_feedback': True
}

# Ingredient Categories and Emojis
FOOD_CATEGORIES = {
    'Grains': {
        'emoji': '🌾',
        'priority': 1,
        'description': 'Rice, wheat, millets, etc.'
    },
    'Pulses': {
        'emoji': '🫘',
        'priority': 2,
        'description': 'Dals, legumes, beans'
    },
    'Vegetables': {
        'emoji': '🥬',
        'priority': 3,
        'description': 'Fresh vegetables'
    },
    'Dairy': {
        'emoji': '🥛',
        'priority': 4,
        'description': 'Milk, curd, paneer'
    },
    'Protein': {
        'emoji': '🥚',
        'priority': 5,
        'description': 'Eggs, meat alternatives'
    },
    'Fats': {
        'emoji': '🧈',
        'priority': 6,
        'description': 'Oils, ghee'
    },
    'Fruits': {
        'emoji': '🍎',
        'priority': 7,
        'description': 'Seasonal fruits'
    },
    'Sweetener': {
        'emoji': '🍯',
        'priority': 8,
        'description': 'Jaggery, sugar'
    }
}

# Meal Preferences (which categories for which meal)
MEAL_PREFERENCES = {
    'breakfast': ['Grains', 'Dairy', 'Fruits', 'Sweetener'],
    'lunch': ['Grains', 'Pulses', 'Vegetables', 'Dairy', 'Fats'],
    'snack': ['Fruits', 'Dairy', 'Grains', 'Sweetener'],
    'dinner': ['Grains', 'Pulses', 'Vegetables', 'Fats']
}

# Validation Settings
VALIDATION_CONFIG = {
    'min_nutrition_score': 60,
    'min_daily_calories': 800,
    'min_daily_protein': 15,
    'max_budget_overrun_percentage': 10,
    'min_ingredients': 5,
    'warn_low_variety_threshold': 10  # unique ingredients
}

# Performance Settings
PERFORMANCE_CONFIG = {
    'cache_enabled': True,
    'cache_ttl': 3600,  # seconds
    'max_ingredients_for_fast_optimization': 15,
    'parallel_processing': False
}

# Feature Flags
FEATURE_FLAGS = {
    'enable_voice_input': False,
    'enable_recipe_suggestions': True,
    'enable_shopping_list': True,
    'enable_cost_prediction': True,
    'enable_seasonal_recommendations': False,
    'enable_allergen_warnings': False,
    'enable_ghg_emissions': False,
    'enable_chatbot': False
}

# Alerts and Notifications
ALERT_CONFIG = {
    'show_low_score_warning': True,
    'low_score_threshold': 70,
    'show_budget_warning': True,
    'show_variety_warning': True,
    'show_success_balloons': True
}

# Default Recommended Ingredients
DEFAULT_INGREDIENTS = [
    'Rice',
    'Wheat Flour (Atta)',
    'Moong Dal',
    'Toor Dal',
    'Potato',
    'Onion',
    'Tomato',
    'Spinach (Palak)',
    'Milk',
    'Eggs',
    'Cooking Oil',
    'Jaggery (Gur)'
]

# Basic Ingredients (minimum required)
BASIC_INGREDIENTS = [
    'Rice',
    'Wheat Flour (Atta)',
    'Moong Dal',
    'Toor Dal',
    'Potato',
    'Onion',
    'Cooking Oil'
]

# Help Text
HELP_TEXT = {
    'num_children': 'Enter the total number of children to plan meals for',
    'age_group': 'Select age group for appropriate nutritional requirements',
    'budget': 'Total budget available for one week of meals (all children)',
    'ingredients': 'Select ingredients currently available in your pantry',
    'nutrition_score': 'Score from 0-100 based on meeting nutritional requirements',
    'generate_button': 'Click to generate optimized meal plan using AI'
}

# Error Messages
ERROR_MESSAGES = {
    'no_ingredients': '⚠️ Please select at least {min} ingredients to generate meal plan',
    'low_budget': '⚠️ Budget seems low for {num} children. Recommended: ₹{amount}',
    'optimization_failed': '❌ Could not generate optimal plan. Try increasing budget or selecting more ingredients',
    'database_error': '❌ Database error. Please contact support',
    'export_error': '❌ Error exporting file: {error}'
}

# Success Messages
SUCCESS_MESSAGES = {
    'plan_generated': '✅ Meal plan generated successfully!',
    'plan_saved': '✅ Meal plan saved to database',
    'export_complete': '✅ File exported successfully',
    'database_initialized': '✅ Database initialized with sample data'
}

# Color Scheme for Charts
CHART_COLORS = {
    'protein': '#FF6B6B',
    'carbs': '#4ECDC4',
    'fat': '#FFE66D',
    'fiber': '#95E1D3',
    'iron': '#F38181',
    'calcium': '#AA96DA',
    'calories': '#FCBAD3'
}

# Thresholds for Color Coding
COLOR_THRESHOLDS = {
    'excellent': {'min': 90, 'max': 110, 'color': '#4CAF50'},
    'good': {'min': 80, 'max': 120, 'color': '#FFC107'},
    'fair': {'min': 70, 'max': 130, 'color': '#FF9800'},
    'poor': {'min': 0, 'max': 70, 'color': '#F44336'}
}

# API Configuration (if needed)
API_CONFIG = {
    'enable_external_api': False,
    'api_timeout': 10,
    'retry_attempts': 3
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'nutrition_advisor.log',
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Development Settings
DEV_CONFIG = {
    'debug_mode': False,
    'show_technical_details': False,
    'enable_profiling': False
}
