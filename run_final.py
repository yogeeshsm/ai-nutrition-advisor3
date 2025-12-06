import sys
import os
import time
from waitress import serve

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

print("="*60)
print("STARTING AI NUTRITION ADVISOR (FULL VERSION)")
print("="*60)

try:
    print("1. Importing Flask application...")
    # Ensure we are in the correct directory
    os.chdir(r'c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w')
    sys.path.append(os.getcwd())
    
    from flask_app import app
    print("   - Flask application imported successfully")
    
    print("2. Initializing server...")
    print("   - Host: 0.0.0.0")
    print("   - Port: 5000")
    print("   - Threads: 4")
    
    print("="*60)
    print("SERVER RUNNING! Access at http://127.0.0.1:5000")
    print("="*60)
    
    # Run with waitress
    serve(app, host='0.0.0.0', port=5000, threads=4)
    
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    print("Please ensure all dependencies are installed.")
except Exception as e:
    print(f"CRITICAL RUNTIME ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("Server stopped.")
