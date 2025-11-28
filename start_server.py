"""Start Flask server"""
from flask_app import app

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting AI Nutrition Advisor Server...")
    print("=" * 60)
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()
