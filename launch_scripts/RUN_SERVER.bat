@echo off
title AI Nutrition Advisor - Full Features Server
cd /d "%~dp0"
echo ============================================================
echo Starting AI Nutrition Advisor with ALL 60+ Features
echo ============================================================
python app_full.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Server failed to start
    echo Error code: %ERRORLEVEL%
    echo.
)
pause
