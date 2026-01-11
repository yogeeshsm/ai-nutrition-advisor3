"""
Simple Flask runner that stays running
"""
import sys
import signal

print("Loading Flask app...")
from flask_app import app

def signal_handler(sig, frame):
    print('\n\nShutting down server...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*60)
    print("AI NUTRITION ADVISOR")
    print("="*60)
    print("Server URL: http://127.0.0.1:5000")
    print("Press CTRL+C to stop")
    print("="*60)
    print("\nStarting server...\n")
    
    try:
        # Use Flask's built-in server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

