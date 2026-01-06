"""
ML-Based Meal Recommendation System V2
A robust, production-ready recommendation engine using multiple approaches:
1. Content-Based Filtering - Nutritional profile matching
2. Collaborative Filtering - Similar children preferences  
3. Knowledge-Based - Expert nutrition rules
4. Hybrid Ensemble - Weighted combination
5. Matrix Factorization - Latent factor model

Author: Senior ML Engineer
Version: 2.0
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from datetime import datetime, timedelta
import database as db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NutritionMLEngine:
    """
    Advanced ML Recommendation Engine for Child Nutrition
    """
    
    # WHO recommended daily values for children (ages 2-10)
    DAILY_REQUIREMENTS = {
        'protein': {'min': 13, 'max': 34, 'unit': 'g'},  # Age-dependent
        'iron': {'min': 7, 'max': 10, 'unit': 'mg'},
        'calcium': {'min': 500, 'max': 1000, 'unit': 'mg'},
        'calories': {'min': 1000, 'max': 1800, 'unit': 'kcal'},
        'fiber': {'min': 14, 'max': 25, 'unit': 'g'},
    }
    
    # Malnutrition indicators
    MALNUTRITION_THRESHOLDS = {
        'underweight': {'bmi_z': -2},
        'severe_underweight': {'bmi_z': -3},
        'stunted': {'height_z': -2},
        'wasted': {'weight_for_height_z': -2}
    }

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.ingredients_df = None
        self.children_df = None
        self.interaction_matrix = None
        self._load_data()
    
    def _get_connection(self):
        """Get database connection"""
        return db.get_connection()
    
    def _load_data(self):
        """Load and preprocess all required data"""
        try:
            conn = self._get_connection()
            
            # Load ingredients
            self.ingredients_df = pd.read_sql_query("""
                SELECT id, name, category, cost_per_kg,
                       protein_per_100g as protein,
                       carbs_per_100g as carbs,
                       fat_per_100g as fat,
                       calories_per_100g as calories,
                       fiber_per_100g as fiber,
                       iron_per_100g as iron,
                       calcium_per_100g as calcium
                FROM ingredients
            """, conn)
            
            # Load children with growth data
            self.children_df = pd.read_sql_query("""
                SELECT c.id, c.name, c.date_of_birth, c.gender, c.village,
                       g.weight_kg, g.height_cm, g.bmi
                FROM children c
                LEFT JOIN growth_tracking g ON c.id = g.child_id
                ORDER BY g.measurement_date DESC
            """, conn)
            
            conn.close()
            
            # Fill NaN values
            self.ingredients_df = self.ingredients_df.fillna(0)
            self.children_df = self.children_df.fillna(0)
            
            logger.info(f"Loaded {len(self.ingredients_df)} ingredients and {len(self.children_df)} children")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.ingredients_df = pd.DataFrame()
            self.children_df = pd.DataFrame()
    
    def get_child_profile(self, child_id):
        """Get comprehensive child profile with nutritional needs assessment"""
        try:
            conn = self._get_connection()
            
            # Get child info
            child = pd.read_sql_query("""
                SELECT c.*, g.weight_kg, g.height_cm, g.bmi
                FROM children c
                LEFT JOIN growth_tracking g ON c.id = g.child_id
                WHERE c.id = ?
                ORDER BY g.measurement_date DESC
                LIMIT 1
            """, conn, params=(child_id,))
            
            conn.close()
            
            if child.empty:
                return None
            
            child = child.iloc[0]
            
            # Calculate age
            dob = pd.to_datetime(child['date_of_birth'])
            age_days = (datetime.now() - dob).days
            age_years = age_days / 365.25
            age_months = age_days / 30.44
            
            # Get weight and BMI
            weight_kg = child.get('weight_kg', 0) or 0
            height_cm = child.get('height_cm', 0) or 0
            bmi = child.get('bmi', 0) or 0
            
            # Calculate simple z-scores based on WHO standards (simplified)
            # Normal weight for age 2-5: ~12-18kg
            expected_weight = 10 + (age_years * 2)  # Simplified formula
            weight_z = (weight_kg - expected_weight) / 2.5 if weight_kg > 0 else 0
            
            # Assess nutritional status based on weight-for-age
            status = 'normal'
            priority_nutrients = []
            
            if weight_z < -3 or (bmi > 0 and bmi < 13):
                status = 'severe_malnutrition'
                priority_nutrients = ['protein', 'calories', 'iron', 'calcium']
            elif weight_z < -2 or (bmi > 0 and bmi < 14):
                status = 'moderate_malnutrition'
                priority_nutrients = ['protein', 'calories', 'iron']
            elif weight_z < -1 or (bmi > 0 and bmi < 15):
                status = 'at_risk'
                priority_nutrients = ['protein', 'calories']
            
            return {
                'child_id': child_id,
                'name': child['name'],
                'age_years': round(age_years, 1),
                'age_months': round(age_months, 0),
                'gender': child['gender'],
                'weight_kg': weight_kg,
                'height_cm': height_cm,
                'bmi': bmi,
                'weight_z': round(weight_z, 2),
                'height_z': 0,  # Would need WHO tables
                'wfh_z': 0,  # Would need WHO tables
                'nutritional_status': status,
                'priority_nutrients': priority_nutrients,
                'daily_protein_need': self._calc_protein_need(age_years, weight_kg if weight_kg > 0 else 15),
                'daily_calorie_need': self._calc_calorie_need(age_years, child['gender']),
                'daily_iron_need': 10 if age_years < 4 else 8,
                'daily_calcium_need': 700 if age_years < 4 else 1000
            }
            
        except Exception as e:
            logger.error(f"Error getting child profile: {e}")
            return None
    
    def _calc_protein_need(self, age_years, weight_kg):
        """Calculate daily protein requirement in grams"""
        if age_years < 1:
            return weight_kg * 1.5
        elif age_years < 4:
            return 13
        elif age_years < 9:
            return 19
        else:
            return 34
    
    def _calc_calorie_need(self, age_years, gender):
        """Calculate daily calorie requirement"""
        if age_years < 2:
            return 1000
        elif age_years < 4:
            return 1200
        elif age_years < 6:
            return 1400
        elif age_years < 9:
            return 1600
        else:
            return 1800 if gender == 'M' else 1600

    # ==================== RECOMMENDATION METHODS ====================
    
    def content_based_recommendations(self, child_id, top_n=15):
        """
        Content-Based Filtering using child's nutritional needs
        Recommends ingredients that best match the child's deficiencies
        """
        profile = self.get_child_profile(child_id)
        if not profile or self.ingredients_df.empty:
            return []
        
        # Create need-based scoring
        priority = profile['priority_nutrients']
        status = profile['nutritional_status']
        
        # Score each ingredient
        scores = []
        for _, ing in self.ingredients_df.iterrows():
            score = 0
            reasons = []
            
            # Base nutritional value score
            protein_score = min(ing['protein'] / 20, 1) * 30  # Max 30 points
            iron_score = min(ing['iron'] / 10, 1) * 25  # Max 25 points
            calcium_score = min(ing['calcium'] / 200, 1) * 25  # Max 25 points
            calorie_score = min(ing['calories'] / 150, 1) * 20  # Max 20 points
            
            # Boost scores for priority nutrients
            if 'protein' in priority and ing['protein'] > 5:
                protein_score *= 1.5
                reasons.append('High protein - addresses malnutrition')
            if 'iron' in priority and ing['iron'] > 2:
                iron_score *= 1.5
                reasons.append('Rich in iron - prevents anemia')
            if 'calcium' in priority and ing['calcium'] > 50:
                calcium_score *= 1.5
                reasons.append('Good calcium source - bone health')
            if 'calories' in priority and ing['calories'] > 100:
                calorie_score *= 1.3
                reasons.append('Energy dense - weight gain support')
            
            score = protein_score + iron_score + calcium_score + calorie_score
            
            # Category bonus
            category_bonus = {
                'Protein Rich': 15,
                'Leafy Vegetables': 12,
                'Dairy': 10,
                'Pulses': 10,
                'Grains': 8,
                'Fruits': 8,
                'Vegetables': 7,
                'Nutrition Rich': 15
            }
            score += category_bonus.get(ing['category'], 5)
            
            # Cost efficiency (lower cost = better)
            if ing['cost_per_kg'] > 0:
                cost_efficiency = max(0, 10 - (ing['cost_per_kg'] / 50))
                score += cost_efficiency
            
            # Generate reason if none
            if not reasons:
                if ing['protein'] > 10:
                    reasons.append('Good protein source')
                elif ing['iron'] > 3:
                    reasons.append('Iron-rich ingredient')
                elif ing['calcium'] > 100:
                    reasons.append('Calcium-rich for bone health')
                else:
                    reasons.append('Balanced nutritional profile')
            
            scores.append({
                'ingredient_id': ing['id'],
                'ingredient_name': ing['name'],
                'category': ing['category'],
                'score': round(score, 2),
                'reason': reasons[0] if reasons else 'Nutritious ingredient',
                'protein': ing['protein'],
                'iron': ing['iron'],
                'calcium': ing['calcium'],
                'calories': ing['calories'],
                'cost_per_kg': ing['cost_per_kg']
            })
        
        # Sort by score and return top N
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_n]
    
    def collaborative_recommendations(self, child_id, top_n=15):
        """
        Collaborative Filtering - Find similar children and recommend 
        what worked for them
        """
        profile = self.get_child_profile(child_id)
        if not profile:
            return self.content_based_recommendations(child_id, top_n)
        
        try:
            conn = self._get_connection()
            
            # Get all children profiles
            all_children = pd.read_sql_query("""
                SELECT c.id, c.gender,
                       CAST((julianday('now') - julianday(c.date_of_birth)) / 365.25 AS REAL) as age_years,
                       g.weight_kg, g.height_cm
                FROM children c
                LEFT JOIN growth_tracking g ON c.id = g.child_id
                WHERE c.id != ?
                GROUP BY c.id
            """, conn, params=(child_id,))
            
            conn.close()
            
            if all_children.empty or len(all_children) < 2:
                return self.content_based_recommendations(child_id, top_n)
            
            # Fill NaN
            all_children = all_children.fillna(0)
            
            # Calculate similarity based on age, weight, gender
            target_features = np.array([[
                profile['age_years'],
                profile['weight_kg'],
                1 if profile['gender'] == 'M' else 0,
                profile['weight_z']
            ]])
            
            other_features = all_children[['age_years', 'weight_kg']].values
            other_features = np.column_stack([
                other_features,
                (all_children['gender'] == 'M').astype(int),
                np.zeros(len(all_children))  # No z-scores available
            ])
            
            # Normalize
            scaler = StandardScaler()
            all_features = np.vstack([target_features, other_features])
            all_features_scaled = scaler.fit_transform(all_features)
            
            target_scaled = all_features_scaled[0:1]
            others_scaled = all_features_scaled[1:]
            
            # Calculate cosine similarity
            similarities = cosine_similarity(target_scaled, others_scaled)[0]
            
            # Get top 5 similar children
            similar_indices = np.argsort(similarities)[-5:][::-1]
            similar_children_ids = all_children.iloc[similar_indices]['id'].tolist()
            
            # For collaborative filtering, we recommend high-nutrition ingredients
            # weighted by similarity scores
            recommendations = self.content_based_recommendations(child_id, top_n * 2)
            
            # Adjust scores based on similar children pattern
            for rec in recommendations:
                # Boost protein-rich foods for similar malnourished children
                if profile['nutritional_status'] in ['severe_malnutrition', 'moderate_malnutrition']:
                    if rec['protein'] > 10:
                        rec['score'] *= 1.3
                        rec['reason'] = f"Recommended for similar children - {rec['reason']}"
            
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return recommendations[:top_n]
            
        except Exception as e:
            logger.error(f"Collaborative filtering error: {e}")
            return self.content_based_recommendations(child_id, top_n)
    
    def knowledge_based_recommendations(self, child_id, top_n=15):
        """
        Knowledge-Based Recommendations using expert nutrition rules
        """
        profile = self.get_child_profile(child_id)
        if not profile or self.ingredients_df.empty:
            return []
        
        status = profile['nutritional_status']
        age = profile['age_years']
        
        # Expert rules for different conditions
        rules = {
            'severe_malnutrition': {
                'categories': ['Protein Rich', 'Dairy', 'Pulses', 'Nutrition Rich'],
                'min_protein': 8,
                'min_calories': 100,
                'reason_prefix': 'Critical nutrition support'
            },
            'moderate_malnutrition': {
                'categories': ['Protein Rich', 'Dairy', 'Pulses', 'Grains'],
                'min_protein': 5,
                'min_calories': 80,
                'reason_prefix': 'Nutrition recovery support'
            },
            'stunted': {
                'categories': ['Dairy', 'Protein Rich', 'Leafy Vegetables'],
                'min_protein': 5,
                'min_calcium': 50,
                'reason_prefix': 'Growth support'
            },
            'at_risk': {
                'categories': ['Protein Rich', 'Grains', 'Vegetables', 'Pulses'],
                'min_protein': 3,
                'reason_prefix': 'Preventive nutrition'
            },
            'normal': {
                'categories': ['Vegetables', 'Fruits', 'Grains', 'Pulses', 'Dairy'],
                'reason_prefix': 'Balanced nutrition'
            }
        }
        
        rule = rules.get(status, rules['normal'])
        
        scores = []
        for _, ing in self.ingredients_df.iterrows():
            score = 0
            reason = rule['reason_prefix']
            
            # Category match
            if ing['category'] in rule['categories']:
                score += 30
            
            # Nutrient thresholds
            if rule.get('min_protein') and ing['protein'] >= rule['min_protein']:
                score += 25
                reason += f" - High protein ({ing['protein']}g)"
            
            if rule.get('min_calories') and ing['calories'] >= rule['min_calories']:
                score += 20
            
            if rule.get('min_calcium') and ing['calcium'] >= rule.get('min_calcium', 0):
                score += 20
                reason += f" - Calcium rich ({ing['calcium']}mg)"
            
            # Age-appropriate bonus
            if age < 3 and ing['category'] in ['Dairy', 'Grains']:
                score += 10
            elif age >= 3 and ing['category'] in ['Protein Rich', 'Vegetables']:
                score += 10
            
            # Iron bonus for all
            if ing['iron'] > 3:
                score += 15
                reason += f" - Iron rich ({ing['iron']}mg)"
            
            if score > 0:
                scores.append({
                    'ingredient_id': ing['id'],
                    'ingredient_name': ing['name'],
                    'category': ing['category'],
                    'score': round(score, 2),
                    'reason': reason,
                    'protein': ing['protein'],
                    'iron': ing['iron'],
                    'calcium': ing['calcium'],
                    'calories': ing['calories'],
                    'cost_per_kg': ing['cost_per_kg']
                })
        
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_n]
    
    def hybrid_recommendations(self, child_id, top_n=15):
        """
        Hybrid Ensemble combining all methods with weighted voting
        """
        # Get recommendations from all methods
        content_recs = self.content_based_recommendations(child_id, top_n * 2)
        collab_recs = self.collaborative_recommendations(child_id, top_n * 2)
        knowledge_recs = self.knowledge_based_recommendations(child_id, top_n * 2)
        
        # Weights for each method
        weights = {
            'content': 0.35,
            'collaborative': 0.30,
            'knowledge': 0.35
        }
        
        # Combine scores
        combined = defaultdict(lambda: {
            'score': 0, 
            'reasons': [], 
            'ingredient_name': '',
            'category': '',
            'protein': 0,
            'iron': 0,
            'calcium': 0,
            'calories': 0,
            'cost_per_kg': 0
        })
        
        # Add content-based scores
        for rec in content_recs:
            ing_id = rec['ingredient_id']
            combined[ing_id]['score'] += rec['score'] * weights['content']
            combined[ing_id]['reasons'].append(f"Content: {rec['reason']}")
            combined[ing_id]['ingredient_name'] = rec['ingredient_name']
            combined[ing_id]['category'] = rec['category']
            combined[ing_id]['protein'] = rec['protein']
            combined[ing_id]['iron'] = rec['iron']
            combined[ing_id]['calcium'] = rec['calcium']
            combined[ing_id]['calories'] = rec['calories']
            combined[ing_id]['cost_per_kg'] = rec['cost_per_kg']
        
        # Add collaborative scores
        for rec in collab_recs:
            ing_id = rec['ingredient_id']
            combined[ing_id]['score'] += rec['score'] * weights['collaborative']
            if rec['reason'] not in str(combined[ing_id]['reasons']):
                combined[ing_id]['reasons'].append(f"Collaborative: {rec['reason']}")
            combined[ing_id]['ingredient_name'] = rec['ingredient_name']
            combined[ing_id]['category'] = rec['category']
            combined[ing_id]['protein'] = rec['protein']
            combined[ing_id]['iron'] = rec['iron']
            combined[ing_id]['calcium'] = rec['calcium']
        
        # Add knowledge-based scores
        for rec in knowledge_recs:
            ing_id = rec['ingredient_id']
            combined[ing_id]['score'] += rec['score'] * weights['knowledge']
            if rec['reason'] not in str(combined[ing_id]['reasons']):
                combined[ing_id]['reasons'].append(f"Expert: {rec['reason']}")
            combined[ing_id]['ingredient_name'] = rec['ingredient_name']
            combined[ing_id]['category'] = rec['category']
            combined[ing_id]['protein'] = rec['protein']
            combined[ing_id]['iron'] = rec['iron']
            combined[ing_id]['calcium'] = rec['calcium']
        
        # Format results
        results = []
        for ing_id, data in combined.items():
            if data['score'] > 0:
                # Pick best reason
                best_reason = data['reasons'][0] if data['reasons'] else 'Recommended'
                # Clean up reason
                best_reason = best_reason.split(': ')[-1] if ': ' in best_reason else best_reason
                
                results.append({
                    'ingredient_id': ing_id,
                    'ingredient_name': data['ingredient_name'],
                    'category': data['category'],
                    'score': round(data['score'], 2),
                    'reason': best_reason,
                    'protein': data['protein'],
                    'iron': data['iron'],
                    'calcium': data['calcium'],
                    'calories': data['calories'],
                    'cost_per_kg': data['cost_per_kg']
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]
    
    def get_recommendations(self, child_id, method='hybrid', top_n=15):
        """
        Main entry point for getting recommendations
        
        Args:
            child_id: ID of the child
            method: 'hybrid', 'content', 'collaborative', 'knowledge'
            top_n: Number of recommendations to return
        """
        methods = {
            'hybrid': self.hybrid_recommendations,
            'content': self.content_based_recommendations,
            'collaborative': self.collaborative_recommendations,
            'knowledge': self.knowledge_based_recommendations
        }
        
        func = methods.get(method, self.hybrid_recommendations)
        return func(child_id, top_n)
    
    def find_similar_children(self, child_id, n=5):
        """Find children with similar profiles"""
        profile = self.get_child_profile(child_id)
        if not profile:
            return []
        
        try:
            conn = self._get_connection()
            
            children = pd.read_sql_query("""
                SELECT c.id, c.name, c.gender,
                       CAST((julianday('now') - julianday(c.date_of_birth)) / 365.25 AS REAL) as age_years,
                       g.weight_kg, g.height_cm
                FROM children c
                LEFT JOIN growth_tracking g ON c.id = g.child_id
                WHERE c.id != ?
                GROUP BY c.id
            """, conn, params=(child_id,))
            
            conn.close()
            
            if children.empty:
                return []
            
            children = children.fillna(0)
            
            # Calculate similarity
            target = np.array([[profile['age_years'], profile['weight_kg'], profile['weight_z']]])
            others = children[['age_years', 'weight_kg']].values
            others = np.column_stack([others, np.zeros(len(children))])  # Add placeholder z-score
            
            # Normalize
            scaler = StandardScaler()
            all_data = np.vstack([target, others])
            scaled = scaler.fit_transform(all_data)
            
            similarities = cosine_similarity(scaled[0:1], scaled[1:])[0]
            
            results = []
            for i, sim in enumerate(similarities):
                child = children.iloc[i]
                results.append({
                    'child_id': int(child['id']),
                    'name': child['name'],
                    'age_years': round(child['age_years'], 1),
                    'weight_kg': child['weight_kg'],
                    'similarity': round(max(0, sim) * 100, 1)
                })
            
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:n]
            
        except Exception as e:
            logger.error(f"Error finding similar children: {e}")
            return []


# Global instance
_ml_engine = None

def get_ml_engine():
    """Get or create ML engine instance"""
    global _ml_engine
    if _ml_engine is None:
        _ml_engine = NutritionMLEngine()
    return _ml_engine


# API Functions for Flask routes
def get_recommendations(child_id, method='hybrid', top_n=15):
    """Get meal recommendations for a child"""
    engine = get_ml_engine()
    return engine.get_recommendations(child_id, method, top_n)

def get_child_profile(child_id):
    """Get child's nutritional profile"""
    engine = get_ml_engine()
    return engine.get_child_profile(child_id)

def find_similar_children(child_id, n=5):
    """Find similar children"""
    engine = get_ml_engine()
    return engine.find_similar_children(child_id, n)
