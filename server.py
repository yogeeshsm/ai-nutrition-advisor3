# -*- coding: utf-8 -*-
"""
Simple launcher - ASCII only for Windows compatibility
"""
import sys
import os

# Force UTF-8 encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("AI NUTRITION ADVISOR - Starting...")
print("="*60)

sys.dont_write_bytecode = True

print("Loading Flask...")
from flask import Flask, render_template, request, jsonify, session
print("Loading database...")
import database as db
print("Loading meal optimizer...")
import meal_optimizer as mo
print("Loading utilities...")
from utils import get_food_emoji, format_currency

print("\n[OK] Core modules loaded")

# Create app
app = Flask(__name__)
app.secret_key = 'nutrition-advisor-secret-key-2025'

print("Initializing database...")
try:
    db.initialize_database()
    print("[OK] Database ready")
except Exception as e:
    print(f"[WARNING] Database: {e}")

# Routes
@app.route('/test')
def test():
    return "SERVER IS WORKING! Go to <a href='/'>Home</a>"

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading homepage: {str(e)}<br><br>Try: <a href='/nutrition-lookup'>Nutrition Lookup</a> | <a href='/analytics'>Analytics</a>"

@app.route('/nutrition-lookup')
def nutrition_lookup():
    try:
        return render_template('nutrition_lookup.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/growth-tracking')
def growth_tracking():
    try:
        return render_template('growth_tracking.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/immunisation')
def immunisation():
    try:
        return render_template('immunisation.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/village-economy')
def village_economy():
    try:
        return render_template('village_economy.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/food-recognition')
def food_recognition():
    try:
        return render_template('food_recognition.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/chatbot')
def chatbot_page():
    try:
        return render_template('chatbot.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/analytics')
def analytics():
    try:
        return render_template('analytics.html')
    except Exception as e:
        return f"Error: {e}"

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        return f"Error: {e}"

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
    print("\n" + "="*60)
    print("[SUCCESS] SERVER READY!")
    print("="*60)
    print("\nOpen in your browser:")
    print("   http://127.0.0.1:5000")
    print("   http://localhost:5000")
    print("\nAvailable Pages:")
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
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
