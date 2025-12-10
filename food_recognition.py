"""
Food Image Recognition + Portion Size Estimation
CUSTOM TRAINED MODEL for Indian Foods
Trains on your dataset and provides accurate predictions
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import io
import os
import json
from datetime import datetime
import pickle

# Indian food mapping database
INDIAN_FOOD_DATABASE = {
    'rice': {
        'names': ['rice', 'steamed_rice', 'white_rice', 'cooked_rice'],
        'category': 'grains',
        'nutrition_per_100g': {
            'calories': 130,
            'protein': 2.7,
            'carbs': 28.2,
            'fat': 0.3,
            'fiber': 0.4,
            'iron': 0.2,
            'calcium': 10
        }
    },
    'ragi_ball': {
        'names': ['ragi', 'finger_millet', 'mudde', 'ragi_ball'],
        'category': 'grains',
        'nutrition_per_100g': {
            'calories': 336,
            'protein': 7.3,
            'carbs': 72.0,
            'fat': 1.3,
            'fiber': 3.6,
            'iron': 3.9,
            'calcium': 344
        }
    },
    'dal': {
        'names': ['dal', 'lentil', 'dhal', 'pulses'],
        'category': 'legumes',
        'nutrition_per_100g': {
            'calories': 116,
            'protein': 9.0,
            'carbs': 20.1,
            'fat': 0.4,
            'fiber': 7.9,
            'iron': 3.3,
            'calcium': 27
        }
    },
    'egg': {
        'names': ['egg', 'boiled_egg', 'fried_egg', 'scrambled_egg'],
        'category': 'protein',
        'nutrition_per_100g': {
            'calories': 155,
            'protein': 13.0,
            'carbs': 1.1,
            'fat': 11.0,
            'fiber': 0,
            'iron': 1.8,
            'calcium': 50
        }
    },
    'banana': {
        'names': ['banana', 'plantain'],
        'category': 'fruit',
        'nutrition_per_100g': {
            'calories': 89,
            'protein': 1.1,
            'carbs': 22.8,
            'fat': 0.3,
            'fiber': 2.6,
            'iron': 0.3,
            'calcium': 5
        }
    },
    'chapati': {
        'names': ['chapati', 'roti', 'flatbread', 'wheat_bread'],
        'category': 'grains',
        'nutrition_per_100g': {
            'calories': 297,
            'protein': 11.0,
            'carbs': 45.0,
            'fat': 8.0,
            'fiber': 4.9,
            'iron': 4.0,
            'calcium': 48
        }
    },
    'chicken_curry': {
        'names': ['chicken', 'chicken_curry', 'poultry', 'meat'],
        'category': 'protein',
        'nutrition_per_100g': {
            'calories': 165,
            'protein': 31.0,
            'carbs': 0,
            'fat': 3.6,
            'fiber': 0,
            'iron': 0.9,
            'calcium': 15
        }
    },
    'milk': {
        'names': ['milk', 'dairy', 'whole_milk'],
        'category': 'dairy',
        'nutrition_per_100g': {
            'calories': 61,
            'protein': 3.2,
            'carbs': 4.8,
            'fat': 3.3,
            'fiber': 0,
            'iron': 0.05,
            'calcium': 113
        }
    },
    'yogurt': {
        'names': ['yogurt', 'curd', 'dahi'],
        'category': 'dairy',
        'nutrition_per_100g': {
            'calories': 61,
            'protein': 3.5,
            'carbs': 4.7,
            'fat': 3.3,
            'fiber': 0,
            'iron': 0.05,
            'calcium': 121
        }
    },
    'vegetable_curry': {
        'names': ['vegetables', 'curry', 'mixed_vegetables', 'sabzi'],
        'category': 'vegetables',
        'nutrition_per_100g': {
            'calories': 65,
            'protein': 2.0,
            'carbs': 12.0,
            'fat': 1.5,
            'fiber': 3.0,
            'iron': 1.2,
            'calcium': 40
        }
    }
}

# Portion size estimation based on image analysis
PORTION_SIZES = {
    'small': {
        'multiplier': 0.5,
        'weight_range': (50, 100),  # grams
        'description': 'Small portion (50-100g)'
    },
    'medium': {
        'multiplier': 1.0,
        'weight_range': (100, 200),  # grams
        'description': 'Medium portion (100-200g)'
    },
    'large': {
        'multiplier': 1.5,
        'weight_range': (200, 300),  # grams
        'description': 'Large portion (200-300g)'
    }
}


class FoodRecognitionModel:
    """Custom trained food recognition model for Indian foods"""
    
    def __init__(self, model_path='models/food_model.h5'):
        """Initialize the custom trained model"""
        self.model = None
        self.model_path = model_path
        self.class_names = list(INDIAN_FOOD_DATABASE.keys())
        self.img_size = (224, 224)
        
        # Try to load existing model
        if os.path.exists(model_path):
            self.load_model()
        else:
            print("⚠️  No trained model found. Please train the model first.")
            print("   Run: python train_food_model.py with your dataset")
    
    def build_model(self, num_classes):
        """
        Build custom CNN model for food classification
        Uses transfer learning with MobileNetV2 as base
        """
        # Base model (MobileNetV2) - frozen initially
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False
        
        # Custom classification head
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def load_model(self):
        """Load pre-trained model from disk"""
        try:
            self.model = keras.models.load_model(self.model_path)
            print(f"✅ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def save_model(self, path=None):
        """Save trained model to disk"""
        if path is None:
            path = self.model_path
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        print(f"✅ Model saved to {path}")
    
    def preprocess_image(self, img_data):
        """
        Preprocess image for model prediction
        Args:
            img_data: PIL Image or bytes
        Returns:
            Preprocessed numpy array
        """
        if isinstance(img_data, bytes):
            img = Image.open(io.BytesIO(img_data))
        else:
            img = img_data
        
        # Resize to model input size
        img = img.resize(self.img_size)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict_food(self, img_data):
        """
        Predict food type from image
        Args:
            img_data: Image data (PIL Image or bytes)
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            return {
                'error': 'Model not loaded. Please train the model first.',
                'class_name': 'unknown',
                'confidence': 0.0,
                'all_predictions': []
            }
        
        # Preprocess image
        processed_img = self.preprocess_image(img_data)
        
        # Make prediction
        predictions = self.model.predict(processed_img, verbose=0)[0]
        
        # Get top prediction
        top_idx = np.argmax(predictions)
        top_class = self.class_names[top_idx]
        top_confidence = float(predictions[top_idx])
        
        # Get all predictions sorted by confidence
        all_predictions = [
            {
                'class_name': self.class_names[i],
                'confidence': float(predictions[i])
            }
            for i in np.argsort(predictions)[::-1]
        ]
        
        return {
            'class_name': top_class,
            'confidence': top_confidence,
            'all_predictions': all_predictions[:5]  # Top 5
        }


class PortionSizeEstimator:
    """Estimate portion size from image analysis"""
    
    def __init__(self):
        """Initialize portion estimator"""
        pass
    
    def estimate_from_image(self, img_data):
        """
        Estimate portion size from image
        Uses image brightness, area, and pixel analysis
        
        Args:
            img_data: PIL Image or bytes
        Returns:
            Portion size category ('small', 'medium', 'large')
        """
        if isinstance(img_data, bytes):
            img = Image.open(io.BytesIO(img_data))
        else:
            img = img_data
        
        # Convert to grayscale for analysis
        gray_img = img.convert('L')
        img_array = np.array(gray_img)
        
        # Calculate features
        total_pixels = img_array.size
        bright_pixels = np.sum(img_array > 100)  # Count bright pixels (likely food)
        coverage_ratio = bright_pixels / total_pixels
        
        # Estimate portion based on coverage
        if coverage_ratio < 0.3:
            return 'small'
        elif coverage_ratio < 0.6:
            return 'medium'
        else:
            return 'large'
    
    def get_portion_weight(self, portion_size):
        """
        Get estimated weight for portion size
        Args:
            portion_size: 'small', 'medium', or 'large'
        Returns:
            Average weight in grams
        """
        if portion_size not in PORTION_SIZES:
            portion_size = 'medium'
        
        weight_range = PORTION_SIZES[portion_size]['weight_range']
        return (weight_range[0] + weight_range[1]) / 2


class FoodNutritionCalculator:
    """Calculate nutritional information for recognized food"""
    
    def __init__(self):
        """Initialize nutrition calculator"""
        self.recognizer = FoodRecognitionModel()
        self.portion_estimator = PortionSizeEstimator()
    
    def analyze_meal(self, img_data):
        """
        Complete meal analysis from image
        Args:
            img_data: Image data (PIL Image or bytes)
        Returns:
            Dictionary with food type, portion, and nutrition info
        """
        try:
            # Recognize food
            prediction = self.recognizer.predict_food(img_data)
            
            # Check if model is trained
            if 'error' in prediction:
                return {
                    'success': False,
                    'error': prediction['error'],
                    'message': 'Please train the model first with your dataset',
                    'timestamp': datetime.now().isoformat()
                }
            
            food_key = prediction['class_name']
            confidence = prediction['confidence']
            
            # Get food data
            if food_key not in INDIAN_FOOD_DATABASE:
                return {
                    'success': False,
                    'error': f'Unknown food: {food_key}',
                    'timestamp': datetime.now().isoformat()
                }
            
            food_data = INDIAN_FOOD_DATABASE[food_key]
            
            # Estimate portion size
            portion_size = self.portion_estimator.estimate_from_image(img_data)
            portion_weight = self.portion_estimator.get_portion_weight(portion_size)
            
            # Calculate nutrition
            nutrition = self.calculate_nutrition(
                food_data['nutrition_per_100g'],
                portion_weight
            )
            
            # Build result
            result = {
                'success': True,
                'food_name': food_key.replace('_', ' ').title(),
                'food_key': food_key,
                'category': food_data['category'],
                'confidence': round(confidence * 100, 2),
                'portion_size': portion_size,
                'portion_weight': portion_weight,
                'portion_description': PORTION_SIZES[portion_size]['description'],
                'nutrition': nutrition,
                'predictions': prediction['all_predictions'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Check nutritional requirements
            result['nutritional_assessment'] = self.assess_nutrition(nutrition)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def calculate_nutrition(self, nutrition_per_100g, weight_grams):
        """
        Calculate nutrition for given weight
        Args:
            nutrition_per_100g: Nutrition per 100g
            weight_grams: Actual weight in grams
        Returns:
            Calculated nutrition values
        """
        multiplier = weight_grams / 100.0
        
        return {
            'calories': round(nutrition_per_100g['calories'] * multiplier, 2),
            'protein': round(nutrition_per_100g['protein'] * multiplier, 2),
            'carbs': round(nutrition_per_100g['carbs'] * multiplier, 2),
            'fat': round(nutrition_per_100g['fat'] * multiplier, 2),
            'fiber': round(nutrition_per_100g['fiber'] * multiplier, 2),
            'iron': round(nutrition_per_100g['iron'] * multiplier, 2),
            'calcium': round(nutrition_per_100g['calcium'] * multiplier, 2)
        }
    
    def assess_nutrition(self, nutrition):
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
            'calories': round((nutrition['calories'] / daily_requirements['calories']) * 100, 1),
            'protein': round((nutrition['protein'] / daily_requirements['protein']) * 100, 1),
            'iron': round((nutrition['iron'] / daily_requirements['iron']) * 100, 1),
            'calcium': round((nutrition['calcium'] / daily_requirements['calcium']) * 100, 1)
        }
        
        # Generate recommendations
        recommendations = []
        
        if percentages['calories'] < 20:
            recommendations.append("⚠️ Low calorie content for a meal")
        if percentages['protein'] < 25:
            recommendations.append("⚠️ Add protein-rich foods (dal, egg, chicken)")
        if percentages['iron'] < 15:
            recommendations.append("⚠️ Include iron-rich foods (ragi, green vegetables)")
        if percentages['calcium'] < 15:
            recommendations.append("⚠️ Add calcium sources (milk, yogurt)")
        
        if not recommendations:
            recommendations.append("✅ Well-balanced meal!")
        
        return {
            'daily_percentages': percentages,
            'recommendations': recommendations,
            'meets_requirements': len([r for r in recommendations if '⚠️' in r]) == 0
        }


# Global instance
_food_calculator = None

def get_food_calculator():
    """Get or create food nutrition calculator instance"""
    global _food_calculator
    if _food_calculator is None:
        _food_calculator = FoodNutritionCalculator()
    return _food_calculator


def analyze_food_image(image_data):
    """
    Main function to analyze food image
    Args:
        image_data: Image bytes or PIL Image
    Returns:
        Analysis result dictionary
    """
    calculator = get_food_calculator()
    return calculator.analyze_meal(image_data)


if __name__ == "__main__":
    # Test with sample image
    print("🍲 Food Recognition System")
    print("=" * 50)
    print("Model: MobileNetV2")
    print("Supported Foods:", len(INDIAN_FOOD_DATABASE))
    print("=" * 50)
    
    # Initialize
    calculator = FoodNutritionCalculator()
    print("✅ System initialized successfully")
