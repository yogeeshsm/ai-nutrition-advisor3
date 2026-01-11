@echo off
echo ============================================================
echo AI NUTRITION ADVISOR - Full Application
echo ============================================================
echo.

REM Kill any existing Python servers on port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul

echo Starting server...
echo.

REM Start Python with unbuffered output
python -u quick_start.py

echo.
echo Server stopped.
pause
