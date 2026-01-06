import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

class TestRecommender:
    def __init__(self):
        self.db_path = 'nutrition_advisor.db'
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _calculate_trend(self, data, column):
        if len(data) < 2:
            return 0
        values = data[column].values
        return (values[0] - values[-1]) / len(values)
    
    def prepare_child_profile(self, child_id):
        conn = self.get_connection()
        
        child_query = "SELECT id, name, date_of_birth, gender, village, health_notes FROM children WHERE id = ?"
        child_data = pd.read_sql_query(child_query, conn, params=(child_id,))
        
        print(f'    Child data query returned {len(child_data)} rows')
        
        if child_data.empty:
            conn.close()
            print(f'    ❌ Child data is empty!')
            return None
        
        growth_latest_query = "SELECT weight_kg, height_cm, bmi FROM growth_tracking WHERE child_id = ? ORDER BY measurement_date DESC LIMIT 1"
        growth_latest = pd.read_sql_query(growth_latest_query, conn, params=(child_id,))
        
        dob = pd.to_datetime(child_data['date_of_birth'].iloc[0])
        age_years = (datetime.now() - dob).days / 365.25
        
        if not growth_latest.empty:
            weight_kg = growth_latest['weight_kg'].iloc[0]
            height_cm = growth_latest['height_cm'].iloc[0]
        else:
            weight_kg = 15.0
            height_cm = 85.0
        
        meal_history_query = "SELECT id, created_at, total_cost, nutrition_score FROM meal_plans ORDER BY created_at DESC LIMIT 20"
        meal_history = pd.read_sql_query(meal_history_query, conn)
        
        growth_query = "SELECT weight_kg, height_cm, bmi, measurement_date FROM growth_tracking WHERE child_id = ? ORDER BY measurement_date DESC LIMIT 5"
        growth_data = pd.read_sql_query(growth_query, conn, params=(child_id,))
        
        conn.close()
        
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
        
        print(f'    ✓ Profile created with {len(profile)} fields')
        return profile

print('\n🧪 Testing prepare_child_profile in isolation...\n')

rec = TestRecommender()

for child_id in [1, 2, 3]:
    print(f'Child ID {child_id}:')
    profile = rec.prepare_child_profile(child_id)
    if profile:
        print(f'  ✓ Success - age: {profile["age_years"]:.1f}')
    else:
        print(f'  ❌ Failed!')
    print()
