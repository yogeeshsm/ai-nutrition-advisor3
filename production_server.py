"""
Production-ready launcher using Waitress WSGI server
This avoids Flask development server issues
"""

print("="*60)
print("AI NUTRITION ADVISOR")
print("Production Server with Waitress")
print("="*60)

# Import with progress
print("\nLoading modules...")
from flask import Flask, render_template, request, jsonify
print("✓ Flask loaded")

import database as db
print("✓ Database loaded")

import meal_optimizer as mo
print("✓ Meal optimizer loaded")

from utils import get_food_emoji, format_currency
print("✓ Utilities loaded")

# Create app
app = Flask(__name__)
app.secret_key = 'nutrition-advisor-secret-key-2025'

# Initialize database
print("\nInitializing database...")
try:
    db.initialize_database()
    print("✓ Database ready")
except Exception as e:
    print(f"⚠ Database warning: {e}")

# Define all routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nutrition-lookup')
def nutrition_lookup():
    return render_template('nutrition_lookup.html')

@app.route('/growth-tracking')
def growth_tracking():
    return render_template('growth_tracking.html')

@app.route('/immunisation')
def immunisation():
    return render_template('immunisation.html')

@app.route('/village-economy')
def village_economy():
    return render_template('village_economy.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/about')
def about():
    return render_template('about.html')

# API Routes
@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    try:
        ingredients = db.get_all_ingredients()
        return jsonify(ingredients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/children', methods=['GET'])
def get_children():
    try:
        children = db.get_all_children()
        return jsonify(children)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/children', methods=['POST'])
def add_child():
    try:
        data = request.json
        child_id = db.add_child(
            data['name'],
            data['age'],
            data['gender'],
            data.get('village', 'Unknown')
        )
        return jsonify({'id': child_id, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize-meal', methods=['POST'])
def optimize_meal():
    try:
        data = request.json
        result = mo.optimize_meal_plan(
            num_children=data.get('num_children', 1),
            budget=data.get('budget', 500),
            age_group=data.get('age_group', '3-6'),
            excluded_ingredients=data.get('excluded_ingredients', [])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/food-search', methods=['GET'])
def search_food():
    try:
        query = request.args.get('q', '')
        results = db.search_ingredients(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

print("\n✓ All routes configured")

# Start with Waitress
if __name__ == '__main__':
    try:
        from waitress import serve
        print("\n" + "="*60)
        print("SERVER STARTING WITH WAITRESS")
        print("="*60)
        print("\n📱 Access URLs:")
        print("   http://127.0.0.1:5000")
        print("   http://localhost:5000")
        print("   http://10.148.75.207:5000")
        print("\n⚡ Features Available:")
        print("   ✓ Nutrition Lookup")
        print("   ✓ Child Growth Tracking")
        print("   ✓ Immunization Schedules")
        print("   ✓ Village Economy")
        print("   ✓ Food Recognition")
        print("   ✓ Analytics")
        print("   ✓ Meal Optimization")
        print("\n" + "="*60)
        print("Server running... Press CTRL+C to stop")
        print("="*60 + "\n")
        
        # Start Waitress server (production-ready, no auto-reload issues)
        serve(app, host='0.0.0.0', port=5000, threads=6)
        
    except ImportError:
        print("\n⚠ Waitress not available, using Flask development server...")
        print("Install waitress for production: pip install waitress")
        print("\n" + "="*60)
        print("Starting Flask development server...")
        print("="*60 + "\n")
        
        # Fallback to Flask (without debug/reloader to avoid crashes)
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
