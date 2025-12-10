# 🚀 QUICK START GUIDE - AI Nutrition Advisor

## ⚡ START THE SERVER (3 Ways)

### Method 1: Double-Click (Easiest)
```
📁 START_FULL_SERVER.bat
```

### Method 2: Command Line
```powershell
python flask_app.py
```

### Method 3: Production Server
```powershell
python production_server.py
```

---

## 🌐 ACCESS THE APP

**Main URL**: http://127.0.0.1:5000

---

## 📋 TOP 10 FEATURES TO TRY

1. **🍽️ Generate Meal Plan** - http://127.0.0.1:5000
   - Set budget, choose ingredients, get 7-day plan

2. **📸 Food Recognition AI** - http://127.0.0.1:5000/food-recognition
   - Upload food photo, get instant nutrition analysis

3. **📊 Analytics Dashboard** - http://127.0.0.1:5000/analytics
   - View 14+ interactive charts and statistics

4. **📈 Growth Tracking** - http://127.0.0.1:5000/growth-tracking
   - Track child growth with WHO Z-scores

5. **💉 Immunization Tracker** - http://127.0.0.1:5000/immunisation
   - Manage vaccination schedules

6. **🏘️ Village Economy** - http://127.0.0.1:5000/village-economy
   - Find cheapest nutritious foods

7. **🔍 Nutrition Lookup** - http://127.0.0.1:5000/nutrition-lookup
   - Search USDA food database

8. **🤖 AI Chatbot** - http://127.0.0.1:5000/chatbot
   - Ask nutrition questions

9. **💊 WHO Vaccines** - http://127.0.0.1:5000/who-vaccines
   - WHO immunization guidelines

10. **📋 About** - http://127.0.0.1:5000/about
    - Learn about all features

---

## ✅ VERIFICATION

Check if server is running:
```powershell
# Open browser to:
http://127.0.0.1:5000
```

You should see the meal planner homepage.

---

## 🛑 STOP THE SERVER

```powershell
Press CTRL+C in the terminal
```

Or:
```powershell
Get-Process python* | Stop-Process -Force
```

---

## 📚 DOCUMENTATION

- **Full Features List**: FEATURES_COMPLETE_LIST.md
- **Success Report**: PROJECT_SUCCESS_REPORT.md
- **Food Recognition**: FOOD_RECOGNITION_GUIDE.md
- **Complete Summary**: COMPLETE_SUMMARY.md

---

## 🎯 STATUS

✅ **Server**: RUNNING  
✅ **Features**: 60+ ACTIVE  
✅ **Database**: INITIALIZED  
✅ **Error Count**: 0 CRITICAL

---

## 💡 TIPS

1. **Server takes 10-30 seconds to start** (TensorFlow loading)
2. **All features work offline** except USDA API and Gemini AI
3. **Default database is SQLite** (no setup needed)
4. **Mobile responsive** - works on phones/tablets
5. **Export options** - CSV, PDF, JSON available

---

## 🔥 QUICK DEMO

1. Start server: `python flask_app.py`
2. Open: http://127.0.0.1:5000
3. Click "Generate Meal Plan"
4. Set Budget: ₹2000
5. Set Children: 20
6. Age Group: 3-6 years
7. Select 10-15 ingredients
8. Click "Generate Plan"
9. View 7-day nutrition-optimized meal plan!

---

## 📞 HELP

If server doesn't start:
1. Check Python is installed: `python --version`
2. Check packages: `pip list`
3. Reinstall requirements: `pip install -r requirements.txt`
4. Check port 5000 is free
5. Read PROJECT_SUCCESS_REPORT.md

---

**Last Updated**: December 10, 2025  
**Version**: 3.0 (Full Features)  
**Python**: 3.13.9  
**Status**: ✅ OPERATIONAL
