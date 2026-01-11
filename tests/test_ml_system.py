from ml_recommender import MealRecommendationSystem

print('\n🧪 Testing ML Recommender System...\n')

try:
    recommender = MealRecommendationSystem()
    print('✓ Recommender initialized')
    
    # Test with child ID 3 (Arjun Patil)
    child_id = 3
    print(f'\n📊 Testing for Child ID: {child_id}')
    
    # Build feature matrix
    print('\n1. Building child feature matrix...')
    recommender.build_child_feature_matrix()
    print(f'   ✓ Feature matrix shape: {recommender.child_profiles.shape if recommender.child_profiles is not None else "None"}')
    
    # Train collaborative model
    print('\n2. Training collaborative filtering model...')
    recommender.train_collaborative_model()
    print('   ✓ Model trained')
    
    # Find similar children
    print(f'\n3. Finding similar children to ID {child_id}...')
    similar = recommender.find_similar_children(child_id, n=5)
    
    if similar:
        print(f'   ✓ Found {len(similar)} similar children:')
        for sim_id, score in similar:
            print(f'      Child ID {sim_id}: Similarity = {score:.3f}')
    else:
        print('   ❌ No similar children found!')
        
except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()
