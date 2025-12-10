"""Test if ai_chatbot imports correctly"""
import sys
print(f"Python path: {sys.path[0]}")

try:
    from ai_chatbot import get_chatbot
    print("✅ ai_chatbot imported successfully")
    
    import os
    os.environ['AI_PROVIDER'] = 'gemini'
    # Make sure GEMINI_API_KEY is set in your .env file
    
    bot = get_chatbot('gemini')
    print(f"✅ Chatbot created: provider={bot.provider}")
    print(f"✅ Model: {bot.model._model_name if hasattr(bot.model, '_model_name') else 'unknown'}")
    
    response = bot.chat("Test")
    print(f"✅ Response received: {response['response'][:100]}...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
