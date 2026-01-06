"""
Simple reliable server - Run this to start the application
"""
import os
import sys

# Set encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 50)
print("🍎 AI NUTRITION ADVISOR")
print("=" * 50)
print("Loading application...")

# Import the app
from flask_app import app

if __name__ == "__main__":
    print()
    print("✅ Server starting...")
    print("📍 URL: http://127.0.0.1:5000")
    print("📍 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Run with Flask development server (most reliable)
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )
