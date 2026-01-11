import requests
import json

url = "http://127.0.0.1:5000/api/get-children"
print(f"Testing {url}...")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Success! Found {len(data['children'])} children.")
            for child in data['children'][:3]: # Show first 3
                print(f"  - {child['name']} (ID: {child['id']}, Age: {child['age_years']}y, Weight: {child['weight_kg']}kg)")
        else:
            print(f"❌ API Error: {data.get('error')}")
    else:
        print(f"❌ HTTP Error: {response.text}")
        
except Exception as e:
    print(f"❌ Connection Failed: {e}")
