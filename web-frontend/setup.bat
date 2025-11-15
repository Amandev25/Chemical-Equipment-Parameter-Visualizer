@echo off
echo ========================================
echo Chemical Equipment Visualizer - Frontend Setup
echo ========================================
echo.

echo [1/2] Installing dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/2] Setup completed!
echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the development server:
echo   npm run dev
echo.
echo The app will be available at:
echo   http://localhost:3000
echo.
echo Make sure the backend is running at:
echo   http://localhost:8000
echo.
pause

