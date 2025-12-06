"""Test if flask_app can run at all"""
import sys
import os

os.chdir(r'c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w')

print("Step 1: Importing Flask...")
from flask import Flask
print("OK")

print("Step 2: Creating app...")
app = Flask(__name__)
print("OK")

print("Step 3: Adding route...")
@app.route('/')
def home():
    return '<h1>Server is running!</h1><p>All features will be available soon.</p>'
print("OK")

print("Step 4: Starting server with waitress...")
try:
    from waitress import serve
    print("Waitress imported")
    print("Starting on http://0.0.0.0:5000")
    serve(app, host='0.0.0.0', port=5000, threads=4)
except KeyboardInterrupt:
    print("\nServer stopped")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
