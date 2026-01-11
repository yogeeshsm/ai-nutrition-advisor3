"""List all Flask routes"""
from flask_app import app

print("\n" + "="*70)
print("REGISTERED FLASK ROUTES")
print("="*70)

routes = []
for rule in app.url_map.iter_rules():
    routes.append({
        'endpoint': rule.endpoint,
        'methods': ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
        'path': rule.rule
    })

# Sort by path
routes.sort(key=lambda x: x['path'])

# Filter malnutrition routes
malnutrition_routes = [r for r in routes if 'malnutrition' in r['path'].lower()]

if malnutrition_routes:
    print("\n🔍 Malnutrition Routes Found:")
    for route in malnutrition_routes:
        print(f"  {route['methods']:10} {route['path']}")
else:
    print("\n❌ No malnutrition routes found!")

print(f"\n📊 Total routes: {len(routes)}")
print("\nAll routes containing 'api':")
api_routes = [r for r in routes if '/api/' in r['path']]
for route in api_routes[:20]:  # Show first 20
    print(f"  {route['methods']:10} {route['path']}")

print("="*70)
