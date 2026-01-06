"""Test if flask app is valid"""
import sys

print("1. Importing flask_app...")
try:
    from flask_app import app
    print("2. App imported successfully")
    print(f"3. App type: {type(app)}")
    print(f"4. App name: {app.name}")
    print(f"5. Number of routes: {len(app.url_map._rules)}")
    print("6. Sample routes:")
    for rule in list(app.url_map.iter_rules())[:10]:
        print(f"   - {rule}")
    
    print("\n7. Testing app.test_client()...")
    with app.test_client() as client:
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        print(f"   Response length: {len(response.data)} bytes")
    
    print("\n✅ App is valid and working!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
