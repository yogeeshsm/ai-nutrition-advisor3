"""Keep server running"""
print("Loading...")
from flask_app import app

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI NUTRITION ADVISOR - http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
