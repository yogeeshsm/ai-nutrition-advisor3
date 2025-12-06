# Railway Deployment Guide - AI Nutrition Advisor

## Quick Deploy to Railway.app

### Step 1: Prepare Your GitHub Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

### Step 2: Deploy on Railway

1. **Go to** [railway.app](https://railway.app)
2. **Click** "Start a New Project"
3. **Select** "Deploy from GitHub repo"
4. **Choose** your repository: `yogeeshsm/ai-nutrition-advisor3`
5. **Railway will auto-detect** Python and start building

### Step 3: Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```
# Required API Keys (Get your own keys from the providers)
GEMINI_API_KEY=your_gemini_api_key_here
USDA_API_KEY=your_usda_api_key_here
DATA_GOV_API_KEY=your_data_gov_api_key_here

# Flask Configuration
SECRET_KEY=nutrition-advisor-secret-key-2025
FLASK_ENV=production

# Database - Railway MySQL (Optional)
DB_TYPE=mysql
MYSQL_HOST=${{MYSQLHOST}}
MYSQL_PORT=${{MYSQLPORT}}
MYSQL_USER=${{MYSQLUSER}}
MYSQL_PASSWORD=${{MYSQLPASSWORD}}
MYSQL_DATABASE=${{MYSQLDATABASE}}
```

### Step 4: Add MySQL Database (Optional but Recommended)

1. **In Railway Dashboard**, click "+ New"
2. **Select** "Database" → "MySQL"
3. **Railway automatically** creates MySQL service and connects it
4. **Environment variables** are auto-injected (MYSQLHOST, MYSQLPORT, etc.)

### Step 5: Deploy!

1. **Railway automatically builds** and deploys your app
2. **Get your URL**: `https://your-app.up.railway.app`
3. **Done!** Your app is live 🎉

---

## Alternative: SQLite (No MySQL)

If you don't want MySQL, just set:
```
DB_TYPE=sqlite
```

Railway will use the local SQLite database (data persists with volumes).

---

## Deployment Files Created

✅ **Procfile** - Tells Railway how to start the app
✅ **railway.json** - Railway configuration
✅ **requirements.txt** - Already exists with all dependencies

---

## Monitoring & Logs

1. **View Logs**: Railway Dashboard → Deployments → View Logs
2. **Metrics**: CPU, Memory, Network usage shown in dashboard
3. **Custom Domain**: Settings → Domains → Add custom domain

---

## Troubleshooting

### Build Fails?
- Check Python version in `runtime.txt`
- Verify all dependencies in `requirements.txt`

### App Crashes?
- Check logs for errors
- Verify environment variables are set
- Ensure MySQL service is running (if using DB_TYPE=mysql)

### Slow Response?
- Upgrade Railway plan for more resources
- Increase workers in Procfile: `--workers 4`

---

## Cost

- **Hobby Plan**: $5/month - 512MB RAM, 1GB storage
- **Pro Plan**: $20/month - 8GB RAM, better performance
- **First $5 free** for new users

---

## Success Indicators

✅ Build completes successfully
✅ Deployment shows "Active"
✅ URL opens the app
✅ Language switcher works
✅ AI Chatbot responds
✅ MySQL connection successful (if enabled)

---

## Support

- Railway Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- GitHub Issues: Create issue in your repo
