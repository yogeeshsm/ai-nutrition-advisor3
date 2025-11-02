"""
AI Nutrition Chatbot using Google Gemini API
Provides personalized nutrition advice and meal plan modifications
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional

class NutritionChatbot:
    """AI Nutrition Chatbot powered by Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the chatbot with Gemini API"""
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model (using latest stable Gemini 2.0 Flash)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # System context for nutrition expertise
        self.system_context = """You are an expert nutritionist and dietitian specializing in child nutrition for Anganwadi centers in India. 

Your expertise includes:
- Indian foods and traditional meal planning
- ICMR nutrition guidelines for children aged 1-10 years
- Budget-friendly meal planning for rural areas
- Managing common nutritional deficiencies (anemia, protein deficiency, vitamin A deficiency)
- Addressing dietary restrictions and allergies
- Creating balanced vegetarian and non-vegetarian meal plans
- Food safety and hygiene practices

Key nutritional requirements for Indian children (3-6 years):
- Energy: 1240-1350 kcal/day
- Protein: 16.7-20.1 g/day
- Calcium: 600 mg/day
- Iron: 9 mg/day
- Vitamin A: 400 μg/day

Always provide:
1. Practical, actionable advice
2. Budget-conscious recommendations
3. Culturally appropriate suggestions (Indian foods)
4. Simple, easy-to-understand language
5. Safety warnings when needed

Keep responses concise (2-3 paragraphs) unless asked for details."""

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
            # Build the full prompt with context
            if conversation_history:
                # Include previous messages for context
                context = "\n\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in conversation_history[-5:]  # Last 5 messages
                ])
                full_prompt = f"{self.system_context}\n\nPrevious conversation:\n{context}\n\nUser: {user_message}\n\nAssistant:"
            else:
                full_prompt = f"{self.system_context}\n\nUser: {user_message}\n\nAssistant:"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            return response.text
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."
    
    def get_meal_advice(self, meal_plan_data: Dict, concern: str) -> str:
        """
        Get specific advice about a meal plan
        
        Args:
            meal_plan_data: Current meal plan details (nutrition score, ingredients, cost)
            concern: User's specific concern (e.g., "too expensive", "lacks protein")
            
        Returns:
            Tailored advice for the meal plan
        """
        prompt = f"""Analyze this meal plan and provide specific advice:

Meal Plan Details:
- Nutrition Score: {meal_plan_data.get('nutrition_score', 'N/A')}/100
- Total Cost: ₹{meal_plan_data.get('total_cost', 'N/A')}
- Number of Children: {meal_plan_data.get('num_children', 'N/A')}
- Age Group: {meal_plan_data.get('age_group', 'N/A')}
- Budget: ₹{meal_plan_data.get('budget', 'N/A')}

User's Concern: {concern}

Provide:
1. Assessment of the current plan
2. Specific recommendations to address the concern
3. 2-3 actionable suggestions with Indian ingredients
4. Expected improvement in nutrition or cost"""

        try:
            response = self.model.generate_content(f"{self.system_context}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error analyzing meal plan: {str(e)}"
    
    def suggest_alternatives(self, ingredient: str, reason: str = "general") -> str:
        """
        Suggest alternative ingredients
        
        Args:
            ingredient: The ingredient to replace
            reason: Why it needs replacement (allergy, cost, availability)
            
        Returns:
            List of alternative ingredients with explanations
        """
        prompt = f"""Suggest 3-4 alternative ingredients to replace "{ingredient}" in an Indian Anganwadi meal plan.

Reason for replacement: {reason}

For each alternative, provide:
1. Ingredient name
2. Nutritional comparison
3. Cost comparison (if relevant)
4. Availability in rural India
5. How to use it in meals

Keep suggestions practical and affordable."""

        try:
            response = self.model.generate_content(f"{self.system_context}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error suggesting alternatives: {str(e)}"
    
    def answer_nutrition_question(self, question: str) -> str:
        """
        Answer general nutrition questions
        
        Args:
            question: User's nutrition-related question
            
        Returns:
            Detailed answer
        """
        prompt = f"""Answer this nutrition question for parents/caregivers of children in Anganwadi centers:

Question: {question}

Provide a clear, practical answer suitable for rural Indian context."""

        try:
            response = self.model.generate_content(f"{self.system_context}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def get_feeding_tips(self, age_group: str, challenge: str) -> str:
        """
        Get tips for specific feeding challenges
        
        Args:
            age_group: Child's age group (1-3, 3-6, 6-10 years)
            challenge: Specific challenge (picky eater, refuses vegetables, etc.)
            
        Returns:
            Practical feeding tips
        """
        prompt = f"""Provide practical tips for handling this feeding challenge:

Age Group: {age_group}
Challenge: {challenge}

Give 4-5 actionable tips that:
1. Are culturally appropriate for India
2. Can be implemented in Anganwadi settings
3. Are based on child psychology and nutrition science
4. Include specific examples"""

        try:
            response = self.model.generate_content(f"{self.system_context}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error generating tips: {str(e)}"


# Helper function to initialize chatbot
def get_chatbot(api_key: Optional[str] = None) -> Optional[NutritionChatbot]:
    """
    Initialize and return a chatbot instance
    
    Usage:
        chatbot = get_chatbot()
        if chatbot:
            response = chatbot.chat("How can I increase protein in meals?")
    """
    try:
        return NutritionChatbot(api_key)
    except ValueError as e:
        print(f"⚠️ Chatbot initialization failed: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Test the chatbot
    chatbot = get_chatbot()
    
    if chatbot:
        print("🤖 Nutrition Chatbot initialized!\n")
        
        # Test questions
        questions = [
            "What are good protein sources for vegetarian children?",
            "My child refuses to eat vegetables. What should I do?",
            "How can I make meals more nutritious on a tight budget?"
        ]
        
        for q in questions:
            print(f"Q: {q}")
            response = chatbot.chat(q)
            print(f"A: {response}\n")
            print("-" * 80 + "\n")
