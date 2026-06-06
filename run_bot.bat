@echo off
title MSRIT Auto-Login
cd /d "%~dp0"

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Install Python from https://python.org
    pause
    exit /b 1
)

:: Install selenium if missing (fast — skips if already installed)
pip install selenium -q

:: Run the login script
python msrit_login.py

:: Exit immediately after script finishes
exit
