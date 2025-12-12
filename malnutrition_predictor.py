"""
Malnutrition Predictor using trained Random Forest model from CSV data
Loads the model trained on real malnutrition data
Auto-fallback to WHO z-score based predictor if models unavailable
"""

import numpy as np
import pickle
import os
from datetime import datetime

class MalnutritionPredictor:
    """Malnutrition prediction using trained Random Forest model"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.metadata = None
        self.model_path = 'models/malnutrition/'
        self.use_fallback = False
        self.fallback_predictor = None
        
        self._load_trained_model()
    
    def _load_trained_model(self):
        """Load the trained model from disk, fallback to simple predictor if unavailable"""
        try:
            # Load main model
            model_file = os.path.join(self.model_path, 'trained_model.pkl')
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load label encoder
            encoder_file = os.path.join(self.model_path, 'label_encoder.pkl')
            with open(encoder_file, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            # Load metadata
            metadata_file = os.path.join(self.model_path, 'model_metadata.pkl')
            with open(metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
            
            print("[OK] Trained model loaded successfully")
            print(f"   Accuracy: {self.metadata['accuracy']*100:.2f}%")
            print(f"   Classes: {self.metadata['classes']}")
            print(f"   Training date: {self.metadata['training_date']}")
            
        except (FileNotFoundError, Exception) as e:
            print(f"[WARNING] Trained model not available: {e}")
            print("[INFO] Using fallback predictor (WHO z-score based)")
            self.use_fallback = True
            
            # Import and use fallback predictor
            try:
                from fallback_predictor import FallbackPredictor
                self.fallback_predictor = FallbackPredictor()
                self.metadata = self.fallback_predictor.metadata
            except ImportError:
                print("[ERROR] Fallback predictor not found!")
                raise Exception("Neither trained model nor fallback predictor available")
    
    def calculate_bmi(self, weight_kg, height_cm):
        """Calculate BMI from weight and height"""
        height_m = height_cm / 100.0
        return weight_kg / (height_m ** 2)
    
    def calculate_muac(self, age_months, weight_kg):
        """Estimate MUAC (Mid-Upper Arm Circumference)"""
        # Simplified estimation based on age and weight
        base_muac = 11.0 + (age_months * 0.05) + (weight_kg * 0.15)
        return np.clip(base_muac, 10.0, 20.0)
    
    def predict(self, age_months, weight_kg, height_cm, muac_cm=None, gender='male'):
        """
        Predict malnutrition status
        
        Args:
            age_months: Child's age in months
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            muac_cm: Mid-Upper Arm Circumference (optional, will be estimated)
            gender: 'male' or 'female' (used in fallback mode)
        
        Returns:
            dict with prediction results
        """
        # Use fallback predictor if trained model not available
        if self.use_fallback:
            return self.fallback_predictor.predict(
                age_months, weight_kg, height_cm, muac_cm, gender
            )
        
        # Use trained model
        # Calculate/estimate features
        bmi = self.calculate_bmi(weight_kg, height_cm)
        
        if muac_cm is None:
            muac_cm = self.calculate_muac(age_months, weight_kg)
        
        # Prepare features in correct order
        features = np.array([[age_months, weight_kg, height_cm, muac_cm, bmi]])
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        # Get class name
        predicted_class = self.label_encoder.inverse_transform([prediction])[0]
        
        # Get probabilities for all classes
        class_probabilities = {}
        for i, class_name in enumerate(self.label_encoder.classes_):
            class_probabilities[class_name] = float(probabilities[i])
        
        # Determine risk level
        risk_level = self._get_risk_level(predicted_class, probabilities[prediction])
        
        # Calculate z-scores for display (simplified WHO calculation)
        z_scores = self._calculate_simple_zscores(age_months, weight_kg, height_cm, bmi, gender)
        
        return {
            'nutrition_status': predicted_class,
            'confidence': float(probabilities[prediction]),
            'risk_level': risk_level,
            'probabilities': class_probabilities,
            'features_used': {
                'age_months': age_months,
                'weight_kg': weight_kg,
                'height_cm': height_cm,
                'muac_cm': muac_cm,
                'bmi': bmi
            },
            'z_scores': z_scores
        }
    
    def _get_risk_level(self, nutrition_status, confidence):
        """Convert nutrition status to risk level"""
        if nutrition_status == 'severe':
            return 'critical'
        elif nutrition_status == 'moderate':
            return 'high'
        elif nutrition_status == 'mild':
            return 'medium'
        else:  # normal
            return 'low'
    
    def _calculate_simple_zscores(self, age_months, weight_kg, height_cm, bmi, gender='male'):
        """
        Calculate simplified z-scores for display
        Based on WHO growth standards (simplified version)
        """
        # Simplified median values (males)
        median_weights = {0: 3.3, 6: 7.9, 12: 9.6, 18: 11.0, 24: 12.2, 36: 14.3, 48: 16.3, 60: 18.3}
        median_heights = {0: 49.9, 6: 67.6, 12: 75.7, 18: 82.3, 24: 87.1, 36: 96.1, 48: 103.3, 60: 109.2}
        median_bmis = {12: 16.5, 24: 16.2, 36: 15.8, 48: 15.5, 60: 15.3}
        
        # Adjust for gender (females ~5% lighter)
        gender_factor = 0.95 if gender.lower() == 'female' else 1.0
        
        # Find closest age bracket
        closest_age_w = min(median_weights.keys(), key=lambda x: abs(x - age_months))
        expected_weight = median_weights[closest_age_w] * gender_factor
        
        closest_age_h = min(median_heights.keys(), key=lambda x: abs(x - age_months))
        expected_height = median_heights[closest_age_h] * gender_factor
        
        closest_age_b = min(median_bmis.keys(), key=lambda x: abs(x - age_months))
        expected_bmi = median_bmis[closest_age_b]
        
        # Calculate z-scores (simplified: (actual - expected) / SD, using SD ~15% of expected)
        waz = (weight_kg - expected_weight) / (expected_weight * 0.15)
        haz = (height_cm - expected_height) / (expected_height * 0.05)
        baz = (bmi - expected_bmi) / (expected_bmi * 0.15)
        
        return {
            'weight_for_age': round(waz, 2),
            'height_for_age': round(haz, 2),
            'bmi_for_age': round(baz, 2)
        }
    
    def predict_from_child_data(self, child_data):
        """
        Predict from child data dictionary (for API compatibility)
        
        Args:
            child_data: Dict with age_months, weight_kg, height_cm, gender
        """
        # Use fallback predictor if trained model not available
        if self.use_fallback:
            return self.fallback_predictor.predict_from_child_data(child_data)
        
        return self.predict(
            age_months=child_data.get('age_months'),
            weight_kg=child_data.get('weight_kg'),
            height_cm=child_data.get('height_cm'),
            muac_cm=child_data.get('muac_cm'),
            gender=child_data.get('gender', 'male')
        )


# Global predictor instance
_predictor_instance = None

def get_predictor(force_reload=False):
    """
    Get the malnutrition predictor instance
    
    Args:
        force_reload: If True, recreates the predictor
    """
    global _predictor_instance
    
    if _predictor_instance is None or force_reload:
        _predictor_instance = MalnutritionPredictor()
    
    return _predictor_instance


# Test function
if __name__ == '__main__':
    print("\n" + "="*80)
    print("   TESTING MALNUTRITION PREDICTOR")
    print("="*80)
    
    predictor = get_predictor()
    
    # Test cases
    test_cases = [
        {'name': 'Healthy Child', 'age_months': 36, 'weight_kg': 14.0, 'height_cm': 95.0},
        {'name': 'Underweight Child', 'age_months': 48, 'weight_kg': 11.0, 'height_cm': 95.0},
        {'name': 'Severely Malnourished', 'age_months': 60, 'weight_kg': 10.0, 'height_cm': 90.0}
    ]
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing: {test['name']}")
        print(f"Age: {test['age_months']}mo, Weight: {test['weight_kg']}kg, Height: {test['height_cm']}cm")
        
        result = predictor.predict(test['age_months'], test['weight_kg'], test['height_cm'])
        
        print(f"\n📊 Prediction:")
        print(f"   Status: {result['nutrition_status'].upper()}")
        print(f"   Risk Level: {result['risk_level'].upper()}")
        print(f"   Confidence: {result['confidence']*100:.1f}%")
        print(f"\n   Probabilities:")
        for status, prob in result['probabilities'].items():
            print(f"      {status:12s}: {prob*100:5.1f}%")
