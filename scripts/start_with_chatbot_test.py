"""
Quick script to test if chatbot is working before starting Flask
"""
import sys
import os

print("=" * 80)
print("🔍 TESTING CHATBOT BEFORE FLASK START")
print("=" * 80)

# Test 1: Import the chatbot
print("\n1️⃣ Testing import...")
try:
    from gemini_chatbot import get_chatbot, NutritionChatbot
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize chatbot
print("\n2️⃣ Testing initialization...")
try:
    chatbot = get_chatbot()
    if chatbot:
        print("✅ Chatbot initialized")
        print(f"   API URL: {chatbot.GROQ_API_URL}")
        print(f"   Model: {chatbot.GROQ_MODEL}")
    else:
        print("❌ Chatbot is None")
        sys.exit(1)
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    sys.exit(1)

# Test 3: Simple chat test
print("\n3️⃣ Testing chat...")
try:
    response = chatbot.chat("Hello, what is protein?")
    if response and "error" not in response.lower() and "api key" not in response.lower():
        print(f"✅ Chat working! Response length: {len(response)} chars")
        print(f"   Preview: {response[:100]}...")
    else:
        print(f"❌ Chat failed: {response}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Chat error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - CHATBOT IS READY!")
print("=" * 80)
print("\n🚀 Now starting Flask app...\n")

# Now start Flask
os.system("python flask_app.py")
