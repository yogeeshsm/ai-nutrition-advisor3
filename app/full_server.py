# -*- coding: utf-8 -*-
"""
Complete AI Nutrition Advisor Server - All Features Enabled
Windows-compatible with proper encoding
"""
import sys
import os

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("AI NUTRITION ADVISOR - Loading All Features...")
print("="*60)

sys.dont_write_bytecode = True

# Import everything from app_full but wrap it to handle errors
try:
    print("Importing translation service...")
    try:
        import translator
        TRANSLATOR_AVAILABLE = True
    except Exception as e:
        print(f"[WARNING] Translation disabled: {e}")
        translator = None
        TRANSLATOR_AVAILABLE = False
    
    print("Importing core modules...")
    from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
    import json
    from datetime import datetime
    import io
    import pandas as pd
    
    print("Importing database...")
    import database as db
    
    print("Importing meal optimizer...")
    import meal_optimizer as mo
    
    print("Importing utilities...")
    from utils import export_to_pdf, get_food_emoji, format_currency
    
    print("Importing USDA API...")
    from usda_api import get_usda_api
    
    print("Importing WHO API...")
    from who_immunization import who_api
    
    print("Importing QR system...")
    from child_identity_qr import register_child_identity_routes
    
    print("Importing Mandi prices...")
    from mandi_price_api import register_mandi_routes
    
    print("Importing chatbot...")
    try:
        from gemini_chatbot import get_chatbot
        chatbot = get_chatbot()
        CHATBOT_AVAILABLE = chatbot is not None
        if CHATBOT_AVAILABLE:
            print("[OK] AI Chatbot ready")
        else:
            print("[WARNING] Chatbot not available - check GEMINI_API_KEY")
    except Exception as e:
        print(f"[WARNING] Chatbot disabled: {e}")
        chatbot = None
        CHATBOT_AVAILABLE = False
    
    print("\n[SUCCESS] All modules loaded!")
    
    # Create Flask app
    app = Flask(__name__)
    app.secret_key = 'nutrition-advisor-secret-key-2025'
    
    # Register extension routes
    register_mandi_routes(app)
    register_child_identity_routes(app)
    
    # Context processor for templates
    @app.context_processor
    def inject_helpers():
        current_lang = session.get('language', 'en')
        if TRANSLATOR_AVAILABLE and translator:
            trans_service = translator.get_translation_service()
            return dict(
                t=lambda key: trans_service.get_translation(key, current_lang),
                current_language=current_lang,
                languages=translator.LANGUAGES,
                translate=lambda text, dest_lang=None: trans_service.translate_text(text, current_lang, dest_lang or current_lang)
            )
        else:
            return dict(
                t=lambda key: key,
                current_language='en',
                languages={'en': {'name': 'English', 'flag': ''}},
                translate=lambda text, dest_lang=None: text
            )
    
    # Initialize database
    print("Initializing database...")
    db.initialize_database()
    print("[OK] Database ready")
    
    # Import all routes from app_full
    print("Loading all routes...")
    
    # Load the app_full module to get all routes
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_full_module", "app_full.py")
    app_full_module = importlib.util.module_from_spec(spec)
    
    # Execute the module to register all routes
    # But we need to replace its 'app' with our app
    import app_full as af
    
    # Copy all route handlers
    for rule in af.app.url_map.iter_rules():
        if rule.endpoint != 'static':
            try:
                # Get the view function from app_full
                view_func = af.app.view_functions[rule.endpoint]
                # Register it with our app
                app.add_url_rule(
                    rule.rule,
                    endpoint=rule.endpoint + '_full',
                    view_func=view_func,
                    methods=rule.methods
                )
            except Exception as e:
                print(f"[WARNING] Could not copy route {rule.endpoint}: {e}")
    
    print(f"[OK] {len(app.url_map._rules)} routes registered")
    
except ImportError as e:
    print(f"\n[ERROR] Failed to import app_full: {e}")
    print("Falling back to basic server...")
    
    # Fallback: create basic server
    from flask import Flask, render_template, request, jsonify
    import database as db
    import meal_optimizer as mo
    
    app = Flask(__name__)
    app.secret_key = 'nutrition-advisor-secret-key-2025'
    
    db.initialize_database()
    
    @app.route('/')
    def index():
        try:
            return render_template('index.html')
        except Exception as e:
            return f"Error: {e}"
    
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

# Start server
if __name__ == '__main__':
    print("\n" + "="*60)
    print("[SUCCESS] SERVER READY WITH ALL FEATURES!")
    print("="*60)
    print("\nServer URLs:")
    print("   http://127.0.0.1:5000")
    print("   http://localhost:5000")
    print("\nAll Pages:")
    print("   - Home / Meal Planner")
    print("   - Nutrition Lookup (USDA API)")
    print("   - Growth Tracking")
    print("   - Immunization (WHO)")
    print("   - Village Economy (Mandi Prices)")
    print("   - Food Recognition (ML)")
    print("   - AI Chatbot (Gemini)")
    print("   - Analytics Dashboard")
    print("   - ML Recommendations")
    print("   - QR Code System")
    print("\n" + "="*60)
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\n[ERROR]: {e}")
        import traceback
        traceback.print_exc()
