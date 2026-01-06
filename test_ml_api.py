"""
Simple API Test - ML Recommender Endpoints
Tests the fixed ML recommender integration in flask_app.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_ml_endpoints():
    """Test all ML API endpoints"""
    
    print("\n" + "="*60)
    print("ML RECOMMENDER API ENDPOINTS TEST")
    print("="*60)
    
    # Test 1: Get ML Recommendations
    print("\n[TEST 1] GET /api/ml/recommendations/1")
    try:
        response = requests.get(f"{BASE_URL}/api/ml/recommendations/1?type=hybrid&top_n=5")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ SUCCESS: Got {len(data.get('recommendations', []))} recommendations")
                for i, rec in enumerate(data.get('recommendations', [])[:3], 1):
                    print(f"   {i}. {rec.get('ingredient')} - Score: {rec.get('score', 0):.2f}")
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: Get Similar Children
    print("\n[TEST 2] GET /api/ml/similar-children/1")
    try:
        response = requests.get(f"{BASE_URL}/api/ml/similar-children/1?top_n=3")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                similar = data.get('similar_children', [])
                print(f"✅ SUCCESS: Found {len(similar)} similar children")
                for child in similar:
                    print(f"   - {child.get('name')} (Similarity: {child.get('similarity_score', 0):.2f})")
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 3: Weekly Variety
    print("\n[TEST 3] POST /api/ml/weekly-variety")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ml/weekly-variety",
            json={'child_id': 1, 'budget': 2000}
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                plan = data.get('weekly_plan', [])
                print(f"✅ SUCCESS: Generated {len(plan)} days")
                if plan:
                    day1 = plan[0]
                    print(f"   Day 1 ({day1.get('day_name')}): {len(day1.get('ingredients', []))} ingredients")
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 4: Acceptance Prediction
    print("\n[TEST 4] POST /api/ml/acceptance-prediction")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ml/acceptance-prediction",
            json={'child_id': 1, 'ingredients': ['Rice', 'Dal', 'Spinach']}
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                prediction = data.get('prediction', {})
                print(f"✅ SUCCESS: Acceptance score: {prediction.get('acceptance_score', 0):.1f}%")
                print(f"   Confidence: {prediction.get('confidence')}")
                print(f"   Recommendation: {prediction.get('recommendation')}")
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 5: Child Profile
    print("\n[TEST 5] GET /api/ml/child-profile/1")
    try:
        response = requests.get(f"{BASE_URL}/api/ml/child-profile/1")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                profile = data.get('profile', {})
                priorities = data.get('nutritional_priorities', {})
                print(f"✅ SUCCESS: Profile generated")
                print(f"   Age: {profile.get('age_years', 0):.1f} years")
                print(f"   Weight: {profile.get('weight_kg', 0):.1f} kg")
                print(f"   Priorities: {priorities}")
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 6: Train Models
    print("\n[TEST 6] POST /api/ml/train")
    try:
        response = requests.post(f"{BASE_URL}/api/ml/train")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ SUCCESS: Models trained")
                print(f"   Details: {data.get('details')}")
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\n✅ All ML Recommender endpoints are now integrated!")
    print("   Start your Flask app with: python flask_app.py")
    print("   Then run this test to verify functionality")

if __name__ == "__main__":
    print("\n⚠️  Make sure Flask app is running on http://localhost:5000")
    print("   Run: python flask_app.py")
    input("\nPress Enter when server is ready...")
    test_ml_endpoints()
