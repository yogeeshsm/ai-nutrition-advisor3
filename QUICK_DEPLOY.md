# 🚀 Deploy to Railway in 5 Minutes

## Step-by-Step Guide

### 1️⃣ Push to GitHub (if not already done)

```bash
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2️⃣ Deploy on Railway

1. Go to **https://railway.app**
2. Click **"Login with GitHub"**
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose **"yogeeshsm/ai-nutrition-advisor3"**
6. Railway automatically detects Python and starts deploying! ✨

### 3️⃣ Add Environment Variables

Click on your deployed service → **Variables** tab → **RAW Editor** → Paste:

```
GEMINI_API_KEY=AIzaSyC5arnzs6fKIyQgo4MmyIgz-Cr31DhBA0s
USDA_API_KEY=bI8E0Icmi3gYlneZJ27MWK6ChaaUYBCn2Vv801NH
DATA_GOV_API_KEY=579b464db66ec23bdd000001e3f853bd7199484e65326b922dbca7ce
SECRET_KEY=nutrition-advisor-secret-key-2025
FLASK_ENV=production
DB_TYPE=sqlite
```

Click **Save** → Railway redeploys automatically!

### 4️⃣ Get Your URL

- Railway provides a URL like: `https://ai-nutrition-advisor3-production.up.railway.app`
- Click **Settings** → **Networking** → **Generate Domain**
- Your app is LIVE! 🎉

---

## 🎯 Want MySQL Database?

### Add MySQL in 30 seconds:

1. In Railway dashboard, click **"+ New"**
2. Select **"Database"** → **"MySQL"**
3. Update your environment variables:

```
DB_TYPE=mysql
MYSQL_HOST=${{MYSQLHOST}}
MYSQL_PORT=${{MYSQLPORT}}
MYSQL_USER=${{MYSQLUSER}}
MYSQL_PASSWORD=${{MYSQLPASSWORD}}
MYSQL_DATABASE=${{MYSQLDATABASE}}
```

Railway auto-fills these variables! Just paste and save.

---

## ✅ Verification Checklist

After deployment:

- [ ] URL opens successfully
- [ ] Homepage loads with "AI Nutrition Advisor"
- [ ] Language switcher works (try Kannada!)
- [ ] AI Chatbot responds
- [ ] Meal planner generates plans
- [ ] No errors in Railway logs

---

## 🆘 Troubleshooting

**Build Failed?**
- Check logs in Railway dashboard
- Verify requirements.txt has all dependencies

**App Crashes?**
- Check environment variables are set correctly
- View logs for error messages

**500 Error?**
- Database connection issue - verify DB_TYPE matches your setup
- Check API keys are valid

---

## 💰 Cost

- **$5/month** (Hobby plan) - Perfect for this app
- **First $5 FREE** for new users
- Can handle 100+ concurrent users

---

## 🎊 That's It!

Your AI Nutrition Advisor is now deployed and accessible worldwide!

Share your URL: `https://your-app.up.railway.app`
