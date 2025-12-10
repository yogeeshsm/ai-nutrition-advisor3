"""
AI Nutrition Chatbot with support for both OpenAI and Gemini APIs
Provides personalized nutrition advice and meal plan modifications
"""

import os
from typing import Dict, List, Optional

class NutritionChatbot:
    """AI Nutrition Chatbot powered by OpenAI or Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        """
        Initialize the chatbot with API
        
        Args:
            api_key: API key (if None, reads from environment)
            provider: "openai" or "gemini"
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            self._init_openai(api_key)
        elif self.provider == "gemini":
            self._init_gemini(api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'gemini'")
        
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
"""
    
    def _init_openai(self, api_key: Optional[str] = None):
        """Initialize OpenAI"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = "gpt-3.5-turbo"  # or "gpt-4" for better quality
    
    def _init_gemini(self, api_key: Optional[str] = None):
        """Initialize Gemini"""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Google GenerativeAI package not installed. Run: pip install google-generativeai")
        
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def chat(self, message: str, context: Optional[str] = None) -> Dict[str, any]:
        """
        Chat with the nutrition AI
        
        Args:
            message: User's question or message
            context: Additional context (meal plan, child info, etc.)
        
        Returns:
            Dict with 'response' and 'success' keys
        """
        try:
            # Build the prompt
            full_prompt = f"{self.system_context}\n\n"
            if context:
                full_prompt += f"Context: {context}\n\n"
            full_prompt += f"User: {message}\n\nNutritionist:"
            
            if self.provider == "openai":
                return self._chat_openai(full_prompt)
            else:
                return self._chat_gemini(full_prompt)
                
        except Exception as e:
            return {
                'success': False,
                'response': f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question.",
                'error': str(e)
            }
    
    def _chat_openai(self, prompt: str) -> Dict[str, any]:
        """Chat using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                'success': True,
                'response': response.choices[0].message.content,
                'provider': 'openai',
                'model': self.model_name
            }
        except Exception as e:
            return {
                'success': False,
                'response': f"OpenAI API error: {str(e)}",
                'error': str(e),
                'provider': 'openai'
            }
    
    def _chat_gemini(self, prompt: str) -> Dict[str, any]:
        """Chat using Gemini"""
        response = self.model.generate_content(prompt)
        
        return {
            'success': True,
            'response': response.text,
            'provider': 'gemini',
            'model': 'gemini-1.5-flash'
        }
    
    def get_meal_advice(self, meal_plan: Dict, child_info: Dict) -> Dict[str, any]:
        """Get advice on a specific meal plan"""
        context = f"""
Child Information:
- Age: {child_info.get('age', 'Unknown')} years
- Weight: {child_info.get('weight', 'Unknown')} kg
- Gender: {child_info.get('gender', 'Unknown')}
- Special needs: {child_info.get('special_needs', 'None')}

Current Meal Plan:
{self._format_meal_plan(meal_plan)}
"""
        
        message = "Please review this meal plan and provide suggestions for improvement."
        return self.chat(message, context)
    
    def suggest_alternatives(self, ingredient: str, reason: str = "") -> Dict[str, any]:
        """Suggest alternative ingredients"""
        message = f"What are good alternatives to {ingredient}"
        if reason:
            message += f" because {reason}"
        message += "? Please suggest 3-5 locally available Indian alternatives."
        
        return self.chat(message)
    
    def _format_meal_plan(self, meal_plan: Dict) -> str:
        """Format meal plan for context"""
        formatted = ""
        for day, meals in meal_plan.items():
            formatted += f"\n{day}:\n"
            for meal_type, items in meals.items():
                formatted += f"  {meal_type}: {', '.join(items)}\n"
        return formatted


def get_chatbot(provider: str = None) -> NutritionChatbot:
    """
    Factory function to get a chatbot instance
    
    Args:
        provider: "openai" or "gemini" (defaults to env var or "openai")
    
    Returns:
        NutritionChatbot instance
    """
    if provider is None:
        provider = os.environ.get('AI_PROVIDER', 'openai')
    
    return NutritionChatbot(provider=provider)


# Example usage
if __name__ == "__main__":
    # Test with OpenAI
    print("Testing OpenAI...")
    try:
        bot_openai = NutritionChatbot(provider="openai")
        response = bot_openai.chat("What are good sources of protein for children?")
        print(f"OpenAI Response: {response['response'][:200]}...")
    except Exception as e:
        print(f"OpenAI Error: {e}")
    
    # Test with Gemini
    print("\nTesting Gemini...")
    try:
        bot_gemini = NutritionChatbot(provider="gemini")
        response = bot_gemini.chat("What are good sources of iron for children?")
        print(f"Gemini Response: {response['response'][:200]}...")
    except Exception as e:
        print(f"Gemini Error: {e}")
