"""List available Gemini models"""
import os
import google.generativeai as genai

# Make sure GEMINI_API_KEY is set in your .env file
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

print("Available Gemini models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")
