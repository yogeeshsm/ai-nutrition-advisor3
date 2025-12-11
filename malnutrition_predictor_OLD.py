"""
Malnutrition Risk Prediction System using Machine Learning
Predicts risk of Underweight, Stunting, and Wasting in children
Uses Random Forest Classifier for accurate predictions
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

class MalnutritionPredictor:
    """ML-based malnutrition risk prediction system"""
    
    def __init__(self):
        self.model_underweight = None
        self.model_stunting = None
        self.model_wasting = None
        self.scaler = StandardScaler()
        self.model_path = 'models/malnutrition/'
        
        # WHO Z-score thresholds
        self.THRESHOLDS = {
            'underweight': -2.0,  # Weight-for-age
            'stunting': -2.0,     # Height-for-age
            'wasting': -2.0       # Weight-for-height
        }
        
        self._ensure_model_directory()
        self._load_or_train_models()
    
    def _ensure_model_directory(self):
        """Create model directory if it doesn't exist"""
        os.makedirs(self.model_path, exist_ok=True)
    
    def calculate_z_score(self, value, mean, sd):
        """Calculate WHO Z-score"""
        if sd == 0:
            return 0
        return (value - mean) / sd
    
    def get_who_standards(self, age_months, gender):
        """
        Get WHO growth standards (simplified)
        In production, use full WHO tables
        """
        # Simplified WHO standards (boys/girls average)
        standards = {
            'M': {  # Males
                6: {'weight': 7.9, 'height': 67.6, 'wsd': 0.97, 'hsd': 2.4},
                12: {'weight': 9.6, 'height': 75.7, 'wsd': 1.16, 'hsd': 2.8},
                24: {'weight': 12.2, 'height': 87.1, 'wsd': 1.46, 'hsd': 3.3},
                36: {'weight': 14.3, 'height': 96.1, 'wsd': 1.74, 'hsd': 3.7},
                48: {'weight': 16.3, 'height': 103.3, 'wsd': 2.01, 'hsd': 4.0},
                60: {'weight': 18.3, 'height': 110.0, 'wsd': 2.28, 'hsd': 4.3},
                72: {'weight': 20.3, 'height': 116.1, 'wsd': 2.55, 'hsd': 4.6}
            },
            'F': {  # Females
                6: {'weight': 7.3, 'height': 65.7, 'wsd': 0.95, 'hsd': 2.4},
                12: {'weight': 9.0, 'height': 74.0, 'wsd': 1.14, 'hsd': 2.8},
                24: {'weight': 11.5, 'height': 85.7, 'wsd': 1.42, 'hsd': 3.3},
                36: {'weight': 13.9, 'height': 95.1, 'wsd': 1.69, 'hsd': 3.8},
                48: {'weight': 16.0, 'height': 102.7, 'wsd': 1.96, 'hsd': 4.1},
                60: {'weight': 18.0, 'height': 109.4, 'wsd': 2.23, 'hsd': 4.4},
                72: {'weight': 20.0, 'height': 115.7, 'wsd': 2.50, 'hsd': 4.7}
            }
        }
        
        # Find nearest age standard
        nearest_age = min(standards[gender].keys(), key=lambda x: abs(x - age_months))
        return standards[gender][nearest_age]
    
    def calculate_nutritional_status(self, age_months, weight_kg, height_cm, gender):
        """Calculate Z-scores and nutritional status"""
        standards = self.get_who_standards(age_months, gender)
        
        # Weight-for-age Z-score (underweight)
        wfa_zscore = self.calculate_z_score(weight_kg, standards['weight'], standards['wsd'])
        
        # Height-for-age Z-score (stunting)
        hfa_zscore = self.calculate_z_score(height_cm, standards['height'], standards['hsd'])
        
        # Weight-for-height (wasting) - simplified calculation
        expected_weight = standards['weight'] * (height_cm / standards['height'])
        wfh_zscore = self.calculate_z_score(weight_kg, expected_weight, standards['wsd'])
        
        return {
            'wfa_zscore': wfa_zscore,
            'hfa_zscore': hfa_zscore,
            'wfh_zscore': wfh_zscore,
            'is_underweight': wfa_zscore < self.THRESHOLDS['underweight'],
            'is_stunted': hfa_zscore < self.THRESHOLDS['stunting'],
            'is_wasted': wfh_zscore < self.THRESHOLDS['wasting']
        }
    
    def prepare_features(self, child_data, growth_history=None):
        """
        Prepare feature vector for ML model
        
        Args:
            child_data: Dict with current child data
            growth_history: List of past growth records (optional)
        """
        features = []
        
        # Basic features
        features.append(child_data.get('age_months', 0))
        features.append(child_data.get('weight_kg', 0))
        features.append(child_data.get('height_cm', 0))
        features.append(1 if child_data.get('gender') == 'M' else 0)
        
        # Calculate current Z-scores
        status = self.calculate_nutritional_status(
            child_data.get('age_months', 0),
            child_data.get('weight_kg', 0),
            child_data.get('height_cm', 0),
            child_data.get('gender', 'M')
        )
        features.extend([status['wfa_zscore'], status['hfa_zscore'], status['wfh_zscore']])
        
        # Growth velocity features (if history available)
        if growth_history and len(growth_history) >= 2:
            # Weight gain rate (kg/month)
            weight_change = growth_history[-1]['weight'] - growth_history[0]['weight']
            months_diff = growth_history[-1]['age_months'] - growth_history[0]['age_months']
            weight_velocity = weight_change / max(months_diff, 1)
            
            # Height gain rate (cm/month)
            height_change = growth_history[-1]['height'] - growth_history[0]['height']
            height_velocity = height_change / max(months_diff, 1)
            
            features.extend([weight_velocity, height_velocity])
        else:
            features.extend([0.0, 0.0])  # No history available
        
        # Dietary features
        features.append(child_data.get('meals_per_day', 3))
        features.append(child_data.get('milk_intake_ml', 500))
        features.append(child_data.get('protein_servings', 2))
        features.append(child_data.get('vegetable_servings', 2))
        
        # Health features
        features.append(child_data.get('illness_days_last_month', 0))
        features.append(1 if child_data.get('diarrhea_recent', False) else 0)
        features.append(1 if child_data.get('fever_recent', False) else 0)
        
        return np.array(features).reshape(1, -1)
    
    def predict_risk(self, child_data, growth_history=None):
        """
        Predict malnutrition risk for a child
        
        Returns:
            Dict with risk predictions and confidence scores
        """
        # Prepare features
        features = self.prepare_features(child_data, growth_history)
        
        # Calculate current nutritional status
        status = self.calculate_nutritional_status(
            child_data.get('age_months', 0),
            child_data.get('weight_kg', 0),
            child_data.get('height_cm', 0),
            child_data.get('gender', 'M')
        )
        
        # Get predictions from models
        predictions = {}
        
        if self.model_underweight:
            underweight_pred = self.model_underweight.predict_proba(features)[0]
            predictions['underweight'] = {
                'risk_level': 'high' if underweight_pred[1] > 0.7 else 'medium' if underweight_pred[1] > 0.4 else 'low',
                'probability': float(underweight_pred[1]),
                'current_status': status['is_underweight'],
                'zscore': float(status['wfa_zscore'])
            }
        
        if self.model_stunting:
            stunting_pred = self.model_stunting.predict_proba(features)[0]
            predictions['stunting'] = {
                'risk_level': 'high' if stunting_pred[1] > 0.7 else 'medium' if stunting_pred[1] > 0.4 else 'low',
                'probability': float(stunting_pred[1]),
                'current_status': status['is_stunted'],
                'zscore': float(status['hfa_zscore'])
            }
        
        if self.model_wasting:
            wasting_pred = self.model_wasting.predict_proba(features)[0]
            predictions['wasting'] = {
                'risk_level': 'high' if wasting_pred[1] > 0.7 else 'medium' if wasting_pred[1] > 0.4 else 'low',
                'probability': float(wasting_pred[1]),
                'current_status': status['is_wasted'],
                'zscore': float(status['wfh_zscore'])
            }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(predictions, child_data)
        
        return {
            'predictions': predictions,
            'recommendations': recommendations,
            'overall_risk': self._calculate_overall_risk(predictions)
        }
    
    def _calculate_overall_risk(self, predictions):
        """Calculate overall malnutrition risk score"""
        high_risks = sum(1 for p in predictions.values() if p['risk_level'] == 'high')
        medium_risks = sum(1 for p in predictions.values() if p['risk_level'] == 'medium')
        
        if high_risks >= 2:
            return 'critical'
        elif high_risks >= 1:
            return 'high'
        elif medium_risks >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, predictions, child_data):
        """Generate personalized recommendations based on risk predictions"""
        recommendations = []
        
        # Underweight recommendations
        if predictions.get('underweight', {}).get('risk_level') in ['high', 'medium']:
            recommendations.extend([
                {
                    'category': 'Diet',
                    'priority': 'high',
                    'action': 'Increase calorie intake by 300-500 kcal/day',
                    'details': 'Add energy-dense foods like banana, potato, rice, ghee'
                },
                {
                    'category': 'Monitoring',
                    'priority': 'high',
                    'action': 'Weekly weight monitoring required',
                    'details': 'Track weight gain progress every 7 days'
                }
            ])
        
        # Stunting recommendations
        if predictions.get('stunting', {}).get('risk_level') in ['high', 'medium']:
            recommendations.extend([
                {
                    'category': 'Nutrition',
                    'priority': 'high',
                    'action': 'Increase protein intake to 15-20g/day',
                    'details': 'Include eggs, dal, milk, paneer, chicken/fish'
                },
                {
                    'category': 'Supplements',
                    'priority': 'medium',
                    'action': 'Consider zinc supplementation',
                    'details': 'Consult doctor for zinc supplements (10mg/day)'
                }
            ])
        
        # Wasting recommendations
        if predictions.get('wasting', {}).get('risk_level') in ['high', 'medium']:
            recommendations.extend([
                {
                    'category': 'Urgent Care',
                    'priority': 'critical',
                    'action': 'Immediate medical evaluation needed',
                    'details': 'Visit health center for assessment and treatment plan'
                },
                {
                    'category': 'Diet',
                    'priority': 'high',
                    'action': 'High-energy, high-protein diet',
                    'details': 'Frequent small meals (6-8 times/day) with energy-dense foods'
                }
            ])
        
        # General recommendations
        if child_data.get('illness_days_last_month', 0) > 5:
            recommendations.append({
                'category': 'Health',
                'priority': 'high',
                'action': 'Address frequent illness',
                'details': 'Consult doctor about recurring infections, ensure vaccinations up-to-date'
            })
        
        if child_data.get('meals_per_day', 3) < 3:
            recommendations.append({
                'category': 'Feeding',
                'priority': 'medium',
                'action': 'Increase meal frequency to minimum 3-4 times/day',
                'details': 'Include healthy snacks between main meals'
            })
        
        return recommendations
    
    def _load_or_train_models(self):
        """Load existing models or train new ones"""
        try:
            # Try to load existing models
            with open(os.path.join(self.model_path, 'underweight_model.pkl'), 'rb') as f:
                self.model_underweight = pickle.load(f)
            with open(os.path.join(self.model_path, 'stunting_model.pkl'), 'rb') as f:
                self.model_stunting = pickle.load(f)
            with open(os.path.join(self.model_path, 'wasting_model.pkl'), 'rb') as f:
                self.model_wasting = pickle.load(f)
            print("✅ Malnutrition prediction models loaded successfully")
        except:
            # Train new models with synthetic data
            print("📊 Training new malnutrition prediction models...")
            self._train_models()
    
    def _train_models(self):
        """Train Random Forest models with synthetic training data"""
        # Generate synthetic training data
        X_train, y_underweight, y_stunting, y_wasting = self._generate_training_data()
        
        # Train underweight model
        self.model_underweight = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model_underweight.fit(X_train, y_underweight)
        
        # Train stunting model
        self.model_stunting = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model_stunting.fit(X_train, y_stunting)
        
        # Train wasting model
        self.model_wasting = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model_wasting.fit(X_train, y_wasting)
        
        # Save models
        with open(os.path.join(self.model_path, 'underweight_model.pkl'), 'wb') as f:
            pickle.dump(self.model_underweight, f)
        with open(os.path.join(self.model_path, 'stunting_model.pkl'), 'wb') as f:
            pickle.dump(self.model_stunting, f)
        with open(os.path.join(self.model_path, 'wasting_model.pkl'), 'wb') as f:
            pickle.dump(self.model_wasting, f)
        
        print("✅ Models trained and saved successfully")
    
    def _generate_training_data(self, n_samples=2000):
        """Generate realistic training data based on WHO standards"""
        np.random.seed(42)
        
        # Generate features with realistic distributions
        age_months = np.random.randint(6, 73, n_samples)
        gender = np.random.choice([0, 1], n_samples)
        
        # Generate realistic Z-score distribution
        # 70% normal (-1 to +1), 20% mild risk (-2 to -1), 8% moderate (-3 to -2), 2% severe (< -3)
        categories = np.random.choice(['normal', 'mild', 'moderate', 'severe'], 
                                     n_samples, p=[0.70, 0.20, 0.08, 0.02])
        
        wfa_zscore = np.zeros(n_samples)
        hfa_zscore = np.zeros(n_samples)
        wfh_zscore = np.zeros(n_samples)
        
        for i in range(n_samples):
            if categories[i] == 'normal':
                wfa_zscore[i] = np.random.uniform(-1, 1)
                hfa_zscore[i] = np.random.uniform(-1, 1)
                wfh_zscore[i] = np.random.uniform(-1, 1)
            elif categories[i] == 'mild':
                wfa_zscore[i] = np.random.uniform(-2, -1)
                hfa_zscore[i] = np.random.uniform(-2, -1)
                wfh_zscore[i] = np.random.uniform(-2, -1)
            elif categories[i] == 'moderate':
                wfa_zscore[i] = np.random.uniform(-3, -2)
                hfa_zscore[i] = np.random.uniform(-3, -2)
                wfh_zscore[i] = np.random.uniform(-3, -2)
            else:  # severe
                wfa_zscore[i] = np.random.uniform(-4, -3)
                hfa_zscore[i] = np.random.uniform(-4, -3)
                wfh_zscore[i] = np.random.uniform(-4, -3)
        
        # Generate weight and height based on z-scores
        weight_kg = np.zeros(n_samples)
        height_cm = np.zeros(n_samples)
        
        for i in range(n_samples):
            # Simplified WHO reference (actual values would come from WHO tables)
            mean_weight = 7 + (age_months[i] / 12) * 1.8
            sd_weight = 1.5
            weight_kg[i] = mean_weight + (wfa_zscore[i] * sd_weight)
            
            mean_height = 65 + (age_months[i] / 12) * 7
            sd_height = 4
            height_cm[i] = mean_height + (hfa_zscore[i] * sd_height)
        
        # Growth velocities correlated with nutritional status
        weight_velocity = np.where(
            wfa_zscore < -2, np.random.normal(0.05, 0.03, n_samples),
            np.where(wfa_zscore < -1, np.random.normal(0.15, 0.05, n_samples),
                    np.random.normal(0.25, 0.08, n_samples))
        )
        
        height_velocity = np.where(
            hfa_zscore < -2, np.random.normal(0.3, 0.1, n_samples),
            np.where(hfa_zscore < -1, np.random.normal(0.5, 0.15, n_samples),
                    np.random.normal(0.7, 0.2, n_samples))
        )
        
        # Diet features correlated with nutritional status
        meals_per_day = np.where(
            wfa_zscore < -2, np.random.randint(1, 3, n_samples),
            np.where(wfa_zscore < -1, np.random.randint(2, 4, n_samples),
                    np.random.randint(3, 6, n_samples))
        )
        
        milk_intake = np.where(
            wfa_zscore < -2, np.random.randint(100, 400, n_samples),
            np.where(wfa_zscore < -1, np.random.randint(300, 600, n_samples),
                    np.random.randint(400, 800, n_samples))
        )
        
        protein_servings = np.where(
            wfa_zscore < -2, np.random.randint(0, 2, n_samples),
            np.where(wfa_zscore < -1, np.random.randint(1, 3, n_samples),
                    np.random.randint(2, 5, n_samples))
        )
        
        veg_servings = np.where(
            wfa_zscore < -2, np.random.randint(0, 2, n_samples),
            np.where(wfa_zscore < -1, np.random.randint(1, 3, n_samples),
                    np.random.randint(2, 5, n_samples))
        )
        
        # Health features correlated with nutritional status
        illness_days = np.where(
            wfa_zscore < -2, np.random.poisson(8, n_samples),
            np.where(wfa_zscore < -1, np.random.poisson(4, n_samples),
                    np.random.poisson(1, n_samples))
        )
        
        diarrhea = np.where(
            wfa_zscore < -2, np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
            np.where(wfa_zscore < -1, np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
                    np.random.choice([0, 1], n_samples, p=[0.9, 0.1]))
        )
        
        fever = np.where(
            wfa_zscore < -2, np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            np.where(wfa_zscore < -1, np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
                    np.random.choice([0, 1], n_samples, p=[0.95, 0.05]))
        )
        
        # Combine features
        X = np.column_stack([
            age_months, weight_kg, height_cm, gender,
            wfa_zscore, hfa_zscore, wfh_zscore,
            weight_velocity, height_velocity,
            meals_per_day, milk_intake, protein_servings, veg_servings,
            illness_days, diarrhea, fever
        ])
        
        # Generate labels using WHO cutoffs (< -2 SD for current malnutrition)
        # But predict risk if approaching threshold (-1.5 to -2) OR poor dietary/health indicators
        y_underweight = (
            (wfa_zscore < -2.0) |  # WHO cutoff for underweight
            ((wfa_zscore < -1.5) & ((meals_per_day < 3) | (weight_velocity < 0.1))) |
            ((wfa_zscore < -1.0) & (illness_days > 7))
        ).astype(int)
        
        y_stunting = (
            (hfa_zscore < -2.0) |  # WHO cutoff for stunting
            ((hfa_zscore < -1.5) & ((protein_servings < 2) | (height_velocity < 0.4))) |
            ((hfa_zscore < -1.0) & (meals_per_day < 2))
        ).astype(int)
        
        y_wasting = (
            (wfh_zscore < -2.0) |  # WHO cutoff for wasting
            ((wfh_zscore < -1.5) & ((illness_days > 5) | (weight_velocity < 0.05))) |
            ((wfh_zscore < -1.0) & (diarrhea == 1) & (illness_days > 3))
        ).astype(int)
        
        return X, y_underweight, y_stunting, y_wasting


# Global predictor instance (will be created on first use)
_predictor_instance = None


def get_predictor(force_reload=False):
    """
    Get the malnutrition predictor instance
    
    Args:
        force_reload: If True, recreates the predictor (useful after retraining)
    """
    global _predictor_instance
    
    if _predictor_instance is None or force_reload:
        _predictor_instance = MalnutritionPredictor()
    
    return _predictor_instance
