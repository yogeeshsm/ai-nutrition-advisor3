# 🤖 AI Chatbot Configuration Guide

Your AI Nutrition Advisor now supports **both OpenAI and Google Gemini**!

## 🎯 Quick Setup

### Option 1: Use OpenAI (ChatGPT) - Recommended

1. **Get API Key**: https://platform.openai.com/api-keys
2. **Update `.env`**:
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

3. **Restart server**

**Pros:**
- ✅ More reliable (better uptime)
- ✅ Better responses
- ✅ Faster
- ✅ Higher rate limits

**Cost:** ~$0.002 per conversation (very cheap)

---

### Option 2: Use Google Gemini (Free)

1. **Get API Key**: https://aistudio.google.com/app/apikey
2. **Update `.env`**:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSy...your-key-here
   ```

3. **Restart server**

**Pros:**
- ✅ Completely free
- ✅ Good for testing

**Cons:**
- ⚠️ Rate limits (quota issues)
- ⚠️ Slower response times

---

## 📝 Environment Variables

Add to your `.env` file:

```env
# Choose provider
AI_PROVIDER=openai  # or "gemini"

# OpenAI (if using)
OPENAI_API_KEY=sk-proj-xxxxx

# Gemini (if using)  
GEMINI_API_KEY=AIzaSyxxxxx
```

---

## 🚀 For Render Deployment

Add these environment variables in Render dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `AI_PROVIDER` | `openai` | Which AI to use |
| `OPENAI_API_KEY` | `sk-proj-...` | Your OpenAI key |

Or for Gemini:

| Variable | Value | Description |
|----------|-------|-------------|
| `AI_PROVIDER` | `gemini` | Which AI to use |
| `GEMINI_API_KEY` | `AIzaSy...` | Your Gemini key |

---

## 🧪 Testing

Test both providers:

```python
# Test OpenAI
python -c "from ai_chatbot import NutritionChatbot; bot = NutritionChatbot(provider='openai'); print(bot.chat('What are good protein sources?'))"

# Test Gemini
python -c "from ai_chatbot import NutritionChatbot; bot = NutritionChatbot(provider='gemini'); print(bot.chat('What are good protein sources?'))"
```

---

## 💰 Cost Comparison

### OpenAI (gpt-3.5-turbo):
- Input: $0.0015 / 1K tokens
- Output: $0.002 / 1K tokens
- **Average chat**: ~$0.001-0.003
- **Perfect for production**

### Gemini (1.5-flash):
- **FREE** (up to quota limits)
- Rate limits: ~15 requests/min
- **Good for development/testing**

---

## 🔄 Switching Providers

### Method 1: Update .env (Permanent)
```env
AI_PROVIDER=openai  # Change to "gemini" to switch
```

### Method 2: Code Override (Temporary)
```python
from ai_chatbot import NutritionChatbot

# Force use OpenAI
bot = NutritionChatbot(provider='openai')

# Force use Gemini
bot = NutritionChatbot(provider='gemini')
```

---

## 🎯 Recommendation

**For Development:**
- Use Gemini (free)

**For Production/Render:**
- Use OpenAI (more reliable, worth the cost)

---

## 📊 Models Used

### OpenAI:
- `gpt-3.5-turbo` (default, fast & cheap)
- Can upgrade to `gpt-4` in `ai_chatbot.py` line 69

### Gemini:
- `gemini-1.5-flash` (fast & free)

---

## ✅ Get Started

1. Get your OpenAI API key: https://platform.openai.com/api-keys
2. Update `.env`: `AI_PROVIDER=openai` and `OPENAI_API_KEY=sk-...`
3. Restart server: `python run_waitress.py`
4. Test chatbot: http://127.0.0.1:5000/chatbot

Done! 🎉
