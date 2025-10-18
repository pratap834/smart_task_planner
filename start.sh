#!/bin/bash
# Quick start script for Smart Task Planner (Production Stack)

set -e

echo "=================================="
echo "Smart Task Planner - Quick Start"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo "  Install from: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    echo "  Install from: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed${NC}"

# Check for .env files
echo ""
echo "Checking environment files..."

if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}! Creating backend/.env from example${NC}"
    cp backend/.env.example backend/.env
    echo -e "${RED}! IMPORTANT: Edit backend/.env and add your GEMINI_API_KEY${NC}"
fi

if [ ! -f "frontend-next/.env.local" ]; then
    echo -e "${YELLOW}! Creating frontend-next/.env.local from example${NC}"
    cp frontend-next/.env.local.example frontend-next/.env.local
fi

# Check if GEMINI_API_KEY is set
if grep -q "your-gemini-api-key-here" backend/.env 2>/dev/null; then
    echo -e "${RED}! WARNING: GEMINI_API_KEY not configured in backend/.env${NC}"
    echo "  Get your API key at: https://makersuite.google.com/app/apikey"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "=================================="
echo "Starting Services with Docker Compose"
echo "=================================="
echo ""

# Start services
docker-compose up --build -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "Checking service health..."

# Check MongoDB
if docker-compose ps | grep -q "mongodb.*Up"; then
    echo -e "${GREEN}✓ MongoDB is running${NC}"
else
    echo -e "${RED}✗ MongoDB failed to start${NC}"
fi

# Check Backend
if docker-compose ps | grep -q "backend.*Up"; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
fi

# Check Frontend
if docker-compose ps | grep -q "frontend.*Up"; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend failed to start${NC}"
fi

echo ""
echo "=================================="
echo "✓ Smart Task Planner is running!"
echo "=================================="
echo ""
echo "Services:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo "  MongoDB:   localhost:27017"
echo ""
echo "View logs:    docker-compose logs -f"
echo "Stop all:     docker-compose down"
echo "Restart all:  docker-compose restart"
echo ""
echo "=================================="
