"""Quick script to list all routes in app_full"""
import app_full

print("\n" + "="*70)
print("REGISTERED ROUTES IN APP_FULL.PY")
print("="*70 + "\n")

routes = []
for rule in app_full.app.url_map.iter_rules():
    if rule.endpoint != 'static':
        routes.append((rule.endpoint, rule.rule, ','.join(rule.methods - {'HEAD', 'OPTIONS'})))

routes.sort()

for endpoint, rule, methods in routes:
    print(f"  {endpoint:45s} {methods:15s} {rule}")

print(f"\n  Total routes: {len(routes)}\n")
