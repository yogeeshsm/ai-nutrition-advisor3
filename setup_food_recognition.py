"""
One-Click Setup for Food Image Recognition Feature
Installs dependencies, runs tests, and starts the server
"""

import subprocess
import sys
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n▶️  {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print_header("🍲 Food Recognition Setup")
    print("\nThis script will:")
    print("1. Install TensorFlow and Keras")
    print("2. Run comprehensive tests")
    print("3. Start the Flask server")
    print("\nPress Ctrl+C at any time to cancel")
    
    try:
        # Step 1: Check Python version
        print_header("Step 1: Checking Python Version")
        python_version = sys.version_info
        print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("❌ Python 3.8 or higher required")
            return 1
        
        print("✅ Python version compatible")
        
        # Step 2: Install dependencies
        print_header("Step 2: Installing Dependencies")
        
        print("\nChoose installation option:")
        print("1. TensorFlow (with GPU support) - ~500MB")
        print("2. TensorFlow CPU (no GPU) - ~200MB (Recommended)")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            package = "tensorflow==2.15.0"
        else:
            package = "tensorflow-cpu==2.15.0"
        
        packages = [package, "keras==2.15.0"]
        
        for pkg in packages:
            if not run_command(
                f"{sys.executable} -m pip install {pkg}",
                f"Installing {pkg}"
            ):
                print("\n⚠️  Installation failed. Trying alternative...")
                run_command(
                    f"{sys.executable} -m pip install --upgrade pip",
                    "Upgrading pip"
                )
                run_command(
                    f"{sys.executable} -m pip install {pkg}",
                    f"Retrying {pkg}"
                )
        
        # Step 3: Verify installation
        print_header("Step 3: Verifying Installation")
        
        try:
            import tensorflow as tf
            import keras
            print(f"✅ TensorFlow version: {tf.__version__}")
            print(f"✅ Keras version: {keras.__version__}")
        except ImportError as e:
            print(f"❌ Verification failed: {e}")
            return 1
        
        # Step 4: Run tests
        print_header("Step 4: Running Tests")
        
        print("\nRun comprehensive tests? (y/n): ", end="")
        run_tests = input().strip().lower()
        
        if run_tests == 'y':
            if not run_command(
                f"{sys.executable} test_food_recognition.py",
                "Running test suite"
            ):
                print("\n⚠️  Some tests failed, but you can still try the server")
        else:
            print("⏭️  Skipping tests")
        
        # Step 5: Start server
        print_header("Step 5: Starting Server")
        
        print("\nStart the Flask server? (y/n): ", end="")
        start_server = input().strip().lower()
        
        if start_server == 'y':
            print("\n🚀 Starting server...")
            print("📍 Visit: http://localhost:5000/food-recognition")
            print("\n⌨️  Press Ctrl+C to stop the server\n")
            
            try:
                subprocess.run([sys.executable, "flask_app.py"])
            except KeyboardInterrupt:
                print("\n\n👋 Server stopped")
        else:
            print("\n✅ Setup complete!")
            print("\nTo start the server manually:")
            print(f"  {sys.executable} flask_app.py")
        
        # Success summary
        print_header("✅ Setup Complete!")
        print("\n📖 Documentation:")
        print("  - Quick Start: FOOD_RECOGNITION_QUICKSTART.md")
        print("  - Full Guide: FOOD_RECOGNITION_GUIDE.md")
        print("  - Summary: FOOD_RECOGNITION_SUMMARY.md")
        print("\n🧪 Run tests:")
        print(f"  {sys.executable} test_food_recognition.py")
        print("\n🚀 Start server:")
        print(f"  {sys.executable} flask_app.py")
        print("\n📱 Visit:")
        print("  http://localhost:5000/food-recognition")
        print("\n" + "="*60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
