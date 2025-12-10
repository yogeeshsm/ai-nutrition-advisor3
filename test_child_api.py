from flask_app import app
import json

with app.test_client() as client:
    response = client.get('/api/get-children')
    data = json.loads(response.data)
    
    if data['success'] and data['children']:
        first_child = data['children'][0]
        print("First child data:")
        for key, value in first_child.items():
            print(f"  {key}: {value}")
        
        # Check for required fields
        required = ['age_years', 'weight_kg']
        missing = [f for f in required if f not in first_child]
        
        if missing:
            print(f"\n⚠️  Missing fields: {missing}")
        else:
            print("\n✅ All required fields present!")
