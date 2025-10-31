# Quick Run Script for AI Nutrition Advisor
# Double-click this file to start the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI Nutrition Advisor - Starting...   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists and activate it
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    Write-Host ""
}

# Check if database exists
if (-not (Test-Path "nutrition_advisor.db")) {
    Write-Host "Database not found. Initializing..." -ForegroundColor Yellow
    python database.py
    Write-Host ""
}

# Start the application
Write-Host "Starting Streamlit application..." -ForegroundColor Green
Write-Host "The app will open in your browser automatically" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
