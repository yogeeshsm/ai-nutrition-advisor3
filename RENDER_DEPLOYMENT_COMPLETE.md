# Render Deployment - Complete Guide

## ✅ Pre-Deployment Checklist

### 1. Code is Ready
- ✅ Trained ML model included (93.90% accuracy)
- ✅ Sample children data auto-initializes on first run
- ✅ SQLite database (works out of the box on Render)
- ✅ All dependencies in requirements.txt

### 2. Required Environment Variable

**CRITICAL:** Add this environment variable in Render dashboard:

```
GEMINI_API_KEY = your_gemini_api_key_here
```

**Where to add it:**
1. Go to: https://dashboard.render.com
2. Select your service: **ai-nutrition-advisor3-3**
3. Click: **Environment** tab
4. Click: **Add Environment Variable**
5. Add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your actual Gemini API key
6. Click: **Save Changes**

---

## 🚀 Deployment Settings

### Build Settings
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn flask_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Runtime
- **Python Version:** 3.13 (as specified in runtime.txt)

---

## 🔍 Verification Steps

### 1. Check Health Endpoint
After deployment completes, test:
```
https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AI Nutrition Advisor",
  "features": "60+",
  "database": "connected",
  "children_count": 15,
  "timestamp": "2025-12-11T..."
}
```

### 2. Check Children API
```
https://your-app.onrender.com/api/get-children
```

Expected response:
```json
{
  "success": true,
  "children": [
    {
      "id": 1,
      "name": "Lakshmi Iyer",
      "age": 5,
      "gender": "Female",
      "village": "Bangalore",
      ...
    },
    ...
  ]
}
```

### 3. Check Malnutrition Prediction
```
POST https://your-app.onrender.com/api/predict-malnutrition/1
```

Expected response:
```json
{
  "success": true,
  "child": {
    "id": 1,
    "name": "Lakshmi Iyer",
    ...
  },
  "prediction": {
    "nutrition_status": "normal",
    "risk_level": "low",
    "confidence": 1.0
  }
}
```

### 4. Check Full Dashboard
Open in browser:
```
https://your-app.onrender.com/malnutrition-prediction
```

Should show:
- ✅ 15 children in dropdown
- ✅ Realistic risk predictions (not all critical)
- ✅ Charts and visualizations

---

## 🎯 What Happens on First Deployment

1. **Database Initialization:**
   - SQLite database created automatically
   - All tables created (children, growth_tracking, immunisation, etc.)
   - Sample ingredients loaded

2. **Sample Data:**
   - 15 sample children auto-created
   - Growth tracking data for each child
   - Realistic weights/heights based on age

3. **ML Model:**
   - Trained Random Forest model loaded (93.90% accuracy)
   - Ready for predictions immediately

4. **All Features Active:**
   - Meal Planner
   - Malnutrition Predictor (with trained model)
   - Growth Tracking
   - Immunization Tracker
   - Health Information
   - Food Recognition
   - Chatbot (requires GEMINI_API_KEY)
   - And 50+ more features

---

## 🔧 Optional: Add MySQL Database

If you want to use MySQL instead of SQLite:

### 1. Add Environment Variables
```
DB_TYPE=mysql
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=nutrition_advisor
```

### 2. Create Database
Run this SQL on your MySQL server:
```sql
CREATE DATABASE nutrition_advisor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Run Migration
After deployment, trigger migration:
```bash
# This happens automatically on first connection
# Or manually run: python migrate_to_mysql.py
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Build Fails with "Exited with status 1"
**Cause:** Missing GEMINI_API_KEY environment variable
**Solution:** Add GEMINI_API_KEY in Environment tab (see step 2 above)

### Issue 2: No Children Showing
**Cause:** Database not initialized
**Solution:** This should not happen anymore! The app now auto-initializes sample data.
- Check health endpoint: `/health` should show `children_count: 15`
- If still empty, check logs for errors

### Issue 3: Chatbot Not Working
**Cause:** Missing or invalid GEMINI_API_KEY
**Solution:** 
1. Verify API key is correct
2. Check Gemini API quota at https://aistudio.google.com
3. Ensure you're using `gemini-2.0-flash` model

### Issue 4: Predictions Still Show "All Critical"
**Cause:** This was fixed! Should not happen anymore.
**Solution:** 
- Verify model files are in repo: `models/malnutrition/trained_model.pkl`
- Check startup logs for "[OK] Trained model loaded successfully"

---

## 📊 Expected Performance

### Response Times (Render Free Tier)
- Health endpoint: ~100ms
- Children API: ~200ms
- Malnutrition prediction: ~500ms
- Full dashboard page: ~1-2s

### Cold Start
- First request after idle: ~30-60 seconds
- Render free tier spins down after 15 minutes idle
- Consider upgrading to paid plan to avoid cold starts

---

## 🎉 Success Indicators

After deployment, you should see:

✅ Build completes without errors  
✅ Server starts successfully  
✅ Health endpoint returns status "healthy"  
✅ Database shows 15 children  
✅ Malnutrition predictions are realistic (not all critical)  
✅ Dashboard loads and shows all features  
✅ Trained model loaded (93.90% accuracy)  

---

## 📝 Quick Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Render Web Service
- [ ] Connect to GitHub repository
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `gunicorn flask_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
- [ ] Add environment variable: `GEMINI_API_KEY`
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes for build
- [ ] Test `/health` endpoint
- [ ] Test `/api/get-children` endpoint
- [ ] Open dashboard in browser
- [ ] Verify children dropdown has 15 entries
- [ ] Test malnutrition prediction
- [ ] Celebrate! 🎉

---

## 🆘 Need Help?

If something doesn't work:

1. **Check Render Logs:**
   - Go to your service → Logs tab
   - Look for error messages
   - Search for "[ERROR]" or "Traceback"

2. **Check Environment Variables:**
   - Environment tab should have GEMINI_API_KEY
   - Value should not be empty or "your_gemini_api_key_here"

3. **Test Locally First:**
   - Run `python flask_app.py` on your machine
   - If it works locally, it will work on Render
   - If it fails locally, fix it before deploying

4. **Verify Model Files:**
   - Check GitHub repo has `models/malnutrition/` folder
   - Should contain 3 files: trained_model.pkl, label_encoder.pkl, model_metadata.pkl

---

## 🔐 Security Notes

- ✅ API key removed from public repository
- ✅ API key stored in Render environment variables
- ✅ Database credentials (if using MySQL) stored as environment variables
- ✅ SECRET_KEY can be set as environment variable (optional)

**Never commit:**
- API keys
- Database passwords
- Secret keys
- `.env` files with real credentials

---

## 📈 Monitoring

### Logs to Watch
```
[OK] Trained model loaded successfully - ✅ Good
[OK] Database has 15 children already - ✅ Good
[OK] Chatbot initialized with gemini - ✅ Good
[WARNING] Chatbot not available - ⚠️ Check API key
[ERROR] - ❌ Investigate immediately
```

### Key Metrics
- Health endpoint response time
- Children API response time
- Prediction accuracy confidence
- Database query times
- Error rates

---

## ✨ Features Available After Deployment

1. **Meal Planner** - Generate optimized meal plans
2. **Malnutrition Predictor** - ML-powered risk assessment (93.90% accuracy)
3. **Growth Tracking** - Monitor child growth over time
4. **Immunization Tracker** - WHO vaccine schedule
5. **Health Information** - Disease prevention & treatment
6. **Food Recognition** - Image-based food identification
7. **Nutrition Lookup** - USDA nutrition database
8. **AI Chatbot** - Nutrition advice (requires API key)
9. **Village Economy** - Mandi price tracking
10. **Child Identity Cards** - QR-based digital ID cards
... and 50+ more features!

---

**Last Updated:** December 11, 2025  
**Version:** 2.0 (Production Ready)
