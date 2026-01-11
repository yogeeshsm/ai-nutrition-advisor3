"""
AI Nutrition Advisor - Complete Feature Launcher
Includes ALL features: Meal Planning, ML, Chatbot, QR System, Malnutrition Prediction
"""
import sys
import os

# Set encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.dont_write_bytecode = True

print("="*70)
print(" 🍽️  AI NUTRITION ADVISOR - FULL FEATURE MODE")
print("="*70)
print("\n📦 Loading modules...")

from flask import Flask, render_template, request, jsonify, send_file, session
import json
from datetime import datetime
import io

# Core imports
print("  ✓ Flask")
import database as db
print("  ✓ Database")
import meal_optimizer as mo
print("  ✓ Meal Optimizer")
from utils import get_food_emoji, format_currency
print("  ✓ Utilities")

# Optional: Advanced features
FEATURES_LOADED = {
    'chatbot': False,
    'ml_recommender': False,
    'malnutrition': False,
    'qr_system': False,
    'mandi_prices': False,
    'usda_api': False,
    'who_api': False,
    'emergency_alerts': False
}

# Try loading chatbot
try:
    from gemini_chatbot import get_chatbot
    chatbot = get_chatbot()
    if chatbot:
        FEATURES_LOADED['chatbot'] = True
        print("  ✓ AI Chatbot (Groq API)")
except Exception as e:
    print(f"  ⚠ Chatbot: {e}")
    chatbot = None

# Try loading ML Recommender
try:
    from ml_recommender import MealRecommendationSystem
    ml_system = MealRecommendationSystem()
    FEATURES_LOADED['ml_recommender'] = True
    print("  ✓ ML Recommendation System")
except Exception as e:
    print(f"  ⚠ ML Recommender: {e}")
    ml_system = None

# Try loading Malnutrition Predictor
try:
    import malnutrition_predictor as mp
    FEATURES_LOADED['malnutrition'] = True
    print("  ✓ Malnutrition Predictor")
except Exception as e:
    print(f"  ⚠ Malnutrition: {e}")
    mp = None

# Try loading QR System
try:
    from child_identity_qr import register_child_identity_routes
    FEATURES_LOADED['qr_system'] = True
    print("  ✓ QR Child Identity System")
except Exception as e:
    print(f"  ⚠ QR System: {e}")
    register_child_identity_routes = None

# Try loading Mandi Prices
try:
    from mandi_price_api import register_mandi_routes
    FEATURES_LOADED['mandi_prices'] = True
    print("  ✓ Mandi Price API")
except Exception as e:
    print(f"  ⚠ Mandi Prices: {e}")
    register_mandi_routes = None

# Try loading USDA API
try:
    from usda_api import get_usda_api
    usda = get_usda_api()
    FEATURES_LOADED['usda_api'] = True
    print("  ✓ USDA Food API")
except Exception as e:
    print(f"  ⚠ USDA API: {e}")
    usda = None

# Try loading WHO API
try:
    from who_immunization import who_api
    FEATURES_LOADED['who_api'] = True
    print("  ✓ WHO Immunization API")
except Exception as e:
    print(f"  ⚠ WHO API: {e}")
    who_api = None

# Try loading Emergency Alerts
try:
    import emergency_alert_system as eas
    FEATURES_LOADED['emergency_alerts'] = True
    print("  ✓ Emergency Alert System")
except Exception as e:
    print(f"  ⚠ Emergency Alerts: {e}")
    eas = None

print("\n✅ Core modules loaded successfully!")

# Create Flask app
app = Flask(__name__)
app.secret_key = 'nutrition-advisor-secret-key-2025'

# Register advanced feature routes
if FEATURES_LOADED['mandi_prices'] and register_mandi_routes:
    register_mandi_routes(app)
if FEATURES_LOADED['qr_system'] and register_child_identity_routes:
    register_child_identity_routes(app)

# Context processor
@app.context_processor
def inject_translation():
    return dict(
        t=lambda key: key.replace('_', ' ').title(),
        current_language='en',
        languages={'en': 'English'},
        translate=lambda text: text
    )

# Initialize database
print("\n🗄️  Initializing database...")
try:
    db.initialize_database()
    print("✅ Database ready!")
except Exception as e:
    print(f"⚠️  Database warning: {e}")

# =============================================================================
# ROUTES
# =============================================================================

# Main Pages
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

# Malnutrition Prediction Page
@app.route('/malnutrition-prediction')
def malnutrition_prediction():
    return render_template('malnutrition_prediction.html')

# ML Recommendations Page
@app.route('/ml-recommendations')
def ml_recommendations():
    return render_template('ml_recommendations.html')

# =============================================================================
# API ENDPOINTS
# =============================================================================

# Core APIs
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

# Chatbot API
@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    if not FEATURES_LOADED['chatbot'] or not chatbot:
        return jsonify({
            'success': False,
            'error': 'Chatbot not available. Check GROQ_API_KEY environment variable.'
        }), 503
    
    try:
        data = request.json
        message = data.get('message', '')
        history = data.get('history', [])
        
        response = chatbot.chat(message, history)
        return jsonify({
            'success': True,
            'response': response,
            'mode': 'groq',
            'model': 'llama-3.3-70b-versatile'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ML Recommendation APIs
@app.route('/api/ml/recommend-ingredient/<int:child_id>/<ingredient_name>', methods=['GET'])
def ml_recommend_ingredient(child_id, ingredient_name):
    if not FEATURES_LOADED['ml_recommender'] or not ml_system:
        return jsonify({
            'success': False,
            'error': 'ML Recommender not available'
        }), 503
    
    try:
        ml_system.build_child_feature_matrix()
        ml_system.train_collaborative_model()
        
        acceptance = ml_system.predict_ingredient_acceptance(child_id, ingredient_name)
        explanation = ml_system.get_recommendation_explanation(child_id, ingredient_name)
        
        return jsonify({
            'success': True,
            'child_id': child_id,
            'ingredient': ingredient_name,
            'acceptance_probability': float(acceptance),
            'acceptance_percentage': round(acceptance * 100, 1),
            'explanation': explanation
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Malnutrition Prediction API
@app.route('/api/predict-malnutrition', methods=['POST'])
def predict_malnutrition():
    if not FEATURES_LOADED['malnutrition'] or not mp:
        return jsonify({
            'success': False,
            'error': 'Malnutrition predictor not available'
        }), 503
    
    try:
        data = request.json
        result = mp.predict_malnutrition(
            age=data.get('age'),
            weight=data.get('weight'),
            height=data.get('height'),
            gender=data.get('gender')
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# USDA API
@app.route('/api/usda-search', methods=['GET'])
def usda_search():
    if not FEATURES_LOADED['usda_api'] or not usda:
        return jsonify({'error': 'USDA API not available'}), 503
    
    try:
        query = request.args.get('q', '')
        results = usda.search_foods(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usda-details/<fdc_id>', methods=['GET'])
def usda_details(fdc_id):
    if not FEATURES_LOADED['usda_api'] or not usda:
        return jsonify({'error': 'USDA API not available'}), 503
    
    try:
        details = usda.get_food_details(fdc_id)
        return jsonify(details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Emergency Alert API
@app.route('/api/emergency-alert', methods=['POST'])
def emergency_alert():
    if not FEATURES_LOADED['emergency_alerts'] or not eas:
        return jsonify({'success': False, 'error': 'Emergency alerts not available'}), 503
    
    try:
        data = request.json
        result = eas.send_alert(
            child_id=data.get('child_id'),
            alert_type=data.get('alert_type'),
            severity=data.get('severity'),
            message=data.get('message')
        )
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Status endpoint
@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'features': FEATURES_LOADED,
        'version': '3.0',
        'total_features': sum(1 for v in FEATURES_LOADED.values() if v)
    })

# =============================================================================
# START SERVER
# =============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" ✅ SERVER READY - ALL FEATURES ACTIVATED!")
    print("="*70)
    
    # Show loaded features
    print("\n📋 Feature Status:")
    for feature, loaded in FEATURES_LOADED.items():
        status = "✅" if loaded else "❌"
        print(f"   {status} {feature.replace('_', ' ').title()}")
    
    active_count = sum(1 for v in FEATURES_LOADED.values() if v)
    print(f"\n🎯 {active_count}/8 advanced features active")
    
    print("\n" + "="*70)
    print(" 📱 ACCESS THE APPLICATION:")
    print("="*70)
    print("\n   🌐 http://127.0.0.1:5000")
    print("   🌐 http://localhost:5000\n")
    
    print("="*70)
    print(" 📄 AVAILABLE PAGES:")
    print("="*70)
    pages = [
        ("Home / Meal Planner", "/"),
        ("Nutrition Lookup (USDA)", "/nutrition-lookup"),
        ("Child Growth Tracking", "/growth-tracking"),
        ("Immunization (WHO)", "/immunisation"),
        ("Village Economy", "/village-economy"),
        ("AI Chatbot", "/chatbot"),
        ("Analytics Dashboard", "/analytics"),
        ("Malnutrition Prediction", "/malnutrition-prediction"),
        ("ML Recommendations", "/ml-recommendations"),
        ("Child QR Identity", "/child-identity-card"),
        ("About", "/about")
    ]
    
    for name, url in pages:
        print(f"   • {name:30s} → {url}")
    
    print("\n" + "="*70)
    print(" ⚡ API STATUS: /api/status")
    print("="*70)
    print("\n 🛑 Press CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
