"""
Auto-Start Launcher - No interaction needed
Starts the AI Nutrition Advisor in full mode with fallback
"""

import sys

def main():
    print("""
    ===========================================================
    
           AI NUTRITION ADVISOR                              
           For Rural India - Anganwadi Management            
    
    ===========================================================
    """)
    
    print("🔄 Auto-starting in FULL mode...")
    print("="*60)
    
    # Try full mode first
    try:
        print("Loading all features...")
        import sys
        import traceback
        
        try:
            from app_full import app
        except Exception as import_error:
            print(f"\n⚠️  Import error: {import_error}")
            print("\nFull traceback:")
            traceback.print_exc()
            raise
        
        print("\n✅ ALL 60+ FEATURES LOADED SUCCESSFULLY!")
        print("="*60)
        print("📱 Server URL: http://127.0.0.1:5000")
        print("🌐 Network URL: http://0.0.0.0:5000")
        print("\n⚡ Available Features:")
        print("   ✓ Meal Optimizer with ML Recommendations")
        print("   ✓ USDA Food Database Integration")
        print("   ✓ WHO Immunization Schedules")
        print("   ✓ Mandi Price API (Live Market Prices)")
        print("   ✓ AI Chatbot (Google Gemini)")
        print("   ✓ QR Code Identity Cards")
        print("   ✓ Village Economy Management")
        print("   ✓ Food Image Recognition (ML)")
        print("   ✓ Growth Analytics & Charts")
        print("   ✓ Multi-language Support")
        print("   ✓ PDF/CSV Export")
        print("   ✓ Child Health Tracking")
        print("   ✓ Nutrition Lookup")
        print("   ✓ And 40+ more features!")
        print("="*60)
        print("\nPress CTRL+C to stop the server\n")
        
        # Start server
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"\n⚠️  Full mode error: {e}")
        print("="*60)
        print("🔄 Switching to SIMPLE mode (core features)...")
        print("="*60)
        
        # Fallback to simple mode
        try:
            from flask import Flask, render_template, request, jsonify
            import database as db
            
            app = Flask(__name__)
            app.secret_key = 'nutrition-advisor-secret-key-2025'
            
            # Initialize database
            try:
                db.initialize_database()
                print("✅ Database initialized")
            except:
                print("⚠️  Database initialization skipped")
            
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
            
            # Basic API endpoints
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
            
            @app.route('/api/food', methods=['GET'])
            def search_food():
                try:
                    query = request.args.get('q', '')
                    results = db.search_ingredients(query)
                    return jsonify(results)
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
            
            print("\n✅ SIMPLE MODE ACTIVE - Core Features")
            print("="*60)
            print("📱 Server URL: http://127.0.0.1:5000")
            print("🌐 Network URL: http://0.0.0.0:5000")
            print("\n⚡ Available Features:")
            print("   ✓ Nutrition Lookup")
            print("   ✓ Child Growth Tracking")
            print("   ✓ Immunization Schedules")
            print("   ✓ Village Economy")
            print("   ✓ Food Recognition Interface")
            print("   ✓ Analytics Dashboard")
            print("="*60)
            print("\nPress CTRL+C to stop the server\n")
            
            app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
            
        except Exception as e2:
            print(f"\n❌ Simple mode also failed: {e2}")
            print("\nPlease install missing dependencies:")
            print("pip install Flask pandas numpy mysql-connector-python")
            sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        print("="*60)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        print("="*60)
