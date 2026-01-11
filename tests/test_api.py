"""Test API endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_get_children():
    """Test GET /api/get-children endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/get-children", timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"\n{json.dumps(data, indent=2)}")
        
        if data.get('success') and data.get('children'):
            print(f"\n✅ Found {len(data['children'])} children:")
            for child in data['children']:
                print(f"   - ID {child['id']}: {child['name']} ({child['age']}y old)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Child Identity API")
    print("=" * 50)
    test_get_children()
