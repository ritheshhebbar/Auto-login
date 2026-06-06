@echo off
title MSRIT Auto-Login
cd /d "%~dp0"



:: Run the login script
python msrit_login.py

:: Exit immediately after script finishes
exit
