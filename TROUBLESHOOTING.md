# 🔧 Troubleshooting Guide - AI Nutrition Advisor

## Common Issues and Solutions

### 1. Installation Issues

#### Error: "Python is not recognized"
**Problem**: Python not installed or not in PATH

**Solution**:
```powershell
# Download and install Python 3.8+ from python.org
# During installation, check "Add Python to PATH"
# Restart PowerShell after installation
python --version  # Verify installation
```

#### Error: "pip is not recognized"
**Problem**: pip not installed or not in PATH

**Solution**:
```powershell
# Reinstall Python with pip option checked
# Or manually install pip:
python -m ensurepip --upgrade
```

#### Error: "execution policy"
**Problem**: PowerShell script execution disabled

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 2. Dependency Issues

#### Error: "No module named 'streamlit'"
**Problem**: Dependencies not installed

**Solution**:
```powershell
pip install -r requirements.txt
# Or install individually:
pip install streamlit pandas numpy plotly pulp fpdf googletrans==4.0.0rc1
```

#### Error: "ImportError: cannot import name..."
**Problem**: Version conflicts

**Solution**:
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Reinstall all packages
pip uninstall -y streamlit pandas numpy plotly pulp fpdf googletrans
pip install -r requirements.txt
```

#### Error: "Microsoft Visual C++ required" (Windows)
**Problem**: Missing build tools for some packages

**Solution**:
```powershell
# Option 1: Install pre-built wheels
pip install --only-binary :all: -r requirements.txt

# Option 2: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

---

### 3. Database Issues

#### Error: "database is locked"
**Problem**: Database file is being accessed by another process

**Solution**:
```powershell
# Stop all running instances of the app (Ctrl+C)
# Close any database viewers/editors
# Restart the application
streamlit run app.py
```

#### Error: "no such table: ingredients"
**Problem**: Database not initialized

**Solution**:
```powershell
# Delete old database and reinitialize
Remove-Item nutrition_advisor.db
python database.py
```

#### Error: "IntegrityError: UNIQUE constraint failed"
**Problem**: Duplicate ingredient insertion

**Solution**:
```powershell
# The database is fine, just skip duplicate entries
# Or reset database:
Remove-Item nutrition_advisor.db
python database.py
```

---

### 4. Application Startup Issues

#### Error: "Address already in use"
**Problem**: Port 8501 already occupied

**Solution**:
```powershell
# Option 1: Kill existing process
# Find process on port 8501
netstat -ano | findstr :8501
# Kill it (replace PID)
taskkill /PID <PID> /F

# Option 2: Use different port
streamlit run app.py --server.port 8502
```

#### Error: "ModuleNotFoundError: No module named 'app'"
**Problem**: Running from wrong directory

**Solution**:
```powershell
# Navigate to project directory first
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
streamlit run app.py
```

#### App opens but shows blank page
**Problem**: JavaScript/browser issue

**Solution**:
- Clear browser cache (Ctrl+Shift+Delete)
- Try different browser (Chrome, Firefox, Edge)
- Disable browser extensions
- Check browser console for errors (F12)

---

### 5. Meal Plan Generation Issues

#### Error: "No ingredients available"
**Problem**: No ingredients selected

**Solution**:
- Select at least 5-7 ingredients before generating
- Use "Recommended" button for quick selection

#### Error: "Could not solve"
**Problem**: Constraints too strict (budget too low)

**Solutions**:
```
1. Increase budget (try ₹30-50 per child per day)
2. Select more common/cheaper ingredients
3. Reduce number of children for testing
4. Check if budget is in weekly amount (not daily)
```

#### Low Nutrition Score (<70)
**Problem**: Selected ingredients lack nutritional variety

**Solutions**:
- Include protein sources (dal, eggs, milk)
- Add green vegetables (spinach, etc.)
- Include dairy products
- Increase budget slightly
- Select ingredients from multiple categories

#### Optimization takes too long (>30 seconds)
**Problem**: Too many ingredients or complex constraints

**Solutions**:
- Select fewer ingredients (10-15 instead of all)
- Use "Basic Only" or "Recommended" selection
- Increase budget to loosen constraints
- Close other applications to free up CPU

---

### 6. Export Issues

#### PDF Export fails
**Problem**: FPDF encoding issues

**Solution**:
```powershell
# Reinstall fpdf
pip uninstall fpdf
pip install fpdf==1.7.2

# Or use CSV export instead
# Download as CSV and convert to PDF using Excel/Google Sheets
```

#### CSV shows garbled text
**Problem**: Encoding issue

**Solution**:
- Open CSV in Excel instead of Notepad
- When opening in Excel: Data → From Text → UTF-8 encoding
- Or use Google Sheets (better Unicode support)

---

### 7. Translation Issues

#### Translation not working
**Problem**: Network issue or googletrans API problem

**Solutions**:
```powershell
# Check internet connection
ping google.com

# Reinstall googletrans
pip uninstall googletrans
pip install googletrans==4.0.0rc1

# Or disable translation temporarily (use English only)
```

#### Translation shows weird characters
**Problem**: Font/encoding issue

**Solution**:
- Ensure browser supports Unicode
- Install language fonts if needed
- Use English mode if translations are problematic

---

### 8. Performance Issues

#### App is slow/laggy
**Problem**: Insufficient resources or too much data

**Solutions**:
- Close other applications
- Clear browser cache
- Reduce number of selected ingredients
- Delete old meal plans from database
- Restart application

#### High memory usage
**Problem**: Too many cached plans or large dataset

**Solution**:
```powershell
# Clear Streamlit cache
# Stop app (Ctrl+C)
# Delete cache folder
Remove-Item -Recurse -Force .streamlit/cache

# Restart app
streamlit run app.py
```

---

### 9. Display Issues

#### Charts not showing
**Problem**: Plotly not loading or JavaScript error

**Solutions**:
- Enable JavaScript in browser
- Disable ad blockers
- Update browser to latest version
- Try incognito/private mode
- Check browser console (F12) for errors

#### Layout broken/misaligned
**Problem**: CSS/Streamlit rendering issue

**Solutions**:
- Refresh page (Ctrl+R)
- Clear browser cache
- Update Streamlit: `pip install --upgrade streamlit`
- Try different browser

#### Emojis not displaying
**Problem**: Font support issue

**Solutions**:
- Update Windows (emojis require Windows 10+)
- Use modern browser (Chrome, Firefox, Edge)
- Update browser to latest version
- Disable emoji feature in config.py if needed

---

### 10. Data Issues

#### Incorrect nutritional values
**Problem**: Data entry error or calculation issue

**Solution**:
- Check database.py for ingredient data
- Verify calculations in meal_optimizer.py
- Cross-reference with ICMR guidelines
- Report issue with specific ingredient name

#### Cost seems unrealistic
**Problem**: Outdated or incorrect cost data

**Solution**:
- Update costs in database.py
- Modify `cost_per_kg` values for ingredients
- Run `python database.py` to reinitialize
- Or manually update in database:
```python
import sqlite3
conn = sqlite3.connect('nutrition_advisor.db')
cursor = conn.cursor()
cursor.execute("UPDATE ingredients SET cost_per_kg = 50 WHERE name = 'Rice'")
conn.commit()
```

---

## Advanced Troubleshooting

### Debug Mode

Enable debug information:

1. Edit `config.py`:
```python
DEV_CONFIG = {
    'debug_mode': True,
    'show_technical_details': True
}
```

2. Run with verbose output:
```powershell
streamlit run app.py --logger.level=debug
```

### Check Logs

View Streamlit logs:
```powershell
# Logs are shown in terminal where you ran streamlit
# Save logs to file:
streamlit run app.py 2>&1 | Tee-Object -FilePath app_log.txt
```

### Database Inspection

Inspect database directly:
```powershell
# Install DB Browser for SQLite
# Or use Python:
python
>>> import sqlite3
>>> conn = sqlite3.connect('nutrition_advisor.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT * FROM ingredients LIMIT 5")
>>> print(cursor.fetchall())
```

### Test Optimization

Test optimizer separately:
```powershell
python
>>> from meal_optimizer import MealOptimizer
>>> import database as db
>>> ingredients = db.get_all_ingredients()
>>> optimizer = MealOptimizer(ingredients, 2000, 20, "3-6 years")
>>> plan = optimizer.generate_meal_plan()
>>> print(plan['nutrition_score'])
```

---

## Getting Help

### Self-Help Resources

1. Check error message carefully
2. Read README.md and QUICK_START.md
3. Review code comments
4. Search online for specific error message

### Report Issues

When reporting issues, include:
- Python version: `python --version`
- OS: Windows version
- Error message (full text)
- Steps to reproduce
- Screenshot if applicable

### Contact

- GitHub Issues: [Repository URL]
- Email: [Your email]
- Documentation: README.md

---

## Preventive Measures

### Regular Maintenance

```powershell
# Update dependencies monthly
pip install --upgrade -r requirements.txt

# Backup database
Copy-Item nutrition_advisor.db nutrition_advisor_backup.db

# Clear old data
# Delete old meal plans (optional)
```

### Best Practices

1. Always use virtual environment
2. Keep Python and packages updated
3. Backup database before major changes
4. Test with small data first
5. Monitor system resources
6. Use version control (git)

---

## Quick Fixes Checklist

When something goes wrong:

- [ ] Restart the application (Ctrl+C, then run again)
- [ ] Refresh browser page (Ctrl+R)
- [ ] Clear browser cache
- [ ] Check internet connection (for translation)
- [ ] Verify Python version (3.8+)
- [ ] Reinstall dependencies
- [ ] Delete and reinitialize database
- [ ] Try different browser
- [ ] Check for Windows updates
- [ ] Restart computer (last resort)

---

## Known Limitations

1. **Translation**: Requires internet, may be slow
2. **Optimization**: Can take 10-20 seconds for many ingredients
3. **PDF Export**: Limited font support for non-English
4. **Browser**: Best on Chrome/Firefox/Edge
5. **Platform**: Optimized for Windows (may need adjustments for Mac/Linux)

---

## Tips for Smooth Operation

✅ **DO**:
- Use recommended ingredients for first time
- Start with reasonable budget (₹30-50/child/day)
- Select 10-15 ingredients for faster optimization
- Export plans regularly
- Keep browser updated

❌ **DON'T**:
- Don't select all ingredients at once (slow)
- Don't set budget too low (<₹20/child/day)
- Don't interrupt optimization process
- Don't modify database while app is running
- Don't forget to activate virtual environment

---

**Still Having Issues?**

Most problems are solved by:
1. Reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`
2. Resetting database: `Remove-Item nutrition_advisor.db; python database.py`
3. Restarting application: Stop and run `streamlit run app.py` again

If problem persists, check GitHub Issues or contact support.

---

**Last Updated**: October 2025
