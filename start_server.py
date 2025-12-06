"""Start Flask server"""
import sys
import os

# Set UTF-8 encoding to avoid emoji errors
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app_full import app

if __name__ == "__main__":
    print("=" * 60)
    print("AI NUTRITION ADVISOR - ALL FEATURES + ML")
    print("=" * 60)
    print("Server: http://127.0.0.1:5000")
    print("Routes: 50+ endpoints active")
    print("ML Features: Collaborative + Content-Based + Hybrid")
    print("=" * 60)
    print("\nStarting Flask development server...")
    print("Press Ctrl+C to stop\n")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
