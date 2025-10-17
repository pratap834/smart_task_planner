@echo off
REM Quick start script for Smart Task Planner (Production Stack) - Windows

echo ==================================
echo Smart Task Planner - Quick Start
echo ==================================
echo.

REM Check Docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Docker is not installed
    echo     Install from: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)
echo [+] Docker installed

REM Check Docker Compose
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Docker Compose is not installed
    echo     Install from: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)
echo [+] Docker Compose installed

echo.
echo Checking environment files...

REM Check backend .env
if not exist "backend\.env" (
    echo [!] Creating backend\.env from example
    copy backend\.env.example backend\.env
    echo [!] IMPORTANT: Edit backend\.env and add your GEMINI_API_KEY
)

REM Check frontend .env.local
if not exist "frontend-next\.env.local" (
    echo [!] Creating frontend-next\.env.local from example
    copy frontend-next\.env.local.example frontend-next\.env.local
)

REM Check if GEMINI_API_KEY is configured
findstr /C:"your-gemini-api-key-here" backend\.env >nul 2>&1
if %errorlevel%==0 (
    echo [!] WARNING: GEMINI_API_KEY not configured in backend\.env
    echo     Get your API key at: https://makersuite.google.com/app/apikey
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

echo.
echo ==================================
echo Starting Services with Docker Compose
echo ==================================
echo.

REM Start services
docker-compose up --build -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ==================================
echo Smart Task Planner is running!
echo ==================================
echo.
echo Services:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo   MongoDB:   localhost:27017
echo.
echo View logs:    docker-compose logs -f
echo Stop all:     docker-compose down
echo Restart all:  docker-compose restart
echo.
echo ==================================
echo.
echo Press any key to view logs (Ctrl+C to exit)...
pause >nul
docker-compose logs -f
