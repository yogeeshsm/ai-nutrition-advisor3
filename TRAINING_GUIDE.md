# 🎓 **TRAIN YOUR OWN FOOD RECOGNITION MODEL**

## ✅ **No Fake APIs - Real Custom Training!**

This guide helps you train a **custom AI model** on **YOUR own food images**. No pre-trained generic models, no fake predictions - real training on real Indian food data!

---

## 📸 **Step 1: Collect Your Dataset**

### **How Many Images Do You Need?**

| Quality | Images per Food | Total (10 foods) | Model Accuracy |
|---------|----------------|------------------|----------------|
| **Minimum** | 20-30 | 200-300 | ~60-70% |
| **Good** | 50-100 | 500-1000 | ~75-85% |
| **Excellent** | 100-200 | 1000-2000 | ~85-95% |

### **Tips for Good Images:**

✅ **DO:**
- Take photos in good lighting
- Multiple angles of same food
- Different portion sizes
- Various plates/bowls
- Real meal photos (not stock images)
- Different cooking styles

❌ **DON'T:**
- Use blurry photos
- Mix multiple foods in one category
- Use very dark/overexposed images
- Download random internet images (unless verified)

### **Example Dataset Collection:**

```
For "Rice":
- 10 photos: small bowl of rice
- 10 photos: medium plate of rice
- 10 photos: large serving
- 10 photos: different rice types (white, brown)
- 10 photos: different lighting conditions
Total: 50 images
```

---

## 📁 **Step 2: Organize Your Dataset**

### **Automatic Setup:**

```bash
python prepare_dataset.py
```

Then choose **Option 1** to create folder structure.

### **Manual Setup:**

Create this folder structure:

```
ai nutrition advisor3w/
└── dataset/
    ├── train/
    │   ├── rice/
    │   │   ├── rice_001.jpg
    │   │   ├── rice_002.jpg
    │   │   └── ... (50-100 images)
    │   ├── ragi_ball/
    │   │   ├── ragi_001.jpg
    │   │   └── ...
    │   ├── dal/
    │   ├── egg/
    │   ├── banana/
    │   ├── chapati/
    │   ├── chicken_curry/
    │   ├── milk/
    │   ├── yogurt/
    │   └── vegetable_curry/
    └── validation/
        ├── rice/ (20% of images)
        ├── ragi_ball/
        └── ... (same structure)
```

### **Easy Workflow:**

1. **Collect all images** → Put in `dataset/train/<food_name>/`
2. **Run splitter:**
   ```bash
   python prepare_dataset.py
   # Choose Option 2: Split dataset
   ```
3. **Validate:**
   ```bash
   python prepare_dataset.py
   # Choose Option 3: Validate dataset
   ```

---

## 🎓 **Step 3: Train the Model**

### **Install Dependencies:**

```bash
pip install tensorflow==2.15.0 matplotlib scikit-learn
```

**For CPU only (most users):**
```bash
pip install tensorflow-cpu==2.15.0
```

### **Start Training:**

```bash
python train_food_model.py
```

### **What Happens:**

1. ✅ **Dataset Check** - Verifies your images
2. ✅ **Data Augmentation** - Creates variations automatically
3. ✅ **Model Building** - Creates custom neural network
4. ✅ **Phase 1 Training** - Trains classification layers (10 epochs)
5. ✅ **Phase 2 Fine-tuning** - Refines entire model (10 epochs)
6. ✅ **Validation** - Tests accuracy
7. ✅ **Model Saving** - Saves to `models/food_model.h5`

### **Training Time:**

| Hardware | Time (20 epochs, 500 images) |
|----------|------------------------------|
| **GPU** | 10-20 minutes |
| **CPU** | 1-2 hours |

### **Training Output:**

```
==============================================================
FOOD RECOGNITION MODEL TRAINING
Custom Indian Food Dataset
==============================================================

📊 Dataset Statistics:
--------------------------------------------------------------
✅ rice                  Train:  80   Val:  20
✅ ragi_ball             Train:  76   Val:  19
✅ dal                   Train:  82   Val:  21
...
--------------------------------------------------------------
Total:                  Train: 800   Val: 200

==============================================================
TRAINING MODEL
==============================================================

📊 Phase 1: Training custom layers (base model frozen)
Epoch 1/10
25/25 [==============================] - 45s - loss: 1.8234 - accuracy: 0.4125 - val_loss: 1.2156 - val_accuracy: 0.6250
Epoch 2/10
25/25 [==============================] - 42s - loss: 0.9876 - accuracy: 0.7250 - val_loss: 0.6543 - val_accuracy: 0.8125
...

✅ Model saved to: models/food_model.h5

📊 Final Results:
   Validation Loss: 0.2134
   Validation Accuracy: 92.50%

✅ Excellent! Model is ready for deployment
```

---

## 📊 **Step 4: Evaluate Your Model**

### **Check Training Plots:**

After training, check `models/training_history.png`:

- **Accuracy Plot** - Should increase over time
- **Loss Plot** - Should decrease over time
- **No overfitting** - Training and validation should be close

### **Good vs Bad Training:**

**✅ GOOD (Ready to Use):**
```
Validation Accuracy: 85-95%
Training and validation curves are close
Validation loss is stable/decreasing
```

**⚠️ NEEDS IMPROVEMENT:**
```
Validation Accuracy: < 70%
Large gap between training/validation
Validation loss increasing (overfitting)
```

**Solutions:**
- Collect more images
- Improve image quality
- Remove mislabeled images
- Train for more epochs

---

## 🚀 **Step 5: Use Your Trained Model**

### **Test the Model:**

```bash
python test_food_recognition.py
```

### **Start the Web App:**

```bash
python flask_app.py
```

Visit: **http://localhost:5000/food-recognition**

### **Now Your Model:**
- ✅ Uses **YOUR images**
- ✅ Predicts **YOUR food categories**
- ✅ Gives **real accuracy scores**
- ✅ No fake API calls!

---

## 🔧 **Advanced: Improve Your Model**

### **1. Collect More Data**
- Add 50 more images per category
- Retrain the model
- Watch accuracy improve!

### **2. Fix Misclassifications**
- Check which foods are confused
- Add more examples of those foods
- Ensure clear differences in images

### **3. Add New Foods**
1. Add new category to `INDIAN_FOOD_DATABASE` in `food_recognition.py`
2. Create folder in `dataset/train/new_food/`
3. Add images
4. Retrain model

### **4. Hyperparameter Tuning**

Edit `train_food_model.py`:

```python
# More epochs for better training
EPOCHS = 30  # instead of 20

# Larger batch size (if you have GPU)
BATCH_SIZE = 64  # instead of 32

# Different learning rates
learning_rate=0.0005  # experiment
```

---

## 📋 **Complete Workflow Summary**

```
Step 1: Collect Images (50-100 per food)
   ↓
Step 2: Organize Dataset
   → python prepare_dataset.py (Option 1 & 2)
   ↓
Step 3: Validate Dataset
   → python prepare_dataset.py (Option 3)
   ↓
Step 4: Train Model
   → python train_food_model.py
   ↓
Step 5: Check Accuracy
   → Look at training plots
   → Validation accuracy > 80%?
   ↓
Step 6: Test Model
   → python test_food_recognition.py
   ↓
Step 7: Deploy
   → python flask_app.py
   ↓
SUCCESS! 🎉
```

---

## ❓ **Troubleshooting**

### **Problem: "No images found"**
**Solution:** Make sure images are in correct folders with extensions `.jpg`, `.jpeg`, or `.png`

### **Problem: "Validation accuracy low (< 60%)"**
**Solution:** 
- Collect more images (aim for 100+ per category)
- Check image quality
- Remove mislabeled images
- Train for more epochs

### **Problem: "Training takes too long"**
**Solution:**
- Use fewer images initially (20 per category)
- Install `tensorflow-cpu` if you don't have GPU
- Reduce epochs to 10
- Increase batch size if you have RAM

### **Problem: "Out of memory"**
**Solution:**
- Reduce batch size: `BATCH_SIZE = 16`
- Close other applications
- Use smaller image size

### **Problem: "Model confuses certain foods"**
**Solution:**
- Add more distinct images of those foods
- Ensure foods look different in images
- Check if images are labeled correctly

---

## 📊 **Expected Results**

### **With 50 images per food:**
- Training time: ~1 hour (CPU)
- Validation accuracy: ~75-85%
- Good for testing and demo

### **With 100 images per food:**
- Training time: ~2 hours (CPU)
- Validation accuracy: ~85-92%
- Production-ready

### **With 200 images per food:**
- Training time: ~3-4 hours (CPU)
- Validation accuracy: ~90-95%
- Excellent performance

---

## 🎯 **What Makes This Real**

✅ **Custom Training** - Learns from YOUR data  
✅ **Transfer Learning** - Uses proven MobileNetV2 base  
✅ **Data Augmentation** - Creates variations automatically  
✅ **Two-Phase Training** - Optimal learning  
✅ **Validation** - Real accuracy metrics  
✅ **No Fake APIs** - Everything runs locally  

---

## 💡 **Where to Get Food Images?**

### **Best Sources:**
1. **Take your own photos** (most accurate)
2. **Local Anganwadi centers** (real meals)
3. **Community submissions** (crowd-sourced)
4. **Food delivery apps** (with permission)

### **Image Requirements:**
- Format: JPG, JPEG, or PNG
- Size: Any (will be resized to 224x224)
- Quality: Clear, well-lit, focused
- Content: Single food item per image

---

## 🎉 **You're Ready!**

Now you can train a **REAL food recognition model** with **REAL data** that gives **REAL results**!

**Start collecting images and train your first model!** 📸🎓

---

**Questions?** Check the training output for hints or run validation tool.
