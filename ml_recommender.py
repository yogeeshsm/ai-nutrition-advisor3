"""
ML-Based Meal Recommendation System
Provides personalized meal recommendations using:
1. Collaborative Filtering - Based on similar children's preferences
2. Content-Based Filtering - Based on nutritional requirements
3. Hybrid Approach - Combined recommendations
"""

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import sqlite3
from datetime import datetime, timedelta
import json

class MealRecommendationSystem:
    """
    Hybrid Recommendation System combining collaborative and content-based filtering
    """
    
    def __init__(self, db_path='nutrition_advisor.db'):
        self.db_path = db_path
        self.scaler = StandardScaler()
        self.collaborative_model = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.content_model = NearestNeighbors(n_neighbors=10, metric='cosine')
        self.svd_model = TruncatedSVD(n_components=10)
        self.child_profiles = None
        self.meal_features = None
        self.ingredient_features = None
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # ==================== DATA PREPARATION ====================
    
    def prepare_child_profile(self, child_id):
        """
        Create comprehensive child profile for recommendations
        Returns: Dictionary with child features
        """
        conn = self.get_connection()
        
        # Get child basic info
        child_query = """
            SELECT id, name, date_of_birth, gender, village, health_notes
            FROM children WHERE id = ?
        """
        child_data = pd.read_sql_query(child_query, conn, params=(child_id,))
        
        if child_data.empty:
            conn.close()
            return None
        
        # Get latest growth measurement for weight/height
        growth_latest_query = """
            SELECT weight_kg, height_cm, bmi
            FROM growth_tracking WHERE child_id = ?
            ORDER BY measurement_date DESC LIMIT 1
        """
        growth_latest = pd.read_sql_query(growth_latest_query, conn, params=(child_id,))
        
        # Calculate age from date_of_birth
        from datetime import datetime
        dob = pd.to_datetime(child_data['date_of_birth'].iloc[0])
        age_years = (datetime.now() - dob).days / 365.25
        
        # Get weight and height from latest growth measurement or use defaults
        if not growth_latest.empty:
            weight_kg = growth_latest['weight_kg'].iloc[0]
            height_cm = growth_latest['height_cm'].iloc[0]
        else:
            weight_kg = 15.0  # default
            height_cm = 85.0  # default
        
        # Get child's meal history
        # Note: meal_plans table doesn't have child_id, so we'll use limited data
        meal_history_query = """
            SELECT id, created_at, total_cost, nutrition_score
            FROM meal_plans
            ORDER BY created_at DESC LIMIT 20
        """
        meal_history = pd.read_sql_query(meal_history_query, conn)
        
        # Get growth measurements
        growth_query = """
            SELECT weight_kg, height_cm, bmi, measurement_date
            FROM growth_tracking WHERE child_id = ?
            ORDER BY measurement_date DESC LIMIT 5
        """
        growth_data = pd.read_sql_query(growth_query, conn, params=(child_id,))
        
        conn.close()
        
        # Calculate derived features
        profile = {
            'child_id': child_id,
            'age_years': age_years,
            'weight_kg': weight_kg,
            'height_cm': height_cm,
            'gender': 1 if child_data['gender'].iloc[0] == 'M' else 0,
            'village': child_data['village'].iloc[0] if child_data['village'].iloc[0] else 'Unknown',
            'has_health_conditions': 1 if (child_data['health_notes'].iloc[0] and len(str(child_data['health_notes'].iloc[0])) > 0) else 0,
            'meal_plan_count': len(meal_history),
            'avg_meal_cost': meal_history['total_cost'].mean() if not meal_history.empty else 0,
            'avg_nutrition_score': meal_history['nutrition_score'].mean() if not meal_history.empty else 0,
            'weight_trend': self._calculate_trend(growth_data, 'weight_kg') if not growth_data.empty else 0,
            'height_trend': self._calculate_trend(growth_data, 'height_cm') if not growth_data.empty else 0,
        }
        
        return profile
    
    def _calculate_trend(self, data, column):
        """Calculate growth trend (positive = gaining, negative = losing)"""
        if len(data) < 2:
            return 0
        values = data[column].values
        return (values[0] - values[-1]) / len(values)
    
    def build_child_feature_matrix(self):
        """Build feature matrix for all children for collaborative filtering"""
        conn = self.get_connection()
        
        # Get all children
        children_query = """
            SELECT id
            FROM children
        """
        children_df = pd.read_sql_query(children_query, conn)
        conn.close()
        
        if children_df.empty:
            return None
        
        # Create feature matrix
        features = []
        child_ids = []
        
        for _, child in children_df.iterrows():
            profile = self.prepare_child_profile(child['id'])
            if profile:
                child_ids.append(child['id'])
                features.append([
                    profile['age_years'],
                    profile['weight_kg'],
                    profile['height_cm'],
                    profile['gender'],
                    profile['has_health_conditions'],
                    profile['avg_meal_cost'],
                    profile['avg_nutrition_score'],
                    profile['weight_trend'],
                    profile['height_trend']
                ])
        
        if not features:
            return None
        
        feature_matrix = np.array(features)
        # Normalize features
        feature_matrix_scaled = self.scaler.fit_transform(feature_matrix)
        
        self.child_profiles = pd.DataFrame(
            feature_matrix_scaled,
            columns=['age', 'weight', 'height', 'gender', 'health_conditions', 
                    'avg_cost', 'nutrition_score', 'weight_trend', 'height_trend'],
            index=child_ids
        )
        
        return self.child_profiles
    
    def build_ingredient_feature_matrix(self):
        """Build feature matrix for ingredients (content-based filtering)"""
        conn = self.get_connection()
        
        ingredients_query = """
            SELECT id, name, category, cost_per_kg, protein_per_100g, 
                   carbs_per_100g, fat_per_100g, calories_per_100g,
                   fiber_per_100g, iron_per_100g, calcium_per_100g
            FROM ingredients
        """
        ingredients_df = pd.read_sql_query(ingredients_query, conn)
        conn.close()
        
        if ingredients_df.empty:
            return None
        
        # Create feature matrix
        feature_columns = ['cost_per_kg', 'protein_per_100g', 'carbs_per_100g', 
                          'fat_per_100g', 'calories_per_100g', 'fiber_per_100g',
                          'iron_per_100g', 'calcium_per_100g']
        
        features = ingredients_df[feature_columns].fillna(0)
        features_scaled = self.scaler.fit_transform(features)
        
        self.ingredient_features = pd.DataFrame(
            features_scaled,
            columns=feature_columns,
            index=ingredients_df['id']
        )
        self.ingredient_features['name'] = ingredients_df['name'].values
        self.ingredient_features['category'] = ingredients_df['category'].values
        
        return self.ingredient_features
    
    # ==================== COLLABORATIVE FILTERING ====================
    
    def train_collaborative_model(self):
        """Train collaborative filtering model using child similarity"""
        if self.child_profiles is None:
            self.build_child_feature_matrix()
        
        if self.child_profiles is None or len(self.child_profiles) < 2:
            return False
        
        # Fit nearest neighbors model
        self.collaborative_model.fit(self.child_profiles.values)
        return True
    
    def find_similar_children(self, child_id, n_neighbors=5):
        """
        Find children similar to the given child
        Returns: List of (child_id, similarity_score) tuples
        """
        if self.child_profiles is None or child_id not in self.child_profiles.index:
            return []
        
        child_features = self.child_profiles.loc[child_id].values.reshape(1, -1)
        distances, indices = self.collaborative_model.kneighbors(child_features, n_neighbors=n_neighbors+1)
        
        similar_children = []
        for i, idx in enumerate(indices[0][1:]):  # Skip first (self)
            similar_child_id = self.child_profiles.index[idx]
            similarity = 1 - distances[0][i+1]  # Convert distance to similarity
            similar_children.append((similar_child_id, similarity))
        
        return similar_children
    
    def get_collaborative_recommendations(self, child_id, top_n=10):
        """
        Get meal recommendations based on what similar children ate
        """
        similar_children = self.find_similar_children(child_id, n_neighbors=5)
        
        if not similar_children:
            return []
        
        conn = self.get_connection()
        
        # Get successful meal plans from similar children
        similar_child_ids = [str(child[0]) for child in similar_children]
        placeholders = ','.join(['?' for _ in similar_child_ids])
        
        query = f"""
            SELECT mp.ingredients, mp.nutrition_score, mp.total_cost,
                   c.id as child_id
            FROM meal_plans mp
            JOIN children c ON mp.child_id = c.id
            WHERE c.id IN ({placeholders})
            AND mp.nutrition_score >= 70
            ORDER BY mp.nutrition_score DESC, mp.created_at DESC
            LIMIT 50
        """
        
        recommendations = pd.read_sql_query(query, conn, params=similar_child_ids)
        conn.close()
        
        if recommendations.empty:
            return []
        
        # Parse ingredients and count popularity
        ingredient_scores = {}
        
        for _, row in recommendations.iterrows():
            if row['ingredients']:
                try:
                    ingredients = json.loads(row['ingredients'])
                    child_similarity = dict(similar_children).get(row['child_id'], 0.5)
                    
                    for ing_name, quantity in ingredients.items():
                        if ing_name not in ingredient_scores:
                            ingredient_scores[ing_name] = 0
                        # Weight by nutrition score and child similarity
                        ingredient_scores[ing_name] += row['nutrition_score'] * child_similarity
                except:
                    pass
        
        # Sort and return top recommendations
        sorted_ingredients = sorted(ingredient_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_ingredients[:top_n]
    
    # ==================== CONTENT-BASED FILTERING ====================
    
    def train_content_model(self):
        """Train content-based filtering model using ingredient features"""
        if self.ingredient_features is None:
            self.build_ingredient_feature_matrix()
        
        if self.ingredient_features is None or len(self.ingredient_features) < 2:
            return False
        
        # Use only numeric columns for model
        numeric_cols = self.ingredient_features.select_dtypes(include=[np.number]).columns
        self.content_model.fit(self.ingredient_features[numeric_cols].values)
        return True
    
    def get_content_based_recommendations(self, child_id, top_n=10):
        """
        Get ingredient recommendations based on child's nutritional needs
        """
        profile = self.prepare_child_profile(child_id)
        if not profile:
            return []
        
        # Determine nutritional priorities based on child profile
        priorities = self._determine_nutritional_priorities(profile)
        
        if self.ingredient_features is None:
            self.build_ingredient_feature_matrix()
        
        # Score ingredients based on priorities
        ingredient_scores = []
        
        for ing_id, ing_data in self.ingredient_features.iterrows():
            score = 0
            
            # High protein priority
            if priorities['protein'] == 'high':
                score += ing_data['protein_per_100g'] * 2
            
            # High iron priority (for anemia risk)
            if priorities['iron'] == 'high':
                score += ing_data['iron_per_100g'] * 3
            
            # High calcium priority (for bone growth)
            if priorities['calcium'] == 'high':
                score += ing_data['calcium_per_100g'] * 2
            
            # Calorie needs
            if priorities['calories'] == 'high':
                score += ing_data['calories_per_100g'] * 0.1
            elif priorities['calories'] == 'low':
                score -= ing_data['calories_per_100g'] * 0.05
            
            # Budget consideration
            score -= ing_data['cost_per_kg'] * 0.1
            
            ingredient_scores.append((ing_data['name'], score))
        
        # Sort and return top recommendations
        sorted_ingredients = sorted(ingredient_scores, key=lambda x: x[1], reverse=True)
        return sorted_ingredients[:top_n]
    
    def _determine_nutritional_priorities(self, profile):
        """
        Determine nutritional priorities based on child profile
        """
        priorities = {
            'protein': 'medium',
            'iron': 'medium',
            'calcium': 'medium',
            'calories': 'medium'
        }
        
        age = profile['age_years']
        weight = profile['weight_kg']
        height = profile['height_cm']
        
        # Calculate BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2) if height_m > 0 else 0
        
        # Age-based priorities
        if age < 2:
            priorities['protein'] = 'high'
            priorities['calcium'] = 'high'
            priorities['calories'] = 'high'
        elif age < 5:
            priorities['protein'] = 'high'
            priorities['iron'] = 'high'
            priorities['calcium'] = 'high'
        
        # Weight-based priorities
        if profile['weight_trend'] < -0.5:  # Losing weight
            priorities['calories'] = 'high'
            priorities['protein'] = 'high'
        
        # BMI-based priorities
        if bmi < 14 and age >= 2:  # Underweight
            priorities['calories'] = 'high'
            priorities['protein'] = 'high'
        elif bmi > 18 and age >= 2:  # Overweight
            priorities['calories'] = 'low'
        
        # Health conditions
        if profile['has_health_conditions']:
            priorities['iron'] = 'high'
            priorities['protein'] = 'high'
        
        return priorities
    
    # ==================== HYBRID RECOMMENDATIONS ====================
    
    def get_hybrid_recommendations(self, child_id, top_n=15):
        """
        Get hybrid recommendations combining collaborative and content-based filtering
        Returns: List of (ingredient_name, score, source) tuples
        """
        # Get both types of recommendations
        collab_recs = self.get_collaborative_recommendations(child_id, top_n=20)
        content_recs = self.get_content_based_recommendations(child_id, top_n=20)
        
        # Combine scores with weights
        combined_scores = {}
        
        # Add collaborative filtering recommendations (weight: 0.6)
        for ingredient, score in collab_recs:
            combined_scores[ingredient] = {
                'score': score * 0.6,
                'source': 'collaborative'
            }
        
        # Add content-based recommendations (weight: 0.4)
        for ingredient, score in content_recs:
            if ingredient in combined_scores:
                combined_scores[ingredient]['score'] += score * 0.4
                combined_scores[ingredient]['source'] = 'hybrid'
            else:
                combined_scores[ingredient] = {
                    'score': score * 0.4,
                    'source': 'content-based'
                }
        
        # Sort by combined score
        sorted_recommendations = sorted(
            combined_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        
        # Format results
        results = [
            (name, data['score'], data['source'])
            for name, data in sorted_recommendations[:top_n]
        ]
        
        return results
    
    # ==================== MEAL VARIETY OPTIMIZATION ====================
    
    def optimize_weekly_variety(self, child_id, days=7):
        """
        Optimize meal variety for a week using recommendations
        Ensures diverse ingredients and balanced nutrition across the week
        """
        recommendations = self.get_hybrid_recommendations(child_id, top_n=50)
        
        if not recommendations:
            return None
        
        conn = self.get_connection()
        
        # Get ingredient details
        ingredient_names = [rec[0] for rec in recommendations]
        placeholders = ','.join(['?' for _ in ingredient_names])
        
        query = f"""
            SELECT name, category, protein_per_100g, carbs_per_100g,
                   fat_per_100g, calories_per_100g, cost_per_kg
            FROM ingredients
            WHERE name IN ({placeholders})
        """
        
        ingredients_df = pd.read_sql_query(query, conn, params=ingredient_names)
        conn.close()
        
        # Create weekly meal plan with variety
        weekly_plan = []
        used_ingredients = set()
        category_count = {}
        
        for day in range(days):
            day_plan = {
                'day': day + 1,
                'ingredients': [],
                'total_cost': 0,
                'total_calories': 0,
                'total_protein': 0
            }
            
            # Select diverse ingredients for each day
            for rec_name, rec_score, rec_source in recommendations:
                ing_data = ingredients_df[ingredients_df['name'] == rec_name]
                
                if ing_data.empty:
                    continue
                
                ing = ing_data.iloc[0]
                category = ing['category']
                
                # Ensure variety - don't repeat ingredients too soon
                if rec_name in used_ingredients and len(day_plan['ingredients']) > 0:
                    continue
                
                # Limit ingredients per category per day
                if category_count.get(category, 0) >= 2:
                    continue
                
                # Add ingredient to day plan
                day_plan['ingredients'].append({
                    'name': rec_name,
                    'category': category,
                    'recommendation_score': rec_score,
                    'source': rec_source
                })
                
                used_ingredients.add(rec_name)
                category_count[category] = category_count.get(category, 0) + 1
                
                # Stop when we have enough ingredients for the day
                if len(day_plan['ingredients']) >= 8:
                    break
            
            # Reset category count for next day
            category_count = {}
            
            # Clear used ingredients every 3 days for variety
            if day % 3 == 2:
                used_ingredients.clear()
            
            weekly_plan.append(day_plan)
        
        return weekly_plan
    
    # ==================== INGREDIENT ACCEPTANCE PREDICTION ====================
    
    def predict_ingredient_acceptance(self, child_id, ingredient_name):
        """
        Predict whether a child will accept a particular ingredient
        Based on similar children's consumption patterns
        """
        similar_children = self.find_similar_children(child_id, n_neighbors=10)
        
        if not similar_children:
            return 0.5  # Neutral prediction
        
        conn = self.get_connection()
        
        # Get meal plans from similar children that included this ingredient
        acceptance_count = 0
        total_count = 0
        
        for similar_child_id, similarity in similar_children:
            query = """
                SELECT ingredients, nutrition_score
                FROM meal_plans
                WHERE child_id = ?
                AND nutrition_score >= 60
            """
            
            plans = pd.read_sql_query(query, conn, params=(similar_child_id,))
            
            for _, plan in plans.iterrows():
                if plan['ingredients']:
                    try:
                        ingredients = json.loads(plan['ingredients'])
                        total_count += 1
                        if ingredient_name in ingredients:
                            acceptance_count += similarity  # Weight by similarity
                    except:
                        pass
        
        conn.close()
        
        if total_count == 0:
            return 0.5
        
        acceptance_probability = acceptance_count / total_count
        return min(1.0, max(0.0, acceptance_probability))
    
    # ==================== TRAINING AND INITIALIZATION ====================
    
    def train_all_models(self):
        """Train all recommendation models"""
        print("Building child feature matrix...")
        self.build_child_feature_matrix()
        
        print("Building ingredient feature matrix...")
        self.build_ingredient_feature_matrix()
        
        print("Training collaborative filtering model...")
        collab_success = self.train_collaborative_model()
        
        print("Training content-based filtering model...")
        content_success = self.train_content_model()
        
        return collab_success and content_success
    
    def get_recommendation_explanation(self, child_id, ingredient_name):
        """
        Provide explanation for why an ingredient was recommended
        """
        profile = self.prepare_child_profile(child_id)
        priorities = self._determine_nutritional_priorities(profile)
        similar_children = self.find_similar_children(child_id, n_neighbors=3)
        acceptance = self.predict_ingredient_acceptance(child_id, ingredient_name)
        
        explanation = {
            'ingredient': ingredient_name,
            'nutritional_priorities': priorities,
            'similar_children_count': len(similar_children),
            'acceptance_probability': round(acceptance * 100, 1),
            'recommendation_strength': 'High' if acceptance > 0.7 else 'Medium' if acceptance > 0.4 else 'Low'
        }
        
        return explanation


# ==================== HELPER FUNCTIONS ====================

def initialize_recommender():
    """Initialize and train the recommendation system"""
    recommender = MealRecommendationSystem()
    success = recommender.train_all_models()
    
    if success:
        print("✅ Recommendation system initialized successfully!")
    else:
        print("⚠️ Warning: Insufficient data for full training. Some features may be limited.")
    
    return recommender


if __name__ == "__main__":
    # Test the recommendation system
    print("Initializing ML Recommendation System...")
    recommender = initialize_recommender()
    
    print("\nRecommendation System Ready!")
    print("Features available:")
    print("- Collaborative Filtering (similar children)")
    print("- Content-Based Filtering (nutritional needs)")
    print("- Hybrid Recommendations")
    print("- Weekly Meal Variety Optimization")
    print("- Ingredient Acceptance Prediction")
