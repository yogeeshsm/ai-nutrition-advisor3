"""Quick test of OpenAI chatbot"""
import os
os.environ['AI_PROVIDER'] = 'openai'
# Make sure OPENAI_API_KEY is set in your .env file

from ai_chatbot import get_chatbot

print("Testing OpenAI chatbot...")
print(f"AI_PROVIDER: {os.environ.get('AI_PROVIDER')}")

bot = get_chatbot()
print(f"Bot provider: {bot.provider}")
print(f"Bot model: {bot.model_name}")

response = bot.chat("List 3 iron-rich foods for toddlers")
print(f"\nResponse: {response['response']}")
print("\n✅ OpenAI chatbot working!")
