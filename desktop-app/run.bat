@echo off
echo ========================================
echo Chemical Equipment Visualizer - Desktop App
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Checking dependencies...
pip show PyQt5 >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting desktop application...
echo Make sure the backend server is running on http://localhost:8000
echo.

python main.py

pause


