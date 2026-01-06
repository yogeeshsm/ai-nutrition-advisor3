"""
Test Acceptance Predictor API
"""
import requests
import json

# Test the acceptance prediction endpoint
url = "http://localhost:5000/api/ml/acceptance-prediction"

# Test with child ID 1 (Lakshmi Iyer) and ingredient "Peanut"
data = {
    "child_id": 1,
    "ingredients": ["Peanut"]
}

print("Testing Acceptance Prediction API...")
print(f"URL: {url}")
print(f"Request: {json.dumps(data, indent=2)}")
print()

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
