# ⚡ RENDER DEPLOYMENT - QUICK REFERENCE

## 🎯 3-Minute Deploy Checklist

### Step 1: Prepare Code (30 seconds)
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Step 2: Create Service (1 minute)
1. Go to: https://dashboard.render.com/
2. Click: **New +** → **Web Service**
3. Connect: Your GitHub repository

### Step 3: Configure (1 minute)
| Setting | Value |
|---------|-------|
| Name | `ai-nutrition-advisor` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn flask_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |

### Step 4: Environment Variables (30 seconds)
Click **Advanced** and add:

```bash
PYTHON_VERSION=3.11.9
FLASK_ENV=production
DB_TYPE=sqlite
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
USDA_API_KEY=your-usda-api-key
DATA_GOV_API_KEY=your-data-gov-api-key
```

### Step 5: Deploy! (30 seconds)
Click: **Create Web Service**

---

## 🔗 Important Links

- **Render Dashboard**: https://dashboard.render.com/
- **Your App URL**: `https://[your-service-name].onrender.com`
- **Health Check**: `https://[your-service-name].onrender.com/health`
- **Logs**: Check in Render dashboard → Your service → Logs

---

## ✅ Post-Deploy Tests

Test these URLs after deployment:

1. Homepage: `/`
2. Health Check: `/health`
3. Chatbot: `/chatbot`
4. ML Recommendations: `/ml-recommendations`
5. Food Recognition: `/food-recognition`

---

## 🐛 Quick Fixes

### Build Failed?
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies

### App Not Starting?
- Check environment variables are set
- Verify `GEMINI_API_KEY` is correct

### App Sleeping?
- Normal on free tier after 15 min
- First request wakes it up (takes 30s)
- Upgrade to $7/month for always-on

### Database Errors?
- Database auto-initializes on first run
- Check logs for specific errors

---

## 📱 One-Click Deploy

Use this button in your GitHub README:

```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/ai-nutrition-advisor3)
```

---

## 🎉 Success Checklist

After deployment, verify:

- [ ] App loads at your Render URL
- [ ] Health check returns: `{"status": "healthy"}`
- [ ] Homepage shows meal planner
- [ ] Can add children in Growth Tracking
- [ ] Chatbot responds (if API key valid)
- [ ] ML recommendations load
- [ ] Food recognition works

---

## 📚 Full Documentation

- **Complete Guide**: [RENDER_DEPLOY_GUIDE.md](RENDER_DEPLOY_GUIDE.md)
- **All Options**: [DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md)
- **Railway**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

---

## 💡 Pro Tips

1. **Custom Domain**: Add in Render → Settings → Custom Domains
2. **Auto-Deploy**: Enabled by default on git push
3. **Rollback**: Click "Manual Deploy" → Choose previous commit
4. **Scale Up**: Upgrade to Starter ($7/mo) for better performance
5. **Monitor**: Check usage in Render dashboard

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "Module not found" | Add to `requirements.txt` |
| "Port already in use" | Render handles this automatically |
| "Database locked" | Restart service |
| "API quota exceeded" | Get new Gemini API key |
| "Build timeout" | Use `tensorflow-cpu` (already set) |

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com
- **GitHub Issues**: Open an issue in your repo

---

**Your app will be live in ~5 minutes!** 🚀

Good luck! 🎉
