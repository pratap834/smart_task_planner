@echo off
REM Smart Task Planner - Quick Start Script for Windows

echo ====================================
echo Smart Task Planner - Quick Start
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [!] Virtual environment not found. Creating...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [+] Virtual environment created
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [!] Dependencies not installed. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [+] Dependencies installed
)

REM Check if .env exists
if not exist ".env" (
    echo [!] .env file not found
    if exist ".env.example" (
        echo [*] Copying .env.example to .env
        copy .env.example .env
        echo.
        echo [!] IMPORTANT: Please edit .env and add your GEMINI_API_KEY
        echo [!] Get your free key: https://makersuite.google.com/app/apikey
        echo [!] Then run this script again
        pause
        exit /b 1
    ) else (
        echo [X] .env.example not found
        pause
        exit /b 1
    )
)

REM Check if Gemini API key is configured
findstr /C:"GEMINI_API_KEY=your-gemini-api-key-here" .env >nul
if %errorlevel%==0 (
    echo [!] Gemini API key not configured in .env
    echo [!] Please edit .env and add your GEMINI_API_KEY
    echo.
    echo Get your free API key at:
    echo   https://makersuite.google.com/app/apikey
    pause
    exit /b 1
)

REM Initialize database
echo [*] Initializing database...
python -c "from backend.database import init_db; init_db(); print('[+] Database initialized')"
if errorlevel 1 (
    echo [X] Failed to initialize database
    pause
    exit /b 1
)

echo.
echo ====================================
echo Starting Smart Task Planner Server
echo ====================================
echo.
echo [+] Backend API: http://localhost:8000
echo [+] API Docs: http://localhost:8000/docs
echo [+] Frontend: Open frontend/index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python backend\main.py
