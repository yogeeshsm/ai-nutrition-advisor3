"""
Stable server runner using Flask development server
Since waitress has issues in VS Code terminals, use Flask directly
"""
import os
import sys

os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("Loading application...")
from flask_app import app

if __name__ == "__main__":
    print("="*60)
    print("🍎 AI NUTRITION ADVISOR - SERVER READY")
    print("="*60)
    print("📍 Open in browser: http://127.0.0.1:5000")
    print("📍 Press Ctrl+C to stop server")
    print("="*60)
    
    try:
        # Use Flask development server directly - more reliable in VS Code
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=False,  # No auto-reload
            threaded=True,  # Handle concurrent requests
            use_reloader=False  # Don't restart on file changes
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


