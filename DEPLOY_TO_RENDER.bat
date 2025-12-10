@echo off
REM Quick script to commit and push for Render deployment

echo ========================================
echo   PREPARING FOR RENDER DEPLOYMENT
echo ========================================
echo.

REM Check if git is initialized
git status >nul 2>&1
if errorlevel 1 (
    echo Initializing git repository...
    git init
    git branch -M main
    echo.
    echo Please set your remote repository:
    echo git remote add origin YOUR_GITHUB_URL
    pause
    exit /b
)

echo Adding all files...
git add .

echo.
echo Committing changes...
git commit -m "Prepare for Render deployment - All 60+ features ready"

echo.
echo Current branch:
git branch --show-current

echo.
echo Ready to push? This will trigger deployment on Render.
pause

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   SUCCESS! Code pushed to GitHub
echo ========================================
echo.
echo Next steps:
echo 1. Go to: https://dashboard.render.com/
echo 2. Click: New + ^> Web Service
echo 3. Connect your GitHub repository
echo 4. Follow: RENDER_QUICK_START.md
echo.
pause
