# 📦 Installation Guide - AI Nutrition Advisor

Complete step-by-step installation instructions for Windows

---

## 🎯 Prerequisites

Before you begin, ensure you have:

- ✅ Windows 10 or higher
- ✅ At least 2 GB free disk space
- ✅ Internet connection (for installation)
- ✅ Administrator privileges (optional, recommended)

---

## 📥 Step-by-Step Installation

### Method 1: Automated Installation (Easiest) ⭐ RECOMMENDED

#### Step 1: Check Python
```powershell
# Open PowerShell and check Python version
python --version
```

**Expected Output**: `Python 3.8.x` or higher

**If Python not found**:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, ✅ CHECK "Add Python to PATH"
3. Restart PowerShell

#### Step 2: Navigate to Project
```powershell
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
```

#### Step 3: Run Setup Script
```powershell
.\setup.ps1
```

**If you get execution policy error**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

#### Step 4: Wait for Setup
The script will:
- ✓ Check Python version
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Initialize database
- ✓ Ask to start the app

#### Step 5: Start Application
When prompted, press `Y` to start the application automatically.

---

### Method 2: Manual Installation

#### Step 1: Install Python

1. **Download Python**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.8 or higher
   - Run installer

2. **During Installation**:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
   - Click "Install Now"

3. **Verify Installation**:
```powershell
python --version
pip --version
```

#### Step 2: Open PowerShell

1. Press `Win + X`
2. Select "Windows PowerShell" or "Terminal"
3. Navigate to project folder:
```powershell
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
```

#### Step 3: Create Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Set execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**Confirmation**: Your prompt should show `(venv)` at the beginning.

#### Step 4: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**This will install**:
- streamlit
- pandas
- numpy
- plotly
- PuLP
- fpdf
- googletrans
- sqlite3-python
- openpyxl

**Wait time**: 2-5 minutes depending on internet speed

#### Step 5: Initialize Database

```powershell
python database.py
```

**Expected output**:
```
✅ Inserted 31 sample ingredients
✅ Database initialized successfully!
```

#### Step 6: Run Application

```powershell
streamlit run app.py
```

**Expected behavior**:
- Terminal shows "You can now view your Streamlit app in your browser"
- Browser automatically opens to `http://localhost:8501`
- Application interface appears

---

### Method 3: Minimal Installation (No Virtual Environment)

If you prefer not to use virtual environment:

```powershell
# 1. Navigate to project
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"

# 2. Install dependencies globally
pip install -r requirements.txt

# 3. Initialize database
python database.py

# 4. Run app
streamlit run app.py
```

---

## ✅ Verification

### Test Installation

Run the comprehensive test suite:
```powershell
python test_all.py
```

**Expected output**:
```
AI NUTRITION ADVISOR - COMPREHENSIVE TEST SUITE
================================================

Testing file structure...
✓ app.py
✓ database.py
...

TEST RESULTS SUMMARY
================================================

File Structure...................... ✅ PASSED
Imports............................. ✅ PASSED
Configuration....................... ✅ PASSED
Database............................ ✅ PASSED
...

🎉 ALL TESTS PASSED! Application is ready to use.
```

---

## 🚀 Running the Application

### First Time

```powershell
# Navigate to project
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"

# Activate virtual environment (if using)
.\venv\Scripts\Activate.ps1

# Run application
streamlit run app.py
```

### Subsequent Times

**Quick Method**:
```powershell
.\run.ps1
```

**Or**:
```powershell
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
streamlit run app.py
```

---

## 🔧 Troubleshooting Installation

### Issue: "Python not found"

**Solution**:
1. Install Python from python.org
2. Ensure "Add to PATH" was checked
3. Restart PowerShell
4. Try: `py --version` instead of `python --version`

### Issue: "pip not found"

**Solution**:
```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Issue: "Cannot activate virtual environment"

**Solution**:
```powershell
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activation again
.\venv\Scripts\Activate.ps1

# Or use different method
.\venv\Scripts\activate.bat
```

### Issue: "Package installation fails"

**Solution**:
```powershell
# Try with --user flag
pip install -r requirements.txt --user

# Or update pip and try again
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "ImportError" when running app

**Solution**:
```powershell
# Verify all packages installed
pip list

# Reinstall problematic package
pip install [package-name] --force-reinstall

# Or reinstall everything
pip install -r requirements.txt --force-reinstall
```

### Issue: "Port 8501 already in use"

**Solution**:
```powershell
# Option 1: Stop existing instance (Ctrl+C in terminal)

# Option 2: Use different port
streamlit run app.py --server.port 8502

# Option 3: Kill process
netstat -ano | findstr :8501
taskkill /PID [PID] /F
```

---

## 📋 Installation Checklist

Use this checklist to track your installation:

- [ ] Python 3.8+ installed
- [ ] pip working
- [ ] PowerShell opened
- [ ] Navigated to project folder
- [ ] Virtual environment created (optional)
- [ ] Virtual environment activated (if created)
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] No errors during dependency installation
- [ ] Database initialized (python database.py)
- [ ] Test suite passed (python test_all.py)
- [ ] Application starts (streamlit run app.py)
- [ ] Browser opens automatically
- [ ] Interface loads correctly

---

## 🎓 Understanding the Installation

### What Gets Installed?

1. **Streamlit** (1.28.0)
   - Web framework for the application
   - Creates the user interface
   - Handles routing and state management

2. **Pandas** (2.1.1)
   - Data manipulation and analysis
   - Handles ingredient data
   - Creates dataframes for display

3. **NumPy** (1.26.0)
   - Numerical computing
   - Array operations
   - Mathematical calculations

4. **Plotly** (5.17.0)
   - Interactive visualizations
   - Charts and graphs
   - Nutrition analysis displays

5. **PuLP** (2.7.0)
   - Linear programming solver
   - Core optimization engine
   - Meal plan generation

6. **FPDF** (1.7.2)
   - PDF generation
   - Export meal plans
   - Create printable reports

7. **Googletrans** (4.0.0rc1)
   - Language translation
   - Multi-language support
   - Text translation API

8. **SQLite3** (Built-in)
   - Database management
   - Store ingredients and plans
   - No separate installation needed

### File Structure After Installation

```
ai nutrition advisor3w/
├── venv/                      # Virtual environment (if created)
│   ├── Scripts/              # Python executables
│   ├── Lib/                  # Installed packages
│   └── ...
├── app.py                     # Main application
├── database.py               # Database operations
├── meal_optimizer.py         # Optimization engine
├── utils.py                  # Utility functions
├── config.py                 # Configuration
├── nutrition_advisor.db      # SQLite database (created)
├── requirements.txt          # Dependencies list
├── README.md                 # Documentation
├── QUICK_START.md           # Quick reference
├── PROJECT_SUMMARY.md        # Project overview
├── TROUBLESHOOTING.md        # Troubleshooting guide
├── INSTALLATION.md           # This file
├── VISUAL_GUIDE.md          # UI guide
├── test_all.py              # Test suite
├── setup.ps1                # Setup script
├── run.ps1                  # Run script
├── LICENSE                   # License file
└── .gitignore               # Git ignore rules
```

---

## 🔄 Updating the Application

### Update Dependencies

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Update all packages
pip install -r requirements.txt --upgrade

# Or update specific package
pip install streamlit --upgrade
```

### Update Database

If ingredients are updated:
```powershell
# Backup current database
Copy-Item nutrition_advisor.db nutrition_advisor_backup.db

# Reinitialize
python database.py
```

---

## 🗑️ Uninstallation

### Remove Application

```powershell
# Navigate to parent folder
cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\"

# Delete entire folder
Remove-Item -Recurse -Force "ai nutrition advisor3w"
```

### Remove Python Packages (if installed globally)

```powershell
pip uninstall streamlit pandas numpy plotly pulp fpdf googletrans -y
```

---

## 💡 Tips for Successful Installation

1. **Use Virtual Environment**: Prevents conflicts with other projects
2. **Stable Internet**: Required for downloading packages
3. **Administrator Rights**: Some installations may require it
4. **Updated Windows**: Ensure Windows is up to date
5. **Antivirus**: May need to allow Python/PowerShell
6. **Disk Space**: Ensure at least 2 GB free space
7. **Close Other Apps**: Free up system resources

---

## 📞 Getting Help

If installation fails:

1. **Read error message carefully**
2. **Check TROUBLESHOOTING.md**
3. **Search error online**
4. **Verify Python version**: `python --version`
5. **Verify pip**: `pip --version`
6. **Check internet connection**
7. **Try running as administrator**

Still having issues? Include these details when asking for help:
- Python version
- Windows version
- Error message (full text)
- Steps you've tried
- Screenshot of error

---

## ✅ Success Indicators

You'll know installation was successful when:

- ✅ No red error messages
- ✅ All green checkmarks in test suite
- ✅ Browser opens to app automatically
- ✅ Can see "AI Nutrition Advisor" header
- ✅ Can select ingredients
- ✅ Can generate meal plan

---

## 🎉 Next Steps After Installation

1. **Read QUICK_START.md** for usage guide
2. **Run test generation** with recommended ingredients
3. **Explore Analytics Dashboard**
4. **Try different budgets and age groups**
5. **Export a sample meal plan**
6. **Customize ingredients in database.py**

---

**Installation Complete! 🎊**

You're now ready to generate nutritious meal plans for Anganwadi children!

Run: `streamlit run app.py` to start.

---

**Last Updated**: October 2025
