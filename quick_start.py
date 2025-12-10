"""
Simple launcher - bypasses complex imports
"""
print("="*60)
print("AI NUTRITION ADVISOR - Starting...")
print("="*60)

import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Set environment to avoid import issues
import sys
sys.dont_write_bytecode = True

print("Loading Flask...")
from flask import Flask, render_template, request, jsonify, session
print("Loading database...")
import database as db
print("Loading meal optimizer...")
import meal_optimizer as mo
print("Loading utilities...")
from utils import get_food_emoji, format_currency

print("\n✅ Core modules loaded")

# Create app
app = Flask(__name__)
app.secret_key = 'nutrition-advisor-secret-key-2025'

print("Initializing database...")
try:
    db.initialize_database()
    print("✅ Database ready")
except Exception as e:
    print(f"⚠️  Database warning: {e}")

# Routes
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

@app.route('/food-recognition')
def food_recognition():
    return render_template('food_recognition.html')

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

# Start server
if __name__ == '__main__':
    try:
        print("\n" + "="*60)
        print("✅ SERVER READY!")
        print("="*60)
        print("\n📱 Open in your browser:")
        print("   http://127.0.0.1:5000")
        print("   http://localhost:5000")
        print("\n⚡ Available Pages:")
        print("   - Home (index)")
        print("   - Nutrition Lookup")
        print("   - Child Growth Tracking")
        print("   - Immunization Schedules")
        print("   - Village Economy")
        print("   - Food Recognition")
        print("   - Analytics")
        print("\n" + "="*60)
        print("Press CTRL+C to stop")
        print("="*60 + "\n")
        
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
