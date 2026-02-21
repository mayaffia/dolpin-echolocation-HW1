@echo off
REM Startup script for Dolphin Echolocation GUI Application (Windows)

echo ==========================================
echo Dolphin Echolocation GUI Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    pause
    exit /b 1
)

REM Install dependencies
echo Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting server...
echo The application will open at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Start the server
cd backend
python server.py

pause