"""
Meal Optimization Engine
Uses linear programming to generate optimal meal plans within budget constraints
"""

import pandas as pd
import numpy as np
from pulp import *
import json
from datetime import datetime, timedelta

class MealOptimizer:
    def __init__(self, ingredients_df, budget, num_children, age_group="3-6 years"):
        self.ingredients_df = ingredients_df
        self.budget = budget
        self.num_children = num_children
        self.age_group = age_group
        
        # Nutritional requirements per child per day (based on ICMR guidelines)
        self.daily_requirements = self._get_daily_requirements()
        
        # Meal distribution (percentage of daily intake)
        self.meal_distribution = {
            'breakfast': 0.25,
            'lunch': 0.40,
            'snack': 0.10,
            'dinner': 0.25
        }
        
    def _get_daily_requirements(self):
        """Get daily nutritional requirements based on age group"""
        requirements = {
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
        return requirements.get(self.age_group, requirements["3-6 years"])
    
    def generate_meal_plan(self, selected_ingredients=None):
        """Generate optimized weekly meal plan"""
        if selected_ingredients:
            ingredients = self.ingredients_df[
                self.ingredients_df['name'].isin(selected_ingredients)
            ].copy()
        else:
            ingredients = self.ingredients_df.copy()
        
        if len(ingredients) == 0:
            raise ValueError("No ingredients available for meal planning")
        
        # Generate meal plan for 7 days
        weekly_plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        weekly_budget = self.budget
        daily_budget = weekly_budget / 7
        
        total_weekly_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'iron': 0,
            'calcium': 0
        }
        
        total_cost = 0
        
        for day in days:
            daily_plan = self._generate_daily_meal_plan(
                ingredients, 
                daily_budget,
                variety_seed=days.index(day)
            )
            weekly_plan[day] = daily_plan
            
            # Accumulate nutrition
            for nutrient in total_weekly_nutrition:
                total_weekly_nutrition[nutrient] += daily_plan['total_nutrition'].get(nutrient, 0)
            
            total_cost += daily_plan['total_cost']
        
        # Calculate nutrition score
        nutrition_score = self._calculate_nutrition_score(total_weekly_nutrition)
        
        return {
            'weekly_plan': weekly_plan,
            'total_cost': total_cost,
            'weekly_nutrition': total_weekly_nutrition,
            'nutrition_score': nutrition_score,
            'daily_requirements': self.daily_requirements
        }
    
    def _generate_daily_meal_plan(self, ingredients, daily_budget, variety_seed=0):
        """Generate optimized meal plan for one day"""
        np.random.seed(variety_seed)
        
        meals = ['breakfast', 'lunch', 'snack', 'dinner']
        daily_meals = {}
        daily_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'iron': 0,
            'calcium': 0
        }
        daily_cost = 0
        
        for meal in meals:
            meal_budget = daily_budget * self.meal_distribution[meal]
            meal_plan = self._generate_meal(
                ingredients, 
                meal, 
                meal_budget,
                variety_seed
            )
            daily_meals[meal] = meal_plan
            
            # Accumulate nutrition
            for nutrient in daily_nutrition:
                daily_nutrition[nutrient] += meal_plan['nutrition'].get(nutrient, 0)
            
            daily_cost += meal_plan['cost']
        
        return {
            'meals': daily_meals,
            'total_nutrition': daily_nutrition,
            'total_cost': daily_cost
        }
    
    def _generate_meal(self, ingredients, meal_type, meal_budget, variety_seed):
        """Generate a single meal using optimization"""
        # Meal-specific ingredient preferences
        meal_preferences = {
            'breakfast': ['Grains', 'Dairy', 'Fruits'],
            'lunch': ['Grains', 'Pulses', 'Vegetables', 'Dairy'],
            'snack': ['Fruits', 'Dairy', 'Grains'],
            'dinner': ['Grains', 'Pulses', 'Vegetables']
        }
        
        preferred_categories = meal_preferences.get(meal_type, ['Grains', 'Pulses', 'Vegetables'])
        
        # Filter ingredients by meal preference
        meal_ingredients = ingredients[
            ingredients['category'].isin(preferred_categories)
        ].copy()
        
        if len(meal_ingredients) == 0:
            meal_ingredients = ingredients.copy()
        
        # Add some randomness for variety
        if len(meal_ingredients) > 5:
            meal_ingredients = meal_ingredients.sample(
                min(12, len(meal_ingredients)), 
                random_state=variety_seed
            )
        
        # Create optimization problem
        prob = LpProblem(f"Meal_Optimization_{meal_type}", LpMaximize)
        
        # Decision variables: quantity in grams for each ingredient
        ingredient_vars = {}
        for idx, row in meal_ingredients.iterrows():
            ingredient_vars[row['name']] = LpVariable(
                f"qty_{row['name']}", 
                lowBound=0, 
                upBound=200  # Max 200g per ingredient per meal
            )
        
        # Objective: Maximize nutritional value (protein + fiber + iron + calcium)
        prob += lpSum([
            ingredient_vars[row['name']] * (
                row['protein_per_100g'] * 2 +  # Weight protein more
                row['fiber_per_100g'] +
                row['iron_per_100g'] * 0.5 +
                row['calcium_per_100g'] * 0.01
            ) / 100
            for idx, row in meal_ingredients.iterrows()
        ])
        
        # Constraint: Budget
        prob += lpSum([
            ingredient_vars[row['name']] * (row['cost_per_kg'] / 1000) * self.num_children
            for idx, row in meal_ingredients.iterrows()
        ]) <= meal_budget
        
        # Constraint: Minimum calories per meal per child
        target_calories = self.daily_requirements['calories'] * self.meal_distribution[meal_type]
        prob += lpSum([
            ingredient_vars[row['name']] * row['calories_per_100g'] / 100
            for idx, row in meal_ingredients.iterrows()
        ]) >= target_calories * 0.8  # At least 80% of target
        
        # Constraint: Maximum calories (don't overeat)
        prob += lpSum([
            ingredient_vars[row['name']] * row['calories_per_100g'] / 100
            for idx, row in meal_ingredients.iterrows()
        ]) <= target_calories * 1.3  # Max 130% of target
        
        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))
        
        # Extract results
        selected_items = []
        meal_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'iron': 0,
            'calcium': 0
        }
        meal_cost = 0
        
        for idx, row in meal_ingredients.iterrows():
            qty = ingredient_vars[row['name']].varValue
            if qty and qty > 5:  # Only include if quantity > 5g
                qty_per_child = round(qty, 1)
                cost = (row['cost_per_kg'] / 1000) * qty_per_child * self.num_children
                
                selected_items.append({
                    'ingredient': row['name'],
                    'category': row['category'],
                    'quantity_per_child_g': qty_per_child,
                    'total_quantity_g': qty_per_child * self.num_children,
                    'cost': round(cost, 2)
                })
                
                # Calculate nutrition (per child)
                factor = qty_per_child / 100
                meal_nutrition['calories'] += row['calories_per_100g'] * factor
                meal_nutrition['protein'] += row['protein_per_100g'] * factor
                meal_nutrition['carbs'] += row['carbs_per_100g'] * factor
                meal_nutrition['fat'] += row['fat_per_100g'] * factor
                meal_nutrition['fiber'] += row['fiber_per_100g'] * factor
                meal_nutrition['iron'] += row['iron_per_100g'] * factor
                meal_nutrition['calcium'] += row['calcium_per_100g'] * factor
                
                meal_cost += cost
        
        # Round nutrition values
        for key in meal_nutrition:
            meal_nutrition[key] = round(meal_nutrition[key], 2)
        
        return {
            'items': selected_items,
            'nutrition': meal_nutrition,
            'cost': round(meal_cost, 2)
        }
    
    def _calculate_nutrition_score(self, weekly_nutrition):
        """Calculate nutrition score (0-100) based on meeting daily requirements"""
        weekly_requirements = {
            nutrient: value * 7 for nutrient, value in self.daily_requirements.items()
        }
        
        scores = []
        for nutrient, requirement in weekly_requirements.items():
            if requirement > 0:
                achieved = weekly_nutrition.get(nutrient, 0)
                ratio = achieved / requirement
                # Score: 100 if 90-110% of requirement, lower if outside range
                if 0.9 <= ratio <= 1.1:
                    score = 100
                elif ratio < 0.9:
                    score = (ratio / 0.9) * 100
                else:  # ratio > 1.1
                    score = max(50, 100 - (ratio - 1.1) * 100)
                scores.append(min(100, score))
        
        return round(np.mean(scores), 1)

def format_meal_plan_for_display(meal_plan_result):
    """Format meal plan result for display"""
    weekly_plan = meal_plan_result['weekly_plan']
    
    formatted_plan = []
    for day, day_plan in weekly_plan.items():
        for meal_type, meal_data in day_plan['meals'].items():
            for item in meal_data['items']:
                formatted_plan.append({
                    'Day': day,
                    'Meal': meal_type.capitalize(),
                    'Ingredient': item['ingredient'],
                    'Category': item['category'],
                    'Qty/Child (g)': item['quantity_per_child_g'],
                    'Total Qty (g)': item['total_quantity_g'],
                    'Cost (₹)': item['cost']
                })
    
    return pd.DataFrame(formatted_plan)

def get_meal_plan_summary(meal_plan_result):
    """Get summary statistics of the meal plan"""
    return {
        'Total Weekly Cost': f"₹{meal_plan_result['total_cost']:.2f}",
        'Nutrition Score': f"{meal_plan_result['nutrition_score']}/100",
        'Weekly Calories': f"{meal_plan_result['weekly_nutrition']['calories']:.0f} kcal",
        'Weekly Protein': f"{meal_plan_result['weekly_nutrition']['protein']:.1f} g",
        'Weekly Carbs': f"{meal_plan_result['weekly_nutrition']['carbs']:.1f} g",
        'Weekly Fat': f"{meal_plan_result['weekly_nutrition']['fat']:.1f} g",
        'Weekly Fiber': f"{meal_plan_result['weekly_nutrition']['fiber']:.1f} g",
        'Weekly Iron': f"{meal_plan_result['weekly_nutrition']['iron']:.1f} mg",
        'Weekly Calcium': f"{meal_plan_result['weekly_nutrition']['calcium']:.1f} mg"
    }
