@echo off
REM Persistent Flask Server Launcher
REM Works with Microsoft Store Python 3.13

echo ============================================================
echo AI NUTRITION ADVISOR - STARTING SERVER
echo ============================================================
echo.

cd /d "%~dp0"

:RETRY
echo Starting Flask server...
python -u quick_start.py
echo.
echo Server stopped. Exit code: %ERRORLEVEL%
echo.
if %ERRORLEVEL% NEQ 0 (
    echo Error detected. Retrying in 2 seconds...
    timeout /t 2 /nobreak > nul
    goto RETRY
)

echo Server closed normally.
pause
