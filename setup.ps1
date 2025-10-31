# AI Nutrition Advisor - Setup Script
# Run this script to set up the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Nutrition Advisor - Setup Script  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Host "✗ Python 3.8 or higher required!" -ForegroundColor Red
            Write-Host "  Please install Python 3.8+ from python.org" -ForegroundColor Yellow
            exit 1
        }
    }
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from python.org" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check pip
Write-Host "Checking pip installation..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ Found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip not found!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Ask about virtual environment
Write-Host "Do you want to create a virtual environment? (Recommended)" -ForegroundColor Yellow
Write-Host "[Y] Yes  [N] No  (default is Y): " -NoNewline -ForegroundColor Cyan
$createVenv = Read-Host

if ($createVenv -eq "" -or $createVenv -eq "Y" -or $createVenv -eq "y") {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    
    if (Test-Path "venv") {
        Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
    } else {
        python -m venv venv
        if ($?) {
            Write-Host "✓ Virtual environment created" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    
    # Check execution policy
    $executionPolicy = Get-ExecutionPolicy -Scope CurrentUser
    if ($executionPolicy -eq "Restricted") {
        Write-Host "Setting execution policy..." -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "✓ Execution policy updated" -ForegroundColor Green
    }
    
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan
Write-Host ""

pip install -r requirements.txt --quiet --disable-pip-version-check

if ($?) {
    Write-Host "✓ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Some dependencies failed to install" -ForegroundColor Red
    Write-Host "  Try running manually: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python database.py

if ($?) {
    Write-Host "✓ Database initialized successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to initialize database" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Success message
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup completed successfully! 🎉     " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  1. Activate virtual environment (if not already):" -ForegroundColor White
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Start the application:" -ForegroundColor White
Write-Host "     streamlit run app.py" -ForegroundColor Yellow
Write-Host ""

Write-Host "Quick start:" -ForegroundColor Cyan
Write-Host "  streamlit run app.py" -ForegroundColor Yellow
Write-Host ""

# Ask if user wants to start now
Write-Host "Do you want to start the application now? [Y/N] (default is Y): " -NoNewline -ForegroundColor Cyan
$startNow = Read-Host

if ($startNow -eq "" -or $startNow -eq "Y" -or $startNow -eq "y") {
    Write-Host ""
    Write-Host "Starting AI Nutrition Advisor..." -ForegroundColor Green
    Write-Host "The app will open in your browser automatically" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 2
    streamlit run app.py
} else {
    Write-Host ""
    Write-Host "Setup complete! Run 'streamlit run app.py' when ready." -ForegroundColor Green
    Write-Host ""
}
