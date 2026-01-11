"""
AI Nutrition Chatbot using Groq API
Provides personalized nutrition advice and meal plan modifications
"""

import os
from groq import Groq
from typing import Dict, List, Optional

# Groq API Configuration - Use environment variable
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GROQ_MODEL = 'llama-3.1-8b-instant'  # Faster model for quicker responses

class NutritionChatbot:
    """AI Nutrition Chatbot powered by Groq"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the chatbot with Groq API"""
        self.api_key = api_key or os.environ.get('GROQ_API_KEY') or GROQ_API_KEY
        
        if not self.api_key:
            raise ValueError("Groq API key not found. Set GROQ_API_KEY environment variable.")
        
        # Configure Groq client
        self.client = Groq(api_key=self.api_key)
        self.model = GROQ_MODEL
        
        # System context for nutrition expertise
        self.system_context = """You are an expert nutritionist specializing in child nutrition for Karnataka Anganwadi centers.

Provide detailed, practical advice on:
- Indian foods and traditional meal planning
- ICMR nutrition guidelines for children aged 1-10 years
- Budget-friendly meal planning for rural areas
- Managing nutritional deficiencies (anemia, protein, vitamin A)
- Creating balanced vegetarian and non-vegetarian meal plans

Response Format:
- Provide 7-8 lines of detailed, actionable advice
- Use simple, easy-to-understand language
- Include specific Indian food examples
- Give practical tips that can be implemented immediately
- Only mention costs/fees when directly asked or when it's essential to the context
- Avoid adding cost information at the end of responses unless specifically requested

Keep responses comprehensive yet concise (7-8 lines)."""

    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Send a message to the chatbot and get a response
        
        Args:
            user_message: The user's question or message
            conversation_history: Previous conversation messages (optional)
            
        Returns:
            The chatbot's response
        """
        try:
            # Build messages for Groq
            messages = [
                {"role": "system", "content": self.system_context}
            ]
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-5:]:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    messages.append({"role": role, "content": content})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call Groq API with balanced settings
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,  # Balanced for detailed yet focused responses
                max_tokens=600,   # Increased for 7-8 lines of detailed response
                top_p=0.9         # Nucleus sampling for better quality
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg or "rate" in error_msg.lower():
                return """🤖 **AI Chatbot Temporarily Unavailable**

The AI service has reached its rate limit. Please wait a moment and try again.

In the meantime, you can use other features:
📊 **Nutrition Lookup** - Search food nutrition information
📈 **Growth Tracking** - Monitor child growth and development  
🍽️ **Meal Planning** - Create optimized meal plans
💉 **Immunization Schedule** - Track vaccination records
🎯 **ML Recommendations** - Get AI-powered food suggestions"""
            return f"I apologize, but I encountered an error: {error_msg}. Please try rephrasing your question."
    
    def get_meal_advice(self, meal_plan_data: Dict, concern: str) -> str:
        """
        Get specific advice about a meal plan
        """
        prompt = f"""Analyze this meal plan and provide specific advice:

Meal Plan Details:
- Nutrition Score: {meal_plan_data.get('nutrition_score', 'N/A')}/100
- Number of Children: {meal_plan_data.get('num_children', 'N/A')}
- Age Group: {meal_plan_data.get('age_group', 'N/A')}
- Budget: ₹{meal_plan_data.get('budget', 'N/A')}

User's Concern: {concern}

Provide:
1. Analysis of the current plan
2. Specific recommendations to address the concern
3. Budget-friendly alternatives if needed (only mention specific costs if the concern is about budget)"""

        return self.chat(prompt)
    
    def suggest_alternatives(self, food_item: str, reason: str) -> str:
        """
        Suggest alternatives for a food item
        """
        prompt = f"""Suggest healthy Indian alternatives for: {food_item}
Reason for seeking alternatives: {reason}

Please provide:
1. 3-5 alternative foods commonly available in India
2. Nutritional benefits of each
3. How to prepare/serve for children
4. Cost comparison only if the reason mentions budget/affordability"""

        return self.chat(prompt)


def get_chatbot(api_key: Optional[str] = None) -> Optional[NutritionChatbot]:
    """
    Factory function to get a chatbot instance
    
    Args:
        api_key: Optional API key (will use env variable if not provided)
        
    Returns:
        NutritionChatbot instance or None if initialization fails
    """
    try:
        return NutritionChatbot(api_key)
    except Exception as e:
        print(f"[WARNING] Failed to initialize chatbot: {e}")
        return None
