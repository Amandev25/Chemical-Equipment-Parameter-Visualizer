@echo off
echo ========================================
echo Chemical Equipment Visualizer - Desktop App Setup
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

python --version
echo.

echo [2/2] Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo   python main.py
echo.
echo Or use:
echo   run.bat
echo.
echo Make sure the backend server is running on http://localhost:8000
echo.
pause


