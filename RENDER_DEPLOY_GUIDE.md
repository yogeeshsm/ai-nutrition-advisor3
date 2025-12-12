# 🚀 Deploy AI Nutrition Advisor to Render

This guide will help you deploy your AI Nutrition Advisor application to Render for free.

## 📋 Prerequisites

1. A [Render account](https://render.com) (free tier available)
2. Your GitHub repository with this project
3. API keys ready:
   - Google Gemini API Key
   - USDA API Key (optional)
   - Data.gov.in API Key (optional)

## 🎯 Quick Deploy Steps

### Step 1: Push to GitHub

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `ai-nutrition-advisor3` repository

### Step 3: Configure Service

Use these settings:

| Setting | Value |
|---------|-------|
| **Name** | `ai-nutrition-advisor` (or your choice) |
| **Runtime** | `Python 3` |
| **Region** | Choose closest to your location |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn flask_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| **Instance Type** | `Free` |

### Step 4: Set Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.9` | Python version |
| `FLASK_ENV` | `production` | Production mode |
| `DB_TYPE` | `sqlite` | Database type |
| `SECRET_KEY` | `your-secret-key-here` | Generate random string |
| `GEMINI_API_KEY` | `your-gemini-api-key-here` | Get from [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `USDA_API_KEY` | `your-usda-api-key` | Optional - Get from [USDA FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html) |
| `DATA_GOV_API_KEY` | `your_data_gov_api_key_here` | Optional |

**🔐 Security Note**: Generate a strong SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for the build to complete
3. Your app will be live at `https://your-app-name.onrender.com`

## ✅ Post-Deployment Verification

After deployment, test these features:

1. **Homepage**: `https://your-app-name.onrender.com/`
2. **Chatbot**: `/chatbot`
3. **Food Recognition**: `/food-recognition`
4. **ML Recommendations**: `/ml-recommendations`
5. **Growth Tracking**: `/growth-tracking`

## 🔧 Deployment Files Created

- ✅ `render.yaml` - Render configuration
- ✅ `build.sh` - Build script
- ✅ `Procfile` - Process configuration
- ✅ `requirements.txt` - Updated for Render
- ✅ `runtime.txt` - Python version

## 📊 Free Tier Limits

Render's free tier includes:

- ✅ 750 hours/month (enough for 24/7 operation)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Auto-deploy from GitHub
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ 512 MB RAM (sufficient for this app)

## 🐛 Troubleshooting

### Build Fails

**Problem**: TensorFlow installation fails
**Solution**: Already using `tensorflow-cpu` (lighter version)

### Database Not Initializing

**Problem**: Database errors on startup
**Solution**: Check logs in Render dashboard, database auto-initializes

### API Key Errors

**Problem**: Gemini API quota exceeded
**Solution**: 
1. Get new API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Update in Render environment variables
3. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

### App Sleeping

**Problem**: First request takes 30+ seconds
**Solution**: This is normal on free tier. Consider:
- Upgrading to paid plan ($7/month for always-on)
- Using [UptimeRobot](https://uptimerobot.com/) to ping every 5 minutes

## 🔄 Updating Your App

To deploy updates:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect changes and redeploy.

## 📱 Custom Domain (Optional)

1. Go to your service settings
2. Click **"Custom Domains"**
3. Add your domain
4. Update DNS settings as shown

## 🎉 Alternative: One-Click Deploy

Click this button to deploy directly:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yogeeshsm/ai-nutrition-advisor3)

## 💡 Tips for Better Performance

1. **Enable Persistent Disk** (paid): Keeps SQLite database across restarts
2. **Use PostgreSQL** (free): Better for production, doesn't sleep
3. **Monitor Usage**: Check Render dashboard for metrics
4. **Set Up Alerts**: Get notified of deployment failures

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

## 🎯 Next Steps After Deployment

1. ✅ Test all 60+ features
2. ✅ Add test children via Growth Tracking
3. ✅ Test chatbot with nutrition questions
4. ✅ Upload food images for recognition
5. ✅ Generate meal plans
6. ✅ Share your app URL!

---

**Your app will be live at**: `https://ai-nutrition-advisor-[random].onrender.com`

Good luck! 🚀
