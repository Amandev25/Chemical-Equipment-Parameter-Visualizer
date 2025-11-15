@echo off
echo ========================================
echo Chemical Equipment Visualizer - Backend Setup
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Creating migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

echo [5/6] Running migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo [6/6] Creating superuser (optional)...
echo.
echo You can skip this step and create superuser later with: python manage.py createsuperuser
set /p create_superuser="Create superuser now? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the development server:
echo   python manage.py runserver
echo.
echo API Documentation will be available at:
echo   http://localhost:8000/swagger/
echo.
echo Admin Panel:
echo   http://localhost:8000/admin/
echo.
pause

