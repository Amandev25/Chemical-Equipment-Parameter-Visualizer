@echo off
echo ========================================
echo Starting Chemical Equipment Visualizer Backend
echo ========================================
echo.

cd /d "%~dp0"

echo Checking virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Starting Django development server...
echo.
echo Server will be available at:
echo   - API: http://localhost:8000/api/
echo   - Swagger: http://localhost:8000/swagger/
echo   - Admin: http://localhost:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.

venv\Scripts\python.exe manage.py runserver

pause

