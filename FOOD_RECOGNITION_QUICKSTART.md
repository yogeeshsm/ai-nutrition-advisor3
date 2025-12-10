# 🚀 Quick Start - Food Image Recognition

## Installation (3 Steps)

### 1. Install ML Dependencies
```bash
pip install tensorflow==2.15.0 keras==2.15.0
```

**For CPU-only systems (recommended for most users):**
```bash
pip install tensorflow-cpu==2.15.0
```

### 2. Run Tests
```bash
python test_food_recognition.py
```

Expected output: All 9 tests should pass ✅

### 3. Start Server
```bash
python flask_app.py
```

Visit: **http://localhost:5000/food-recognition**

---

## Quick Usage

### Web Interface
1. Go to `http://localhost:5000/food-recognition`
2. Click "Choose Image" or "Use Camera"
3. Select a food photo
4. Click "Analyze Food"
5. View nutrition results!

### API Usage

**Python:**
```python
import requests

with open('food_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post(
        'http://localhost:5000/api/analyze-food-image',
        files=files
    )
    result = response.json()
    print(f"Food: {result['food_name']}")
    print(f"Calories: {result['nutrition']['calories']}")
```

**cURL:**
```bash
curl -X POST http://localhost:5000/api/analyze-food-image \
  -F "image=@food_photo.jpg"
```

**JavaScript:**
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/api/analyze-food-image', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  console.log('Food:', data.food_name);
  console.log('Nutrition:', data.nutrition);
});
```

---

## Supported Foods

✅ **10 Common Indian Foods:**
- 🍚 Rice
- 🫘 Ragi Ball (Finger Millet)
- 🥘 Dal (Lentils)
- 🥚 Egg
- 🍌 Banana
- 🫓 Chapati/Roti
- 🍗 Chicken Curry
- 🥛 Milk
- 🥣 Yogurt/Curd
- 🥗 Vegetable Curry

---

## What You Get

For each food image:
- ✅ Food type identification
- ✅ Portion size (small/medium/large)
- ✅ Weight estimation (grams)
- ✅ Calories
- ✅ Protein, Carbs, Fats
- ✅ Iron & Calcium
- ✅ Daily requirement percentages
- ✅ Personalized recommendations

---

## Example Output

**Input:** Photo of ragi ball

**Output:**
```json
{
  "food_name": "Ragi Ball",
  "portion_size": "medium",
  "portion_weight": 150,
  "nutrition": {
    "calories": 504,
    "protein": 10.95,
    "carbs": 108,
    "fat": 1.95,
    "iron": 5.85,
    "calcium": 516
  },
  "nutritional_assessment": {
    "daily_percentages": {
      "calories": 42.0,
      "protein": 54.8,
      "iron": 58.5,
      "calcium": 86.0
    },
    "recommendations": [
      "✅ Well-balanced meal!"
    ]
  }
}
```

---

## Tips for Best Results

📸 **Photo Quality:**
- ✅ Good lighting
- ✅ Center the food
- ✅ Clear, focused image
- ✅ Plain background

❌ **Avoid:**
- Dark/blurry photos
- Multiple foods mixed
- Extreme angles
- Too much background clutter

---

## Troubleshooting

**Issue:** TensorFlow installation fails
```bash
# Solution: Use CPU version
pip install tensorflow-cpu==2.15.0
```

**Issue:** Model takes too long to load
```
# Normal: First load downloads ~14MB model
# Subsequent loads: Instant (cached)
```

**Issue:** Low accuracy
```
# Tips:
- Use clear, well-lit photos
- Center the food in frame
- Try different angles
- Ensure food is visible
```

---

## Next Steps

📖 **Read Full Documentation:** `FOOD_RECOGNITION_GUIDE.md`

🧪 **Run Tests:** `python test_food_recognition.py`

🔧 **Customize:** Edit `food_recognition.py` to add foods

📱 **Mobile App:** Use API endpoints for mobile integration

---

## Architecture

```
User Photo → MobileNetV2 → Food Classification
                           ↓
                    Portion Estimator
                           ↓
                    Nutrition Calculator
                           ↓
                    Daily Assessment
                           ↓
                    Recommendations
```

---

**Built with:** TensorFlow, MobileNetV2, Flask, Computer Vision

**Purpose:** Empowering parents to ensure proper child nutrition

**Ready to use!** 🎉
