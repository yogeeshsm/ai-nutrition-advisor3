"""
Quick test to verify Groq chatbot is working
"""

from gemini_chatbot import NutritionChatbot

print("🚀 Testing Groq-powered Nutrition Chatbot...\n")
print("=" * 80)

# Initialize chatbot
try:
    chatbot = NutritionChatbot()
    print("✅ Chatbot initialized successfully!")
    print(f"   Model: {chatbot.GROQ_MODEL}")
    print(f"   API Key: {chatbot.api_key[:20]}...")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    exit(1)

print("\n" + "=" * 80)
print("📝 Testing Chat Functionality")
print("=" * 80 + "\n")

# Test questions
test_questions = [
    "What are good iron sources for preventing anemia in children?",
    "How much protein does a 5-year-old child need daily?",
    "What are budget-friendly calcium sources?"
]

for i, question in enumerate(test_questions, 1):
    print(f"\n{i}. Question: {question}")
    print("-" * 80)
    
    try:
        response = chatbot.chat(question)
        print(f"✅ Response received ({len(response)} chars):")
        print(response)
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ CHATBOT TEST COMPLETE!")
print("=" * 80)

print("\n🔗 To use in Flask app:")
print("   1. Run: python flask_app.py")
print("   2. Open: http://localhost:5000/chatbot")
print("   3. Or POST to: http://localhost:5000/api/chatbot")
