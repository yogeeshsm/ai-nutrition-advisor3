# Render Deployment Guide

## Quick Setup

### 1. Environment Variables in Render

Go to your Render dashboard → Your service → Environment tab and add:

```
GEMINI_API_KEY=AIzaSyBJARiL5ADGAJ9XhUzI_tAG5u724v6hbd4
DB_HOST=your_mysql_host
DB_USER=your_mysql_user  
DB_PASSWORD=your_mysql_password
DB_NAME=nutrition_advisor
SECRET_KEY=your_random_secret_key
```

### 2. Build Settings

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn flask_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### 3. Common Build Issues

#### Issue: "Exited with status 1"

**Causes:**
1. Missing environment variables
2. Large model files timing out
3. Memory limit exceeded

**Solutions:**

**Option A: Use environment variables (Recommended)**
```bash
# In Render dashboard, set:
GEMINI_API_KEY=AIzaSyBJARiL5ADGAJ9XhUzI_tAG5u724v6hbd4
```

**Option B: If model files are too large**

The trained model files in `models/malnutrition/` total ~4MB. If Render times out:

1. Add to `.gitignore`:
```
models/malnutrition/trained_model.pkl
```

2. Download model on first run:
```python
# In malnutrition_predictor.py, add fallback to retrain
if not os.path.exists(model_file):
    print("Model not found, using lightweight fallback...")
```

**Option C: Increase build timeout**

In Render dashboard:
- Settings → Build Command
- Add: `--timeout 600` (10 minutes)

### 4. Database Setup

**Option A: Use Render PostgreSQL**
1. Create PostgreSQL database in Render
2. Get connection string
3. Update `database.py` to use PostgreSQL instead of MySQL

**Option B: Use External MySQL (PlanetScale/Railway)**
1. Create free MySQL database
2. Get connection credentials
3. Add to Render environment variables

### 5. Verify Deployment

After successful build, test:

```bash
# Check health
curl https://your-app.onrender.com/health

# Test malnutrition prediction
curl -X POST https://your-app.onrender.com/api/predict-malnutrition/9 \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected response:
```json
{
  "success": true,
  "prediction": {
    "nutrition_status": "normal",
    "risk_level": "low",
    "confidence": 1.0
  }
}
```

### 6. Model Performance

- **Accuracy**: 93.90%
- **Training time**: 0.85 seconds
- **Key feature**: MUAC (59.39% importance)
- **Model size**: 4 MB

### 7. Troubleshooting

**Build fails with "No module named 'malnutrition_predictor'"**
- Check if `malnutrition_predictor.py` is committed
- Verify `models/malnutrition/trained_model.pkl` exists

**Runtime error: "Model not found"**
- Model files not included in deployment
- Use fallback or retrain on startup

**Database connection fails**
- Check environment variables are set
- Verify database is accessible from Render's IP

## Current Deployment Status

✅ GitHub: Pushed successfully (commit 1355a43)
✅ Model: Trained Random Forest (93.90% accuracy)
✅ API Key: AIzaSyBJARiL5ADGAJ9XhUzI_tAG5u724v6hbd4
⏳ Render: Waiting for environment variables

## Next Steps

1. Add `GEMINI_API_KEY` to Render environment
2. Trigger redeploy
3. Monitor build logs
4. Test API endpoints
