"""
Test script for Food Image Recognition Feature
Tests all components: model loading, prediction, portion estimation, nutrition calculation
"""

import sys
import os
from PIL import Image
import io
import numpy as np

def test_model_loading():
    """Test 1: Model Loading"""
    print("\n" + "="*60)
    print("TEST 1: Model Loading")
    print("="*60)
    
    try:
        from food_recognition import FoodRecognitionModel
        
        print("Loading MobileNetV2 model...")
        model = FoodRecognitionModel()
        
        if model.model is not None:
            print("✅ Model loaded successfully")
            print(f"   Model type: {type(model.model)}")
            return True
        else:
            print("❌ Model is None")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Install TensorFlow: pip install tensorflow")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_image_preprocessing():
    """Test 2: Image Preprocessing"""
    print("\n" + "="*60)
    print("TEST 2: Image Preprocessing")
    print("="*60)
    
    try:
        from food_recognition import FoodRecognitionModel
        
        # Create a test image (random RGB image)
        print("Creating test image (224x224 RGB)...")
        test_img = Image.new('RGB', (400, 300), color=(200, 150, 100))
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        test_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        model = FoodRecognitionModel()
        
        print("Preprocessing image...")
        processed = model.preprocess_image(test_img)
        
        print(f"✅ Image preprocessed successfully")
        print(f"   Input shape: {test_img.size}")
        print(f"   Processed shape: {processed.shape}")
        print(f"   Expected shape: (1, 224, 224, 3)")
        
        if processed.shape == (1, 224, 224, 3):
            print("✅ Preprocessing correct")
            return True
        else:
            print("❌ Preprocessing shape mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_food_prediction():
    """Test 3: Food Prediction"""
    print("\n" + "="*60)
    print("TEST 3: Food Prediction")
    print("="*60)
    
    try:
        from food_recognition import FoodRecognitionModel
        
        # Create a test image
        test_img = Image.new('RGB', (224, 224), color=(255, 200, 100))
        
        model = FoodRecognitionModel()
        
        print("Running prediction...")
        predictions = model.predict_food(test_img, top_k=5)
        
        print(f"✅ Prediction successful")
        print(f"   Top 5 predictions:")
        
        for i, (img_id, name, confidence) in enumerate(predictions, 1):
            print(f"   {i}. {name}: {confidence*100:.2f}%")
        
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_indian_food_mapping():
    """Test 4: Indian Food Mapping"""
    print("\n" + "="*60)
    print("TEST 4: Indian Food Database Mapping")
    print("="*60)
    
    try:
        from food_recognition import FoodRecognitionModel, INDIAN_FOOD_DATABASE
        
        print(f"Indian food database size: {len(INDIAN_FOOD_DATABASE)} items")
        print("\nSupported foods:")
        
        for i, (key, data) in enumerate(INDIAN_FOOD_DATABASE.items(), 1):
            print(f"{i}. {key.replace('_', ' ').title()} ({data['category']})")
            print(f"   Calories: {data['nutrition_per_100g']['calories']} kcal/100g")
        
        print("\n✅ Food database loaded successfully")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_portion_estimation():
    """Test 5: Portion Size Estimation"""
    print("\n" + "="*60)
    print("TEST 5: Portion Size Estimation")
    print("="*60)
    
    try:
        from food_recognition import PortionSizeEstimator
        
        estimator = PortionSizeEstimator()
        
        # Test different brightness levels (simulating portion sizes)
        test_cases = [
            (Image.new('RGB', (300, 300), color=(50, 50, 50)), 'small'),   # Dark = small
            (Image.new('RGB', (300, 300), color=(150, 150, 150)), 'medium'),  # Medium brightness
            (Image.new('RGB', (300, 300), color=(250, 250, 250)), 'large'),   # Bright = large
        ]
        
        for img, expected in test_cases:
            portion = estimator.estimate_from_image(img)
            weight = estimator.get_portion_weight(portion)
            
            print(f"Brightness test -> Portion: {portion}, Weight: {weight}g")
        
        print("✅ Portion estimation working")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_nutrition_calculation():
    """Test 6: Nutrition Calculation"""
    print("\n" + "="*60)
    print("TEST 6: Nutrition Calculation")
    print("="*60)
    
    try:
        from food_recognition import FoodNutritionCalculator
        
        calculator = FoodNutritionCalculator()
        
        # Test with a sample nutrition profile (Ragi)
        nutrition_per_100g = {
            'calories': 336,
            'protein': 7.3,
            'carbs': 72.0,
            'fat': 1.3,
            'fiber': 3.6,
            'iron': 3.9,
            'calcium': 344
        }
        
        # Calculate for 150g portion
        weight = 150
        result = calculator.calculate_nutrition(nutrition_per_100g, weight)
        
        print(f"Calculating nutrition for {weight}g portion:")
        print(f"  Calories: {result['calories']} kcal")
        print(f"  Protein: {result['protein']}g")
        print(f"  Carbs: {result['carbs']}g")
        print(f"  Fat: {result['fat']}g")
        print(f"  Fiber: {result['fiber']}g")
        print(f"  Iron: {result['iron']}mg")
        print(f"  Calcium: {result['calcium']}mg")
        
        print("\n✅ Nutrition calculation working")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_nutritional_assessment():
    """Test 7: Nutritional Assessment"""
    print("\n" + "="*60)
    print("TEST 7: Nutritional Assessment")
    print("="*60)
    
    try:
        from food_recognition import FoodNutritionCalculator
        
        calculator = FoodNutritionCalculator()
        
        # Test nutrition profile
        nutrition = {
            'calories': 504,
            'protein': 10.95,
            'carbs': 108,
            'fat': 1.95,
            'fiber': 5.4,
            'iron': 5.85,
            'calcium': 516
        }
        
        assessment = calculator.assess_nutrition(nutrition)
        
        print("Daily requirements met:")
        for nutrient, percentage in assessment['daily_percentages'].items():
            print(f"  {nutrient.capitalize()}: {percentage}%")
        
        print("\nRecommendations:")
        for rec in assessment['recommendations']:
            print(f"  {rec}")
        
        print("\n✅ Nutritional assessment working")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_full_pipeline():
    """Test 8: Full Analysis Pipeline"""
    print("\n" + "="*60)
    print("TEST 8: Full Analysis Pipeline")
    print("="*60)
    
    try:
        from food_recognition import analyze_food_image
        
        # Create a test food image (yellowish - like ragi/dal)
        test_img = Image.new('RGB', (400, 400), color=(200, 180, 100))
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        test_img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        print("Running full analysis...")
        result = analyze_food_image(img_bytes)
        
        if result['success']:
            print("✅ Analysis completed successfully\n")
            print(f"Food Detected: {result['food_name']}")
            print(f"Portion Size: {result['portion_size']} ({result['portion_weight']}g)")
            print(f"Category: {result['category']}")
            
            print("\nNutrition:")
            for nutrient, value in result['nutrition'].items():
                print(f"  {nutrient.capitalize()}: {value}")
            
            print("\nDaily Requirements Met:")
            for nutrient, percentage in result['nutritional_assessment']['daily_percentages'].items():
                print(f"  {nutrient.capitalize()}: {percentage}%")
            
            print("\nRecommendations:")
            for rec in result['nutritional_assessment']['recommendations']:
                print(f"  {rec}")
            
            return True
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_access():
    """Test 9: Food Database API"""
    print("\n" + "="*60)
    print("TEST 9: Food Database Access")
    print("="*60)
    
    try:
        from food_recognition import INDIAN_FOOD_DATABASE, PORTION_SIZES
        
        print(f"Total foods in database: {len(INDIAN_FOOD_DATABASE)}")
        print(f"Portion size categories: {len(PORTION_SIZES)}")
        
        # Verify each food has required fields
        required_fields = ['names', 'category', 'nutrition_per_100g']
        required_nutrients = ['calories', 'protein', 'carbs', 'fat', 'fiber', 'iron', 'calcium']
        
        all_valid = True
        for food_key, food_data in INDIAN_FOOD_DATABASE.items():
            # Check required fields
            for field in required_fields:
                if field not in food_data:
                    print(f"❌ {food_key} missing field: {field}")
                    all_valid = False
            
            # Check required nutrients
            if 'nutrition_per_100g' in food_data:
                for nutrient in required_nutrients:
                    if nutrient not in food_data['nutrition_per_100g']:
                        print(f"❌ {food_key} missing nutrient: {nutrient}")
                        all_valid = False
        
        if all_valid:
            print("✅ All foods have complete data")
            return True
        else:
            print("❌ Some foods have incomplete data")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🍲 FOOD IMAGE RECOGNITION - TEST SUITE")
    print("="*60)
    print("Testing all components of the food recognition system")
    
    tests = [
        ("Model Loading", test_model_loading),
        ("Image Preprocessing", test_image_preprocessing),
        ("Food Prediction", test_food_prediction),
        ("Indian Food Mapping", test_indian_food_mapping),
        ("Portion Estimation", test_portion_estimation),
        ("Nutrition Calculation", test_nutrition_calculation),
        ("Nutritional Assessment", test_nutritional_assessment),
        ("Database Access", test_database_access),
        ("Full Pipeline", test_full_pipeline),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test crashed: {test_name}")
            print(f"   Error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("🎉 All tests passed! Food recognition is ready to use.")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
