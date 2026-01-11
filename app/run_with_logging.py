"""
Flask app runner with file logging
"""
import sys
import os
from datetime import datetime

# Setup logging to file
log_file = 'server_startup.log'
sys.stdout = open(log_file, 'w', encoding='utf-8')
sys.stderr = sys.stdout

print(f"Server startup log - {datetime.now()}")
print("="*60)

try:
    print("Importing Flask and dependencies...")
    from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
    print("Flask imported successfully")
    
    print("Importing flask_app...")
    # Change to app directory
    os.chdir(r'c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w')
    
    # Import the app
    import flask_app
    print("flask_app imported successfully")
    
    print("App should now be running...")
    print("If you see this message, check if server is accessible at http://127.0.0.1:5000")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
