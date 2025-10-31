# 🚀 Quick Start Guide - AI Nutrition Advisor

## 5-Minute Setup

### 1️⃣ Open PowerShell in Project Folder
```powershell
cd "C:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
```

### 2️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3️⃣ Initialize Database
```powershell
python database.py
```

### 4️⃣ Run the App
```powershell
streamlit run app.py
```

### 5️⃣ Open Browser
The app will automatically open at: http://localhost:8501

---

## ⚡ Quick Commands

### Start the App
```powershell
streamlit run app.py
```

### Reset Database
```powershell
Remove-Item nutrition_advisor.db; python database.py
```

### Update Dependencies
```powershell
pip install -r requirements.txt --upgrade
```

### Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 🎯 First-Time Usage

1. **Click "Recommended" button** - Selects common ingredients
2. **Set Budget** - Try ₹2000 for 20 children
3. **Select Age Group** - Choose "3-6 years"
4. **Click "Generate Meal Plan"** - Wait 5-15 seconds
5. **Review Results** - Check nutrition score and cost
6. **Export Plan** - Download as PDF or CSV

---

## 💡 Pro Tips

### Get Better Results
- ✅ Select 12-15 ingredients (not all)
- ✅ Include mix of grains, pulses, vegetables, dairy
- ✅ Budget: ₹30-50 per child per day
- ✅ Use "Recommended" button for beginners

### Faster Generation
- Select fewer ingredients (10-15)
- Avoid selecting too many exotic items
- Increase budget slightly if optimization is slow

### Higher Nutrition Score
- Include protein sources (dal, eggs, milk)
- Add green vegetables (spinach, etc.)
- Include dairy products
- Add jaggery or fruits for micronutrients

---

## 🐛 Quick Fixes

### Error: Module not found
```powershell
pip install [module-name]
```

### Error: Database locked
```powershell
# Close app and restart
Ctrl+C
streamlit run app.py
```

### App won't start
```powershell
# Check Python version (need 3.8+)
python --version

# Reinstall Streamlit
pip install streamlit --force-reinstall
```

---

## 📱 Sample Scenarios

### Small Anganwadi (10 children, 3-6 years)
- Budget: ₹1000/week (₹14/child/day)
- Select: Rice, Wheat, 2 dals, 4 vegetables, milk, oil
- Expected Score: 75-85/100

### Medium Anganwadi (25 children, 3-6 years)
- Budget: ₹2500/week (₹14/child/day)
- Select: Recommended ingredients + eggs
- Expected Score: 85-95/100

### Large Anganwadi (50 children, multiple age groups)
- Budget: ₹5000/week
- Select: All available ingredients
- Expected Score: 90-100/100

---

## 🎨 Interface Guide

### Main Page
- **Left Sidebar**: Settings and navigation
- **Top Section**: Input fields (children, budget, age)
- **Middle Section**: Ingredient selection by category
- **Bottom**: Generate button and results

### Analytics Page
- View statistics across all meal plans
- Compare budget effectiveness
- Track nutrition trends

### About Page
- Information about the app
- Nutritional guidelines
- Contact details

---

## 📊 Understanding Results

### Nutrition Score
- **90-100**: Excellent - Meets all requirements
- **70-89**: Good - Minor adjustments needed
- **50-69**: Fair - Increase budget or diversity
- **Below 50**: Poor - Revise ingredient selection

### Cost Metrics
- **Total Cost**: Weekly cost for all children
- **Per Child/Week**: Weekly cost per child
- **Per Child/Day**: Daily cost per child
- **Per Meal**: Average cost per meal

### Nutrition Charts
- **Pie Chart**: Macronutrient distribution (protein/carbs/fat)
- **Bar Chart**: Requirements vs achieved for each nutrient
- **Percentage Cards**: How well each nutrient target is met

---

## 🔄 Workflow

```
Select Ingredients → Set Budget → Choose Age Group
          ↓
    Generate Plan (AI Optimization)
          ↓
    Review Nutrition Score & Cost
          ↓
    View Day-wise Meals
          ↓
    Export (PDF/CSV/JSON)
          ↓
    Implement & Track Results
```

---

## 📞 Need Help?

### Common Questions

**Q: How long does optimization take?**  
A: Usually 5-15 seconds. More ingredients = longer time.

**Q: Why is my nutrition score low?**  
A: Increase budget or select more diverse ingredients, especially protein sources.

**Q: Can I edit the generated plan?**  
A: Export to CSV and edit in Excel, or regenerate with different parameters.

**Q: How accurate are the nutrition values?**  
A: Based on ICMR data, accurate within 10-15% for most ingredients.

**Q: Can I add my own ingredients?**  
A: Yes! Edit database.py and add to the ingredients list.

### Contact Support
- GitHub Issues: [Repository URL]
- Email: [Your email]
- Anganwadi Coordinator: [Contact]

---

**Happy Meal Planning! 🍽️**
