import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from ml_recommender import MealRecommendationSystem

print('\n🔍 Deep Debugging...\n')

recommender = MealRecommendationSystem()
conn = sqlite3.connect('nutrition_advisor.db')

children_query = "SELECT id FROM children"
children_df = pd.read_sql_query(children_query, conn)
conn.close()

print(f'✓ Found {len(children_df)} children in database')
print(f'   IDs: {list(children_df["id"])}')

features = []
child_ids = []
failed_profiles = []

for _, child in children_df.iterrows():
    child_id = child['id']
    print(f'\n  Processing child ID {child_id}...', end='')
    
    try:
        profile = recommender.prepare_child_profile(child_id)
        if profile:
            child_ids.append(child_id)
            feature_row = [
                profile['age_years'],
                profile['weight_kg'],
                profile['height_cm'],
                profile['gender'],
                profile['has_health_conditions'],
                profile['avg_meal_cost'],
                profile['avg_nutrition_score'],
                profile['weight_trend'],
                profile['height_trend']
            ]
            features.append(feature_row)
            print(' ✓')
        else:
            print(' ❌ Profile is None')
            failed_profiles.append(child_id)
    except Exception as e:
        print(f' ❌ Error: {e}')
        failed_profiles.append(child_id)

print(f'\n\nSummary:')
print(f'  Successful profiles: {len(features)}')
print(f'  Failed profiles: {len(failed_profiles)}')

if features:
    print(f'\n  Creating feature matrix...')
    feature_matrix = np.array(features)
    print(f'  ✓ Matrix shape: {feature_matrix.shape}')
    
    scaler = StandardScaler()
    feature_matrix_scaled = scaler.fit_transform(feature_matrix)
    print(f'  ✓ Scaled matrix shape: {feature_matrix_scaled.shape}')
    
    df = pd.DataFrame(
        feature_matrix_scaled,
        columns=['age', 'weight', 'height', 'gender', 'health_conditions', 
                'avg_cost', 'nutrition_score', 'weight_trend', 'height_trend'],
        index=child_ids
    )
    print(f'  ✓ DataFrame created with index: {list(df.index)}')
    print(f'\n  Sample data:')
    print(df.head(3))
else:
    print(f'\n  ❌ No features collected - cannot build matrix!')
