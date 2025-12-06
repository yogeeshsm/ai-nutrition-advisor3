from app_full import app
import sys

print("Starting server on http://127.0.0.1:5000")
print("Press Ctrl+C to stop")
print()

try:
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
