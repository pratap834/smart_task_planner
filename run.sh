#!/bin/bash
# Smart Task Planner - Quick Start Script for Linux/Mac

set -e

echo "===================================="
echo "Smart Task Planner - Quick Start"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[!] Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "[+] Virtual environment created"
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "[!] Dependencies not installed. Installing..."
    pip install -r requirements.txt
    echo "[+] Dependencies installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "[!] .env file not found"
    if [ -f ".env.example" ]; then
        echo "[*] Copying .env.example to .env"
        cp .env.example .env
        echo ""
        echo "[!] IMPORTANT: Please edit .env and add your GEMINI_API_KEY"
        echo "[!] Get your free key: https://makersuite.google.com/app/apikey"
        echo "[!] Then run this script again"
        exit 1
    else
        echo "[X] .env.example not found"
        exit 1
    fi
fi

# Check if Gemini API key is configured
if grep -q "GEMINI_API_KEY=your-gemini-api-key-here" .env; then
    echo "[!] Gemini API key not configured in .env"
    echo "[!] Please edit .env and add your GEMINI_API_KEY"
    echo ""
    echo "Get your free API key at:"
    echo "  https://makersuite.google.com/app/apikey"
    exit 1
fi

# Initialize database
echo "[*] Initializing database..."
python -c "from backend.database import init_db; init_db(); print('[+] Database initialized')"

echo ""
echo "===================================="
echo "Starting Smart Task Planner Server"
echo "===================================="
echo ""
echo "[+] Backend API: http://localhost:8000"
echo "[+] API Docs: http://localhost:8000/docs"
echo "[+] Frontend: Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python backend/main.py
