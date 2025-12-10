# 📸 Food Image Recognition Feature - Documentation

## Overview

This feature uses Computer Vision and Machine Learning to:
- **Recognize food types** from images (Rice, Ragi, Dal, Egg, Banana, etc.)
- **Estimate portion sizes** (Small/Medium/Large)
- **Calculate nutritional values** (Calories, Protein, Carbs, Fats, Iron, Calcium)
- **Assess meal adequacy** against daily requirements for children

## 🧠 Technology Stack

### ML Model
- **MobileNetV2** - Efficient deep learning model optimized for mobile/low-end devices
- Pre-trained on ImageNet dataset
- Fine-tuned mapping to Indian food categories

### Key Features
1. **Food Classification** - Identifies 10+ common Indian foods
2. **Portion Estimation** - Analyzes image pixels to estimate serving size
3. **Nutrition Calculation** - Computes nutrients based on portion weight
4. **Requirement Assessment** - Compares against WHO/ICMR guidelines for children

## 📁 Files Created

### 1. `food_recognition.py` (Backend)
**Main ML Module** - Contains three core classes:

#### `FoodRecognitionModel`
- Loads MobileNetV2 model
- Preprocesses images (resize to 224x224, RGB conversion)
- Predicts food type using deep learning
- Maps predictions to Indian food database

```python
from food_recognition import FoodRecognitionModel

model = FoodRecognitionModel()
predictions = model.predict_food(image_data)
```

#### `PortionSizeEstimator`
- Analyzes image brightness and coverage
- Estimates portion: small (50-100g), medium (100-200g), large (200-300g)
- Returns average weight for nutrition calculation

```python
from food_recognition import PortionSizeEstimator

estimator = PortionSizeEstimator()
portion = estimator.estimate_from_image(image_data)
weight = estimator.get_portion_weight(portion)
```

#### `FoodNutritionCalculator`
- Combines food recognition + portion estimation
- Calculates nutritional values
- Assesses against daily requirements
- Generates personalized recommendations

```python
from food_recognition import analyze_food_image

result = analyze_food_image(image_bytes)
```

### 2. Flask API Endpoints (Added to `flask_app.py`)

#### `GET /food-recognition`
Renders the food recognition web interface

#### `POST /api/analyze-food-image`
Analyzes a single food image
- **Input**: multipart/form-data with 'image' file
- **Accepts**: PNG, JPG, JPEG, GIF, WEBP
- **Returns**: JSON with food type, portion, nutrition, recommendations

**Example Response:**
```json
{
  "success": true,
  "food_name": "Ragi Ball",
  "portion_size": "medium",
  "portion_weight": 150,
  "nutrition": {
    "calories": 504,
    "protein": 10.95,
    "carbs": 108,
    "fat": 1.95,
    "fiber": 5.4,
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

#### `POST /api/batch-analyze-food`
Analyzes multiple images (max 5) for complete meal analysis
- Returns individual results + aggregated nutrition totals

#### `GET /api/food-database`
Returns list of all supported foods with nutrition data

### 3. `templates/food_recognition.html` (Frontend)

**Modern, Interactive UI featuring:**
- Drag-and-drop image upload
- Camera capture support (mobile devices)
- Real-time image preview
- Beautiful results display with:
  - Food name and confidence
  - Portion size badge
  - Nutrition value cards
  - Progress bars for daily requirements
  - Personalized recommendations
  - Raw AI predictions (expandable)

**Responsive Design:**
- Mobile-first approach
- Touch-friendly controls
- Optimized for low-bandwidth

## 🍲 Supported Indian Foods

| Food | Category | Key Nutrients |
|------|----------|---------------|
| Rice | Grains | Carbs, Calories |
| Ragi Ball | Grains | Iron, Calcium, Fiber |
| Dal (Lentils) | Legumes | Protein, Iron, Fiber |
| Egg | Protein | Protein, Fats, Iron |
| Banana | Fruit | Carbs, Fiber |
| Chapati/Roti | Grains | Carbs, Protein, Fiber |
| Chicken Curry | Protein | Protein, Iron |
| Milk | Dairy | Calcium, Protein |
| Yogurt/Curd | Dairy | Calcium, Protein |
| Vegetable Curry | Vegetables | Fiber, Iron, Vitamins |

## 🎯 Portion Size Estimation

| Size | Weight Range | Multiplier | Use Case |
|------|-------------|------------|----------|
| Small | 50-100g | 0.5x | Toddler snack, Side dish |
| Medium | 100-200g | 1.0x | Regular child meal |
| Large | 200-300g | 1.5x | Main meal, Older child |

**Estimation Algorithm:**
1. Convert image to grayscale
2. Count bright pixels (likely food)
3. Calculate coverage ratio
4. Map to portion category

## 📊 Nutritional Assessment

Based on **WHO and ICMR guidelines** for children aged 1-6 years:

| Nutrient | Daily Requirement | Recommendation Threshold |
|----------|------------------|-------------------------|
| Calories | 1200 kcal | < 20% per meal = Low |
| Protein | 20g | < 25% per meal = Add protein |
| Iron | 10mg | < 15% per meal = Add iron-rich foods |
| Calcium | 600mg | < 15% per meal = Add dairy |

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key packages installed:**
- `tensorflow==2.15.0` - Deep learning framework
- `keras==2.15.0` - High-level neural networks API
- `Pillow==11.0.0` - Image processing (already installed)
- `numpy==1.26.4` - Numerical computing (already installed)

**For CPU-only systems:**
```bash
pip install tensorflow-cpu==2.15.0
```

### 2. Test the Feature

Run the test script:
```bash
python test_food_recognition.py
```

### 3. Start the Server
```bash
python flask_app.py
```

Visit: `http://localhost:5000/food-recognition`

## 🧪 Testing

### Test Script: `test_food_recognition.py`

Tests all components:
1. Model loading
2. Image preprocessing
3. Food prediction
4. Portion estimation
5. Nutrition calculation
6. Full pipeline integration

**Run:**
```bash
python test_food_recognition.py
```

### Manual Testing

1. **Test with Sample Image:**
   - Take a photo of rice, ragi, dal, or egg
   - Upload via web interface
   - Verify food type and nutrition values

2. **Test Camera Capture:**
   - On mobile device, tap "Use Camera"
   - Take photo of meal
   - Check real-time analysis

3. **Test Batch Analysis:**
   - Upload multiple food items
   - Verify total nutrition calculation

## 🎨 UI Features

### Upload Interface
- Clean, modern design with gradient backgrounds
- Drag-and-drop zone
- Camera button for mobile
- Image preview before analysis

### Results Display
- Animated card transitions
- Color-coded portion badges
- Nutrition grid with icons
- Progress bars for daily requirements
- Collapsible AI predictions section

### Mobile Optimization
- Touch-friendly buttons
- Responsive layout
- Camera access
- Fast loading

## 🔧 Customization

### Add New Foods

Edit `food_recognition.py`:

```python
INDIAN_FOOD_DATABASE = {
    'your_food': {
        'names': ['your_food', 'alternative_name'],
        'category': 'category',
        'nutrition_per_100g': {
            'calories': 100,
            'protein': 5,
            'carbs': 20,
            'fat': 2,
            'fiber': 3,
            'iron': 1,
            'calcium': 50
        }
    }
}
```

### Adjust Portion Sizes

Modify in `food_recognition.py`:

```python
PORTION_SIZES = {
    'small': {
        'multiplier': 0.5,
        'weight_range': (50, 100)  # Adjust range
    }
}
```

### Change Daily Requirements

Update in `FoodNutritionCalculator.assess_nutrition()`:

```python
daily_requirements = {
    'calories': 1500,  # Adjust for different age groups
    'protein': 25,
    'iron': 12,
    'calcium': 700
}
```

## 📱 Mobile App Integration

The API is ready for mobile app integration:

### Android/iOS Example:

```javascript
// React Native example
const formData = new FormData();
formData.append('image', {
  uri: imageUri,
  type: 'image/jpeg',
  name: 'food.jpg'
});

fetch('http://your-server/api/analyze-food-image', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  console.log(data.food_name);
  console.log(data.nutrition);
});
```

## 🔍 How It Works - Technical Details

### 1. Image Preprocessing
```python
# Resize to MobileNetV2 input size
image = image.resize((224, 224))

# Convert to RGB
if image.mode != 'RGB':
    image = image.convert('RGB')

# Normalize pixel values
img_array = preprocess_input(img_array)
```

### 2. Food Classification
```python
# MobileNetV2 prediction
predictions = model.predict(processed_image)

# Decode top-5 predictions
decoded = decode_predictions(predictions, top=5)

# Map to Indian food database
food_key, food_data = map_to_indian_food(decoded)
```

### 3. Portion Estimation
```python
# Analyze pixel coverage
gray_image = image.convert('L')
bright_pixels = count(pixels > 100)
coverage_ratio = bright_pixels / total_pixels

# Map to portion size
if coverage_ratio < 0.3:
    return 'small'
elif coverage_ratio < 0.6:
    return 'medium'
else:
    return 'large'
```

### 4. Nutrition Calculation
```python
# Scale nutrition by weight
multiplier = portion_weight / 100.0
nutrition = {
    'calories': base_calories * multiplier,
    'protein': base_protein * multiplier,
    # ... other nutrients
}
```

## 🎯 Future Enhancements

### Planned Features:
1. **Custom Model Training** - Train on Indian food dataset for better accuracy
2. **Ingredient Detection** - Identify multiple items in single image
3. **Calorie Counter** - Track daily intake across multiple meals
4. **Recipe Suggestions** - Recommend balanced meal combinations
5. **AR Portion Guide** - Augmented reality portion size reference
6. **Voice Commands** - "What's in this food?"
7. **Offline Mode** - TensorFlow Lite for offline mobile use

### Model Improvements:
- Fine-tune on Indian food dataset (10,000+ images)
- Add EfficientNet-B0 as alternative
- Implement object detection for multi-item plates
- Add depth estimation for more accurate portions

## 🐛 Troubleshooting

### Issue: Model not loading
**Solution:** Ensure TensorFlow is properly installed
```bash
pip install --upgrade tensorflow
```

### Issue: Low accuracy
**Solution:** Ensure good lighting and clear images. The model works best with:
- Well-lit photos
- Food centered in frame
- Minimal background clutter

### Issue: Slow predictions
**Solution:** Use TensorFlow CPU version for consistency
```bash
pip uninstall tensorflow
pip install tensorflow-cpu
```

### Issue: Out of memory
**Solution:** Reduce batch size or use lighter model:
```python
# In food_recognition.py
model = MobileNetV2(weights='imagenet', include_top=False)
```

## 📄 License

This feature is part of the AI Nutrition Advisor project.
MIT License - See LICENSE file.

## 🤝 Contributing

To improve food recognition:
1. Collect Indian food images
2. Label with food type and portion
3. Submit via pull request
4. Help expand food database

## 📞 Support

For issues or questions:
- Open GitHub issue
- Check documentation
- Review test scripts

---

**Created for:** AI Nutrition Advisor - Empowering communities with technology
**Technology:** MobileNetV2, TensorFlow, Flask, Computer Vision
**Purpose:** Helping parents ensure proper nutrition for their children
