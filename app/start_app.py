"""
Quick Start Launcher for AI Nutrition Advisor
Handles import issues and provides fallback options
"""

import sys
import os

def check_dependencies():
    """Check if all required packages are installed"""
    required = {
        'flask': 'Flask',
        'pandas': 'pandas',
        'numpy': 'numpy',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    # Check MySQL separately (it's optional)
    try:
        import mysql.connector
    except ImportError:
        print("⚠️  MySQL connector not available (optional - will use SQLite)")
    
    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False
    
    print("✅ Core dependencies available")
    return True

def start_simple_server():
    """Start the simple server (most stable)"""
    print("\n" + "="*60)
    print("🚀 Starting AI Nutrition Advisor - Simple Mode")
    print("="*60)
    
    from flask import Flask, render_template, request, jsonify
    import database as db
    
    app = Flask(__name__)
    app.secret_key = 'nutrition-advisor-secret-key-2025'
    
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
    def chatbot():
        return render_template('chatbot.html')
    
    @app.route('/analytics')
    def analytics():
        return render_template('analytics.html')
    
    # API endpoints
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
    
    @app.route('/api/immunization/<int:child_id>')
    def get_immunization(child_id):
        try:
            records = db.get_immunization_records(child_id)
            return jsonify(records)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    print("\n✅ Server starting...")
    print("📱 Open in browser: http://127.0.0.1:5000")
    print("🌐 Network access: http://0.0.0.0:5000")
    print("\n⚡ Available features:")
    print("   - Nutrition Lookup")
    print("   - Child Growth Tracking")
    print("   - Immunization Schedules")
    print("   - Village Economy")
    print("   - Food Recognition (needs model training)")
    print("   - Analytics Dashboard")
    print("\n" + "="*60)
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")

def start_full_server():
    """Start the full server with all features"""
    print("\n" + "="*60)
    print("🚀 Starting AI Nutrition Advisor - Full Mode")
    print("="*60)
    print("Loading all 60+ features...")
    
    try:
        # Import the full app
        from app_full import app
        
        print("\n✅ Server starting with ALL features...")
        print("📱 Open in browser: http://127.0.0.1:5000")
        print("🌐 Network access: http://0.0.0.0:5000")
        print("\n⚡ Available features:")
        print("   - Meal Optimizer with ML")
        print("   - USDA Food Database")
        print("   - WHO Immunization")
        print("   - Mandi Price API")
        print("   - AI Chatbot (Gemini)")
        print("   - QR Code Identity Cards")
        print("   - Village Economy Management")
        print("   - Food Recognition (ML)")
        print("   - Growth Analytics")
        print("   - Multi-language Support")
        print("   - PDF/CSV Export")
        print("   - And 50+ more features!")
        print("\n" + "="*60)
        print("Press CTRL+C to stop the server")
        print("="*60 + "\n")
        
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except ImportError as e:
        print(f"\n❌ Full mode unavailable: {e}")
        print("Falling back to simple mode...\n")
        start_simple_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         AI NUTRITION ADVISOR                              ║
    ║         For Rural India - Anganwadi Management            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("\nSelect mode:")
    print("1. Simple Mode (fastest, core features)")
    print("2. Full Mode (all 60+ features)")
    print("3. Auto (try full, fallback to simple)")
    
    choice = input("\nEnter choice (1/2/3) [default: 3]: ").strip() or "3"
    
    if choice == "1":
        start_simple_server()
    elif choice == "2":
        start_full_server()
    else:  # Auto mode (default)
        print("\n🔄 Auto mode: Attempting full server...")
        start_full_server()
