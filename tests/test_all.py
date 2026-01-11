"""
Test Suite for AI Nutrition Advisor
Run this to verify all components are working correctly
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import streamlit
        print("✓ Streamlit imported")
        
        import pandas
        print("✓ Pandas imported")
        
        import numpy
        print("✓ NumPy imported")
        
        import plotly
        print("✓ Plotly imported")
        
        from pulp import *
        print("✓ PuLP imported")
        
        from fpdf import FPDF
        print("✓ FPDF imported")
        
        from googletrans import Translator
        print("✓ Googletrans imported")
        
        import sqlite3
        print("✓ SQLite3 imported")
        
        print("\n✅ All imports successful!\n")
        return True
    except Exception as e:
        print(f"\n❌ Import error: {e}\n")
        return False

def test_database():
    """Test database operations"""
    print("Testing database...")
    try:
        import database as db
        
        # Initialize database
        db.initialize_database()
        print("✓ Database initialized")
        
        # Get ingredients
        ingredients_df = db.get_all_ingredients()
        print(f"✓ Retrieved {len(ingredients_df)} ingredients")
        
        # Check if we have enough ingredients
        if len(ingredients_df) < 10:
            print("⚠️ Warning: Less than 10 ingredients in database")
        
        # Get ingredients by category
        by_category = db.get_ingredients_by_category()
        print(f"✓ Ingredients organized in {len(by_category)} categories")
        
        print("\n✅ Database tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Database error: {e}\n")
        return False

def test_optimizer():
    """Test meal optimization engine"""
    print("Testing meal optimizer...")
    try:
        import database as db
        from meal_optimizer import MealOptimizer
        
        # Get ingredients
        ingredients_df = db.get_all_ingredients()
        
        # Select some test ingredients
        test_ingredients = [
            'Rice', 'Wheat Flour (Atta)', 'Moong Dal', 'Toor Dal',
            'Potato', 'Onion', 'Tomato', 'Spinach (Palak)',
            'Milk', 'Cooking Oil'
        ]
        
        # Create optimizer
        optimizer = MealOptimizer(
            ingredients_df=ingredients_df,
            budget=2000,
            num_children=20,
            age_group="3-6 years"
        )
        print("✓ Optimizer created")
        
        # Generate meal plan
        print("  Generating meal plan (this may take 10-20 seconds)...")
        meal_plan = optimizer.generate_meal_plan(test_ingredients)
        print("✓ Meal plan generated")
        
        # Verify meal plan structure
        assert 'weekly_plan' in meal_plan
        assert 'total_cost' in meal_plan
        assert 'nutrition_score' in meal_plan
        print("✓ Meal plan structure valid")
        
        # Check if we have 7 days
        assert len(meal_plan['weekly_plan']) == 7
        print("✓ Plan contains 7 days")
        
        # Check nutrition score
        score = meal_plan['nutrition_score']
        print(f"✓ Nutrition score: {score}/100")
        
        if score < 60:
            print("⚠️ Warning: Nutrition score is low")
        
        # Check cost
        cost = meal_plan['total_cost']
        print(f"✓ Total cost: ₹{cost:.2f}")
        
        print("\n✅ Optimizer tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Optimizer error: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_utils():
    """Test utility functions"""
    print("Testing utilities...")
    try:
        from utils import get_food_emoji, format_currency
        
        # Test emoji function
        emoji = get_food_emoji('Grains')
        print(f"✓ Emoji for Grains: {emoji}")
        
        # Test currency formatting
        formatted = format_currency(1234.56)
        print(f"✓ Currency format: {formatted}")
        
        print("\n✅ Utility tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Utility error: {e}\n")
        return False

def test_config():
    """Test configuration file"""
    print("Testing configuration...")
    try:
        import config
        
        # Check if main config sections exist
        assert hasattr(config, 'APP_CONFIG')
        print("✓ APP_CONFIG found")
        
        assert hasattr(config, 'OPTIMIZATION_CONFIG')
        print("✓ OPTIMIZATION_CONFIG found")
        
        assert hasattr(config, 'NUTRITIONAL_REQUIREMENTS')
        print("✓ NUTRITIONAL_REQUIREMENTS found")
        
        # Check age groups
        age_groups = list(config.NUTRITIONAL_REQUIREMENTS.keys())
        print(f"✓ Age groups configured: {len(age_groups)}")
        
        print("\n✅ Configuration tests passed!\n")
        return True
    except Exception as e:
        print(f"\n❌ Configuration error: {e}\n")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'app.py',
        'database.py',
        'meal_optimizer.py',
        'utils.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'QUICK_START.md',
        'PROJECT_SUMMARY.md',
        'TROUBLESHOOTING.md',
        'setup.ps1',
        'run.ps1',
        'LICENSE',
        '.gitignore'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    if all_exist:
        print("\n✅ All files present!\n")
        return True
    else:
        print("\n⚠️ Some files are missing\n")
        return False

def test_database_content():
    """Test database content"""
    print("Testing database content...")
    try:
        import database as db
        import pandas as pd
        
        ingredients_df = db.get_all_ingredients()
        
        # Check required columns
        required_columns = [
            'name', 'category', 'cost_per_kg',
            'protein_per_100g', 'carbs_per_100g', 'fat_per_100g',
            'calories_per_100g'
        ]
        
        for col in required_columns:
            assert col in ingredients_df.columns
            print(f"✓ Column '{col}' exists")
        
        # Check for null values
        nulls = ingredients_df[required_columns].isnull().sum()
        if nulls.sum() == 0:
            print("✓ No null values in critical columns")
        else:
            print("⚠️ Warning: Some null values found")
        
        # Check data types
        assert pd.api.types.is_numeric_dtype(ingredients_df['cost_per_kg'])
        print("✓ Cost data is numeric")
        
        assert pd.api.types.is_numeric_dtype(ingredients_df['calories_per_100g'])
        print("✓ Calorie data is numeric")
        
        # Check categories
        categories = ingredients_df['category'].unique()
        print(f"✓ Found {len(categories)} categories: {', '.join(categories)}")
        
        print("\n✅ Database content validated!\n")
        return True
    except Exception as e:
        print(f"\n❌ Database content error: {e}\n")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("AI NUTRITION ADVISOR - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()
    
    results = {
        'File Structure': test_file_structure(),
        'Imports': test_imports(),
        'Configuration': test_config(),
        'Database': test_database(),
        'Database Content': test_database_content(),
        'Utilities': test_utils(),
        'Optimizer': test_optimizer(),
    }
    
    print("=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print()
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print()
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"Total: {passed_count}/{total_count} tests passed")
    print()
    
    if passed_count == total_count:
        print("🎉 ALL TESTS PASSED! Application is ready to use.")
        print()
        print("To start the application, run:")
        print("  streamlit run app.py")
        return True
    else:
        print("⚠️ SOME TESTS FAILED! Please review errors above.")
        print()
        print("Common solutions:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Check Python version: python --version (need 3.8+)")
        print("  3. Reinitialize database: python database.py")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
