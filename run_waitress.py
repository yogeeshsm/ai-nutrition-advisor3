"""Run server with waitress WSGI server"""
from waitress import serve
from flask_app import app

if __name__ == '__main__':
    print("="*60)
    print("AI NUTRITION ADVISOR - FULL VERSION")
    print("="*60)
    print("Server starting on http://127.0.0.1:5000")
    print("All 60+ features enabled")
    print("Press CTRL+C to stop")
    print("="*60)
    serve(app, host='0.0.0.0', port=5000, threads=4)
