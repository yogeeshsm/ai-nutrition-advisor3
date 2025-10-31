# 🍽️ AI Nutrition Advisor for Karnataka Children

A comprehensive Flask-based web application that helps Anganwadi workers generate balanced weekly meal plans using AI-based recommendations and optimization algorithms.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Purpose

This application is designed to help Anganwadi workers create nutritionally balanced and cost-effective meal plans for children, ensuring they receive adequate nutrition within budget constraints.

## ✨ Key Features

### Core Features

- **🤖 AI-Powered Optimization**: Uses linear programming (PuLP) to maximize nutritional value within budget
- **🍽️ 7-Day Meal Plans**: Complete weekly plans with breakfast, lunch, snack, and dinner
- **📊 Nutrition Analysis**: Detailed breakdown of macronutrients and micronutrients
- **💰 Budget Management**: Optimize meals to stay within weekly budget
- **👶 Age-Specific Plans**: Customized plans for different age groups (1-3, 3-6, 6-10 years)

### User Interface

### User Interface

- **🥗 66 Ingredients Database**: Comprehensive nutrition data across 11 categories
- **📈 14 Interactive Charts**: Powered by Chart.js with multiple visualization types
- **📥 Multiple Export Formats**: CSV, JSON, and PDF downloads
- **🎨 Beautiful Design**: Modern UI with 25+ CSS animations and glass-morphism
- **📱 Mobile Responsive**: Works seamlessly on all devices

### Advanced Features

- **� 25+ Animations**: Smooth transitions, gradient shifts, and interactive effects
- **⭐ Nutrition Scoring**: 0-100 score for meal plan quality
- **📊 Analytics Dashboard**: Track effectiveness across budgets and age groups
- **🗄️ Database Storage**: SQLite for storing meal plans and data
- **🔄 Meal Variety**: Automatically varies meals across the week
- **🎯 Category-wise Analysis**: Analyze nutrition by food categories

## 🏗️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask 3.0.0 |
| Frontend | Bootstrap 5, Chart.js 4.4.0, jQuery 3.7.0 |
| Database | SQLite3 |
| Optimization | PuLP 2.7.0 (Linear Programming) |
| Data Processing | Pandas 2.1.1, NumPy 1.26.0 |
| Visualization | Chart.js (14 chart types) |
| PDF Export | FPDF 1.7.2 |
| UI Framework | Font Awesome 6.4.0, Google Fonts (Poppins) |

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 2GB+ RAM recommended
- Modern web browser (Chrome, Firefox, Edge)

## 🚀 Installation

### Step 1: Clone or Download the Repository

```powershell
# Clone the repository
git clone https://github.com/yogeeshsm/ai-nutrition-advisor3.git
cd ai-nutrition-advisor3

# Or simply download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an error about execution policy, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Initialize Database

```powershell
python database.py
```

This will create the SQLite database and populate it with sample ingredient data.

## 🎮 Usage

### Running the Application

```powershell
python flask_app.py
```

The application will automatically open at `http://localhost:5000`

### Using the Meal Planner

1. **Set Parameters**
   - Select age group (1-3, 3-6, or 6-10 years)
   - Set weekly budget

2. **Generate Plan**
   - Click "Generate Meal Plan" button
   - Wait for optimization (usually takes 5-15 seconds)
   - Review the generated 7-day meal plan with all meals

3. **Analyze Results**
   - View nutrition score (0-100)
   - Explore 14 interactive visualizations across 4 categories:
     * Macronutrients (Pie, Bar, Doughnut)
     * Daily Breakdown (Line, Multi-line)
     * By Category (Polar Area, Radar, Grouped Bar)
     * Micronutrients (Bar, Doughnut)
   - See day-wise meal details
   - Review cost breakdown

4. **Export Plan**
   - Download as CSV for spreadsheet use
   - Export as JSON for data processing
   - Generate PDF for printing

### Using the Analytics Dashboard

1. Navigate to "Analytics" from navigation bar
2. View comprehensive analytics:
   - Budget vs Nutrition Score scatter plots
   - Age group comparison charts
   - Cost effectiveness
3. Analyze trends:
   - Budget vs nutrition score
   - Popular age group plans
4. Review recent meal plans

## 📊 Database Schema

### Ingredients Table

```sql
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    cost_per_kg REAL NOT NULL,
    protein_per_100g REAL,
    carbs_per_100g REAL,
    fat_per_100g REAL,
    calories_per_100g REAL,
    fiber_per_100g REAL,
    iron_per_100g REAL,
    calcium_per_100g REAL,
    serving_size_g REAL
)
```

### Meal Plans Table

```sql
CREATE TABLE meal_plans (
    id INTEGER PRIMARY KEY,
    plan_name TEXT,
    budget REAL,
    num_children INTEGER,
    age_group TEXT,
    total_cost REAL,
    nutrition_score REAL,
    plan_data TEXT,
    created_at TIMESTAMP
)
```

## 🔧 Configuration

### Customizing Ingredients

Edit `database.py` and modify the `insert_sample_ingredients()` function to add or update ingredients:

```python
ingredients = [
    ("Ingredient Name", "Category", cost_per_kg, protein, carbs, fat, 
     calories, fiber, iron, calcium, serving_size)
]
```

### Adjusting Nutritional Requirements

Edit `meal_optimizer.py` and modify the `_get_daily_requirements()` method:

```python
requirements = {
    "age_group": {
        'calories': value,
        'protein': value,
        # ... other nutrients
    }
}
```

### Modifying Meal Distribution

In `meal_optimizer.py`, adjust the `meal_distribution` dictionary:

```python
self.meal_distribution = {
    'breakfast': 0.25,  # 25% of daily intake
    'lunch': 0.40,      # 40% of daily intake
    'snack': 0.10,      # 10% of daily intake
    'dinner': 0.25      # 25% of daily intake
}
```

## 📖 Project Structure

```
ai nutrition advisor3w/
├── app.py                  # Main Streamlit application
├── database.py            # Database operations and initialization
├── meal_optimizer.py      # Meal optimization engine
├── utils.py               # Utility functions (PDF export, translation)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── nutrition_advisor.db  # SQLite database (auto-generated)
```

## 🧮 Optimization Algorithm

The meal optimizer uses **Linear Programming** to:

1. **Maximize**: Nutritional value (protein, fiber, iron, calcium)
2. **Subject to**:
   - Budget constraint
   - Minimum calorie requirements (80% of target)
   - Maximum calorie limits (130% of target)
   - Maximum quantity per ingredient per meal

The optimization ensures balanced nutrition while staying within budget.

## 📊 Nutrition Scoring

The nutrition score (0-100) is calculated based on:

- Meeting daily requirements for 7 key nutrients
- Optimal range: 90-110% of requirement = 100 points
- Below 90%: Proportional reduction
- Above 110%: Penalty for excess

## 🌐 Language Support

Supports translation to:
- 🇬🇧 English
- 🇮🇳 Hindi (हिंदी)
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Tamil (தமிழ்)

*Note: Translation uses Google Translate API and requires internet connection*

## 🎨 Customization

### Changing Theme

Modify the custom CSS in `app.py`:

```python
st.markdown("""
    <style>
    .main-header {
        color: #YOUR_COLOR;
    }
    </style>
""", unsafe_allow_html=True)
```

### Adding Food Categories

1. Update `FOOD_EMOJIS` in `utils.py`
2. Add ingredients to database with new category
3. Restart application

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found error
```powershell
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue**: Database error
```powershell
# Solution: Delete and reinitialize database
Remove-Item nutrition_advisor.db
python database.py
```

**Issue**: Optimization takes too long
- Reduce number of selected ingredients
- Increase budget slightly
- Select more common ingredients

**Issue**: Low nutrition score
- Increase budget
- Select more diverse ingredients
- Include protein and dairy sources

### Getting Help

If you encounter issues:
1. Check the error message in terminal
2. Verify all dependencies are installed
3. Ensure database is initialized
4. Try with default/recommended ingredients

## 📈 Performance Tips

- **Faster Generation**: Select 10-15 ingredients instead of all
- **Better Results**: Include mix of grains, pulses, vegetables, and dairy
- **Budget Optimization**: Start with recommended budget per child: ₹30-50/day
- **Variety**: Use different ingredients for consecutive days

## 🔒 Data Privacy

- All data is stored locally in SQLite database
- No data is sent to external servers (except for translation)
- Meal plans can be deleted from database manually

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Target Users

- Anganwadi Workers
- Nutritionists
- Child Care Centers
- School Meal Programs
- NGOs working in child nutrition
- Government nutrition programs

## 🙏 Acknowledgments

- Nutritional data based on ICMR (Indian Council of Medical Research) guidelines
- Food cost data approximated for Indian markets (2024)
- Icons and emojis from Unicode Standard

## 📞 Support

For questions, feedback, or support:
- Create an issue in the repository
- Contact your local Anganwadi coordinator
- Email: [Your contact email]

## 🎯 Future Enhancements

Planned features:
- [ ] Voice input for accessibility
- [ ] Mobile app version
- [ ] Offline mode
- [ ] Recipe suggestions
- [ ] Inventory management
- [ ] Seasonal ingredient recommendations
- [ ] Multi-user support with authentication
- [ ] Integration with government databases

## 📊 Sample Results

With a budget of ₹2000 for 20 children (₹14.28/child/day):
- Nutrition Score: 85-95/100
- Balanced macronutrients
- Meets 90-110% of daily requirements
- Variety of 15-20 ingredients across week

## 🌟 Impact

This tool helps:
- ✅ Ensure nutritional adequacy
- ✅ Optimize limited budgets
- ✅ Reduce meal planning time
- ✅ Maintain variety in diet
- ✅ Track nutrition trends
- ✅ Improve child health outcomes

---

**Made with ❤️ for India's children**

**Version**: 1.0.0  
**Last Updated**: October 2025
