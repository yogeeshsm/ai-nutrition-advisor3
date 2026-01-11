"""Test ML Recommender with Peanuts directly"""
from ml_recommender import MealRecommendationSystem

print("Initializing ML Recommender...")
recommender = MealRecommendationSystem()

print("\nTesting Peanuts ingredient acceptance...")
child_id = 1
ingredient = "Peanuts"

acceptance_prob, found = recommender.predict_ingredient_acceptance(child_id, ingredient)

if found:
    print(f"✅ SUCCESS! '{ingredient}' found in database")
    print(f"   Acceptance Probability: {acceptance_prob*100:.1f}%")
    print(f"   Recommendation Strength: {'High' if acceptance_prob > 0.7 else 'Medium' if acceptance_prob > 0.4 else 'Low'}")
else:
    print(f"❌ '{ingredient}' not found in database")
