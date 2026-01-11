"""
Standalone server launcher - bypasses import issues
"""
import sys
import os
import subprocess

# Change to project directory
os.chdir(r'c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w')

# Path to venv python
venv_python = r"C:/Users/S M Yogesh/OneDrive/ドキュメント/ai nutrition advisor3w/.venv/Scripts/python.exe"

print("="*60)
print("AI NUTRITION ADVISOR - LAUNCHING FULL VERSION")
print("="*60)
print("Attempting to start server with all 60+ features...")
print("="*60)

# Create a minimal launcher that will exec flask_app
launcher_code = """
import signal
import sys

# Ignore keyboard interrupt during startup
def ignore_sigint(signum, frame):
    pass

signal.signal(signal.SIGINT, ignore_sigint)

# Now import and run the app
print("Loading Flask application...")
try:
    import flask_app
    print("Flask app loaded successfully!")
except Exception as e:
    print(f"Error loading flask_app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""

# Write launcher
with open('_launcher.py', 'w') as f:
    f.write(launcher_code)

# Run it
try:
    subprocess.run([venv_python, '_launcher.py'], check=True)
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Cleanup
    if os.path.exists('_launcher.py'):
        os.remove('_launcher.py')
