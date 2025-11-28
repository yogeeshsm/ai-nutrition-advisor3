"""
Server startup script with error handling
"""
import sys
import traceback

try:
    print("🚀 Starting AI Nutrition Advisor...")
    print("=" * 60)
    
    from flask_app import app
    import os
    
    print("✅ Flask app loaded successfully")
    print(f"✅ Registered routes: {len(app.url_map._rules)}")
    print("=" * 60)
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Starting server on http://127.0.0.1:{port}")
    print("   Press CTRL+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n👋 Server stopped by user")
    sys.exit(0)
    
except Exception as e:
    print("\n\n❌ ERROR STARTING SERVER:")
    print("=" * 60)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    print("=" * 60)
    print("\nFull Traceback:")
    traceback.print_exc()
    sys.exit(1)
