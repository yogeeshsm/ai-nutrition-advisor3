from ml_recommender import MealRecommendationSystem

print('\n🔍 Debugging prepare_child_profile...\n')

recommender = MealRecommendationSystem()

# Test with child ID 3
child_id = 3
print(f'Testing with Child ID: {child_id}\n')

profile = recommender.prepare_child_profile(child_id)

if profile:
    print('✓ Profile created successfully!')
    print('\nProfile data:')
    for key, value in profile.items():
        print(f'   {key}: {value}')
else:
    print('❌ Profile is None or empty!')
