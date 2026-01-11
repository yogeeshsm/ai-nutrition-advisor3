@echo off
echo ========================================
echo   AI NUTRITION ADVISOR - SERVER START
echo ========================================
echo.
echo Stopping any running servers...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting server...
echo.
start "AI Nutrition Advisor" python flask_app.py

timeout /t 8 /nobreak >nul

echo.
echo ========================================
echo   SERVER STARTED!
echo ========================================
echo.
echo   Main Page: http://127.0.0.1:5000
echo   Malnutrition ML: http://127.0.0.1:5000/malnutrition-prediction
echo   Test Page: http://127.0.0.1:5000/test-dropdown
echo.
echo Press any key to open browser...
pause >nul
start http://127.0.0.1:5000/malnutrition-prediction
