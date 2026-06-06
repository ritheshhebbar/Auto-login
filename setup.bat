@echo off
title MSRIT Auto-Login Setup
cd /d "%~dp0"

echo =======================================
echo     MSRIT Auto-Login Setup
echo =======================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to your PATH!
    echo Please download and install Python from: https://www.python.org/downloads/
    echo Make sure to check the box: "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo 1. Checking and installing Selenium...
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo Installing selenium package...
    pip install selenium -q
    if errorlevel 1 (
        echo [ERROR] Failed to install selenium. Please check your internet connection.
        pause
        exit /b 1
    )
) else (
    echo selenium is already installed. Skipping installation.
)

echo 2. Creating Desktop shortcut...
powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'MSRIT Auto-Login.lnk')); $Shortcut.TargetPath = '%~dp0run_bot.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save();"

echo.
echo =======================================
echo Setup complete! 
echo A shortcut 'MSRIT Auto-Login' has been created on your Desktop.
echo This setup file will now self-delete.
echo =======================================
echo.
timeout /t 3 >nul

:: Self-deletion trick
(goto) 2>nul & del "%~f0"
