"""Direct test of gemini_chatbot with fresh import"""
import sys
# Remove cached module
if 'gemini_chatbot' in sys.modules:
    del sys.modules['gemini_chatbot']

import os
# Make sure GEMINI_API_KEY is set in your .env file

from gemini_chatbot import get_chatbot

print("Creating chatbot...")
bot = get_chatbot()
print(f"Model: {bot.model._model_name}")

print("\nTesting chat...")
response = bot.chat("Name 2 protein foods")
print(f"Response: {response}")
