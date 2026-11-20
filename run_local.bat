@echo off
title AmiCare Mental Wellness Platform
echo =========================================================
echo Starting AmiCare Local Server (Backend + OpenCV + Frontend)...
echo =========================================================
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in your PATH!
    pause
    exit /b 1
)

python run_local.py
pause
