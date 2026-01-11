from ml_recommender import MealRecommendationSystem
import traceback

print('\n🔍 Debugging build_child_feature_matrix...\n')

try:
    recommender = MealRecommendationSystem()
    
    print('Building feature matrix...')
    result = recommender.build_child_feature_matrix()
    
    if result is not None:
        print(f'\n✓ Feature matrix built successfully!')
        print(f'   Shape: {result.shape}')
        print(f'   Children: {list(result.index)}')
        print(f'\n   Columns: {list(result.columns)}')
        print(f'\n   Sample data:')
        print(result.head())
    else:
        print('\n❌ Feature matrix is None!')
        
except Exception as e:
    print(f'\n❌ Error occurred: {e}')
    traceback.print_exc()
