import requests
import json

# Test malnutrition prediction API
url = "http://127.0.0.1:5000/api/predict-malnutrition/1"
data = {
    "meals_per_day": 3,
    "milk_intake_ml": 500,
    "protein_servings": 2,
    "vegetable_servings": 2,
    "illness_days_last_month": 0,
    "diarrhea_recent": False,
    "fever_recent": False
}

print("Testing Malnutrition Prediction API...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("\n" + "="*60)

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print("\nResponse:")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if result.get('success'):
        print("\n✅ API Test Successful!")
        pred = result['prediction']
        print(f"\nChild: {result['child']['name']}")
        print(f"Overall Risk: {pred['overall_risk'].upper()}")
        print(f"\nPredictions:")
        print(f"  Underweight: {pred['predictions']['underweight']['risk_level']} ({pred['predictions']['underweight']['probability']:.1%})")
        print(f"  Stunting: {pred['predictions']['stunting']['risk_level']} ({pred['predictions']['stunting']['probability']:.1%})")
        print(f"  Wasting: {pred['predictions']['wasting']['risk_level']} ({pred['predictions']['wasting']['probability']:.1%})")
        print(f"\nRecommendations: {len(pred['recommendations'])} items")
    else:
        print(f"\n❌ Error: {result.get('error')}")
        
except Exception as e:
    print(f"\n❌ Test Failed: {e}")
