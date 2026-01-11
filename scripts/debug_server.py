"""
Server with logging to file to debug why it's exiting
"""
import sys
import os
from datetime import datetime

# Redirect output to log file
log_file = open('server_log.txt', 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file

print(f"[{datetime.now()}] Server starting...")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

try:
    from flask import Flask, render_template
    print(f"[{datetime.now()}] Flask imported successfully")
    
    import database as db
    print(f"[{datetime.now()}] Database imported successfully")
    
    app = Flask(__name__)
    app.secret_key = 'test-key'
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    print(f"[{datetime.now()}] Routes configured")
    
    # Try Waitress
    try:
        from waitress import serve
        print(f"[{datetime.now()}] Waitress loaded, starting server...")
        serve(app, host='0.0.0.0', port=5000)
        print(f"[{datetime.now()}] Waitress serve() returned (this shouldn't happen)")
    except Exception as e:
        print(f"[{datetime.now()}] Waitress error: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"[{datetime.now()}] Fatal error: {e}")
    import traceback
    traceback.print_exc()
finally:
    print(f"[{datetime.now()}] Server exiting")
    log_file.close()
