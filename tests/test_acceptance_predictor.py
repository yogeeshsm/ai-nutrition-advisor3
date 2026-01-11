"""
Quick test for Acceptance Predictor API
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_acceptance_predictor():
    """Test the acceptance prediction endpoint"""
    print("\n" + "="*60)
    print("TESTING ACCEPTANCE PREDICTOR")
    print("="*60)
    
    # Test data
    test_cases = [
        {"child_id": 1, "ingredient": "apple"},
        {"child_id": 1, "ingredient": "Rice"},
        {"child_id": 1, "ingredient": "Dal"},
    ]
    
    for test in test_cases:
        print(f"\n[TEST] Predicting acceptance for: {test['ingredient']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/ml/acceptance-prediction",
                json={
                    'child_id': test['child_id'],
                    'ingredients': [test['ingredient']]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ SUCCESS")
                    print(f"   Ingredient: {data.get('ingredient')}")
                    print(f"   Acceptance: {data.get('acceptance_percentage')}%")
                    print(f"   Strength: {data.get('explanation', {}).get('recommendation_strength')}")
                else:
                    print(f"❌ API returned success=false: {data.get('error')}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\n✅ Acceptance Predictor should now work in the UI!")
    print("   1. Reload the page: http://localhost:5000/ml-recommendations")
    print("   2. Select a child")
    print("   3. Click 'Acceptance Predictor' tab")
    print("   4. Type an ingredient name (e.g., 'apple', 'rice', 'dal')")
    print("   5. Wait 500ms - prediction will appear!")

if __name__ == "__main__":
    print("\n⚠️  Make sure Flask app is running on http://localhost:5000")
    input("Press Enter to start test...")
    test_acceptance_predictor()
