"""
Simple wrapper to run the Flask app
"""
import os
import sys
os.environ['FLASK_DEBUG'] = '0'  # Disable debug mode reloader

from flask_app import app

if __name__ == '__main__':
    print("="*60)
    print("Starting AI Nutrition Advisor...")
    print("="*60)
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: Server crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
