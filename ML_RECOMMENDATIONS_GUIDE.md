# ML Recommendation System - User Guide

## 🤖 Machine Learning Features Implemented

### 1. **Hybrid Recommendation System**
Combines collaborative filtering and content-based filtering for best results.

**How it works:**
- Analyzes similar children's meal preferences
- Matches ingredients to child's nutritional needs
- Combines both approaches with optimal weights (60% collaborative + 40% content-based)

**API Endpoint:**
```
GET /api/ml/recommendations/{child_id}?type=hybrid&top_n=15
```

---

### 2. **Collaborative Filtering**
Recommends meals based on what similar children ate and enjoyed.

**How it works:**
- Finds children with similar age, weight, height, health conditions
- Analyzes their successful meal plans
- Recommends ingredients that worked well for them

**API Endpoint:**
```
GET /api/ml/recommendations/{child_id}?type=collaborative&top_n=15
```

**Use Case:**
- "Children like this one enjoyed these meals"
- Leverages community knowledge
- Great for new children without history

---

### 3. **Content-Based Filtering**
Matches ingredients to child's specific nutritional requirements.

**How it works:**
- Analyzes child's nutritional priorities (protein, iron, calcium, calories)
- Scores ingredients based on nutrient content
- Considers budget constraints
- Recommends high-value, nutrient-dense foods

**API Endpoint:**
```
GET /api/ml/recommendations/{child_id}?type=content&top_n=15
```

**Use Case:**
- Personalized to child's unique needs
- Adapts to health conditions
- Considers growth trends

---

### 4. **Similar Children Finder**
Identifies children with similar nutritional profiles.

**How it works:**
- Uses K-Nearest Neighbors algorithm
- Considers: age, weight, height, gender, health conditions, growth trends
- Calculates similarity scores (0-100%)

**API Endpoint:**
```
GET /api/ml/similar-children/{child_id}?n=5
```

**Use Case:**
- Learn from successful interventions
- Group children for targeted programs
- Share best practices across similar profiles

---

### 5. **Weekly Meal Variety Optimizer**
Creates diverse weekly meal plans with balanced nutrition.

**How it works:**
- Uses ML recommendations as input
- Ensures ingredient diversity (no repetition)
- Balances categories across days
- Optimizes for nutrition and cost

**API Endpoint:**
```
GET /api/ml/weekly-variety/{child_id}?days=7
```

**Features:**
- 7-day meal plan generation
- Automatic variety management
- Category balancing (grains, proteins, vegetables, etc.)
- Prevents ingredient fatigue

---

### 6. **Ingredient Acceptance Predictor**
Predicts whether a child will accept a specific ingredient.

**How it works:**
- Analyzes consumption patterns of similar children
- Calculates acceptance probability
- Provides confidence score
- Explains reasoning

**API Endpoint:**
```
GET /api/ml/predict-acceptance/{child_id}/{ingredient_name}
```

**Returns:**
- Acceptance percentage (0-100%)
- Recommendation strength (High/Medium/Low)
- Number of similar children analyzed
- Nutritional priorities explanation

---

### 7. **ML Child Profile**
Comprehensive profile with nutritional priorities.

**How it works:**
- Calculates BMI and growth trends
- Determines nutritional priorities based on:
  - Age group
  - Weight trend (gaining/losing)
  - BMI category
  - Health conditions
  
**Priority Levels:**
- **High**: Critical nutritional need
- **Medium**: Important for balanced diet
- **Low**: Adequate intake

**API Endpoint:**
```
GET /api/ml/child-profile/{child_id}
```

---

## 🎯 How to Use ML Recommendations

### **Step 1: Access ML Page**
Navigate to: http://127.0.0.1:5000/ml-recommendations

### **Step 2: Select Child**
Choose a child from the dropdown menu

### **Step 3: View Recommendations**
- **Recommendations Tab**: See hybrid, collaborative, or content-based suggestions
- **Similar Children Tab**: Find children with similar profiles
- **Weekly Variety Tab**: Generate 7-day diverse meal plan
- **Acceptance Predictor Tab**: Test specific ingredients
- **ML Profile Tab**: View nutritional priorities

### **Step 4: Generate Meal Plan**
Use the recommendations to create optimal meal plans:
1. Copy top recommended ingredients
2. Use "Plan Meals" feature on home page
3. Enter child details and budget
4. System will optimize based on ML recommendations

---

## 📊 Technical Details

### **Algorithms Used:**
1. **K-Nearest Neighbors (KNN)**: For finding similar children
2. **Cosine Similarity**: For ingredient matching
3. **Truncated SVD**: For dimensionality reduction
4. **StandardScaler**: For feature normalization

### **Features Analyzed:**
**Child Profile:**
- Age, weight, height, gender
- Growth trends (weight/height change over time)
- Meal history (cost, nutrition score)
- Health conditions

**Ingredient Features:**
- Nutritional content (protein, carbs, fat, calories)
- Micronutrients (iron, calcium, fiber)
- Cost per kg
- Category

### **Model Training:**
```python
from ml_recommender import initialize_recommender

# Initialize and train all models
recommender = initialize_recommender()

# Get recommendations
recommendations = recommender.get_hybrid_recommendations(child_id=1, top_n=15)
```

---

## 🔄 Model Updates

### **Automatic Retraining:**
Models retrain automatically when:
- New children are added
- New meal plans are created
- Growth measurements are updated

### **Manual Training:**
```
POST /api/ml/train-models
```

---

## 💡 Best Practices

### **For ASHA Workers:**
1. ✅ Use **Hybrid Recommendations** for best results
2. ✅ Check **Acceptance Predictor** before introducing new foods
3. ✅ Review **Similar Children** to learn from successful cases
4. ✅ Generate **Weekly Variety** to avoid monotonous meals

### **For Data Quality:**
1. ✅ Record accurate meal plans and outcomes
2. ✅ Update growth measurements regularly
3. ✅ Document health conditions
4. ✅ Track ingredient acceptance

### **For Optimal Results:**
1. ✅ Need at least 5-10 children in database for collaborative filtering
2. ✅ Need 2-3 meal plans per child for pattern recognition
3. ✅ Regular updates improve recommendations
4. ✅ Diverse data leads to better predictions

---

## 🚀 Future Enhancements

### **Planned Features:**
- [ ] Deep Learning models (Neural Networks)
- [ ] Time series forecasting for growth prediction
- [ ] Image recognition for food photos
- [ ] Multi-language NLP for voice commands
- [ ] Reinforcement learning for adaptive planning
- [ ] Clustering for village-level insights

---

## 📈 Performance Metrics

### **Recommendation Quality:**
- **Precision**: How many recommended items are relevant
- **Recall**: How many relevant items are recommended
- **Diversity**: Variety in recommendations
- **Novelty**: Introduction of new beneficial foods

### **Model Accuracy:**
Track via:
- Nutrition score improvements
- Meal plan acceptance rates
- Growth trajectory alignment
- Cost efficiency

---

## 🆘 Troubleshooting

### **No Recommendations Showing:**
- Ensure child exists in database
- Check if meal history is available
- Verify at least 5 children in system

### **Low Acceptance Predictions:**
- Normal for new/uncommon ingredients
- Based on limited data initially
- Improves with more meal records

### **Similar Children Not Found:**
- Need diverse child profiles in database
- Check if features are properly recorded
- Ensure growth measurements exist

---

## 📞 API Reference Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/ml/recommendations/{child_id}` | GET | Get ML recommendations |
| `/api/ml/similar-children/{child_id}` | GET | Find similar children |
| `/api/ml/weekly-variety/{child_id}` | GET | Generate weekly plan |
| `/api/ml/predict-acceptance/{child_id}/{ingredient}` | GET | Predict acceptance |
| `/api/ml/child-profile/{child_id}` | GET | Get ML profile |
| `/api/ml/train-models` | POST | Retrain models |

---

## ✅ Success Indicators

**You're using ML effectively when:**
1. ✅ Nutrition scores improve over time
2. ✅ Meal acceptance rates increase
3. ✅ Budget utilization optimizes
4. ✅ Growth trajectories improve
5. ✅ Variety in weekly meals increases
6. ✅ ASHA workers report easier planning

---

**ML Recommendation System v1.0**
*Powered by scikit-learn, pandas, and numpy*
