# 🚀 Quick Start Commands - Smart Task Planner

## Prerequisites Check

```powershell
# Check Python version (need 3.9+)
python --version

# Check if MongoDB is running
docker ps | Select-String mongodb

# Check if Node.js is installed (for frontend)
node --version
npm --version
```

---

## 🐳 Step 1: Start MongoDB

### Option A: Using Docker (Recommended)

```powershell
# Start MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Verify it's running
docker ps
```

### Option B: If Docker is Already Running

```powershell
# Just check if MongoDB is running
docker ps | Select-String mongodb

# If stopped, start it
docker start mongodb
```

---

## ⚙️ Step 2: Setup Backend

### First Time Setup

```powershell
# Navigate to project root
cd D:\Matrix\smart_task_planner

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
Copy-Item backend\.env.example backend\.env

# Edit .env file with your Gemini API key
notepad backend\.env
```

**Edit backend/.env:**
```env
GEMINI_API_KEY=your-gemini-api-key-here
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

### Every Time You Run

```powershell
# Navigate to backend directory
cd D:\Matrix\smart_task_planner\backend

# Activate virtual environment (if not already)
..\venv\Scripts\Activate.ps1

# Start the backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend will be running at:** http://localhost:8000  
**API Documentation:** http://localhost:8000/docs

---

## 🎨 Step 3: Setup Frontend (Next.js)

### First Time Setup

```powershell
# Open NEW terminal/PowerShell window
cd D:\Matrix\smart_task_planner\frontend-next

# Install dependencies (first time only)
npm install

# Create .env.local file
Copy-Item .env.local.example .env.local

# Edit .env.local if needed
notepad .env.local
```

**Edit frontend-next/.env.local:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-here
```

### Every Time You Run

```powershell
# Navigate to frontend directory
cd D:\Matrix\smart_task_planner\frontend-next

# Start the frontend development server
npm run dev
```

**Frontend will be running at:** http://localhost:3000

---

## 🎯 Complete Startup Sequence

### Terminal 1: MongoDB

```powershell
# Start MongoDB (if not running)
docker start mongodb

# OR first time:
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

### Terminal 2: Backend

```powershell
cd D:\Matrix\smart_task_planner\backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 3: Frontend

```powershell
cd D:\Matrix\smart_task_planner\frontend-next
npm run dev
```

---

## 🧪 Testing Commands

### Test API Endpoints

```powershell
# Health check
curl http://localhost:8000/health

# OR in PowerShell
Invoke-RestMethod -Uri http://localhost:8000/health
```

### Run Automated Tests

```powershell
cd D:\Matrix\smart_task_planner
.\venv\Scripts\Activate.ps1
pytest test_api.py -v
```

### Run Demo Script

```powershell
cd D:\Matrix\smart_task_planner
.\venv\Scripts\Activate.ps1
python demo_api.py
```

---

## 📝 Quick Test via API

### PowerShell Example

```powershell
# Create a plan
$body = @{
    goal_text = "Launch a mobile app in 2 weeks"
    plan_type = "MODERATE"
    constraints = @{
        max_hours_per_day = 8
        no_work_on_weekends = $true
    }
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:8000/api/plans `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Display the plan
$response | ConvertTo-Json -Depth 10
```

### cURL Example (if you have it)

```bash
curl -X POST "http://localhost:8000/api/plans" \
  -H "Content-Type: application/json" \
  -d '{
    "goal_text": "Build a REST API for task management",
    "plan_type": "MODERATE",
    "constraints": {
      "max_hours_per_day": 8,
      "no_work_on_weekends": true
    }
  }'
```

---

## 🛠️ Troubleshooting Commands

### Check if ports are in use

```powershell
# Check port 8000 (backend)
netstat -ano | findstr :8000

# Check port 3000 (frontend)
netstat -ano | findstr :3000

# Check port 27017 (MongoDB)
netstat -ano | findstr :27017
```

### Stop processes if needed

```powershell
# Stop MongoDB
docker stop mongodb

# Kill process on port (replace PID)
Stop-Process -Id <PID> -Force
```

### Clear database (if needed)

```powershell
# Stop MongoDB
docker stop mongodb

# Remove MongoDB container
docker rm mongodb

# Restart fresh
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

### Reinstall dependencies

```powershell
# Backend
cd D:\Matrix\smart_task_planner
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend-next
Remove-Item -Recurse -Force node_modules
npm install
```

---

## 🎬 Access Points

Once everything is running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Web interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs (Swagger)** | http://localhost:8000/docs | Interactive API documentation |
| **API Docs (ReDoc)** | http://localhost:8000/redoc | Alternative API documentation |
| **Health Check** | http://localhost:8000/health | Server status |
| **MongoDB** | mongodb://localhost:27017 | Database |

---

## 🚦 Quick Status Check

```powershell
# Check all services
Write-Host "=== Service Status ===" -ForegroundColor Cyan

# MongoDB
Write-Host "`nMongoDB:" -ForegroundColor Yellow
docker ps | Select-String mongodb

# Backend (check if port 8000 is in use)
Write-Host "`nBackend (Port 8000):" -ForegroundColor Yellow
netstat -ano | findstr :8000

# Frontend (check if port 3000 is in use)
Write-Host "`nFrontend (Port 3000):" -ForegroundColor Yellow
netstat -ano | findstr :3000

# Test backend health
Write-Host "`nBackend Health:" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri http://localhost:8000/health
    Write-Host "✅ Backend is healthy" -ForegroundColor Green
    $health | ConvertTo-Json
} catch {
    Write-Host "❌ Backend is not responding" -ForegroundColor Red
}
```

---

## 📦 Alternative: Use Quick Start Scripts

### Windows

```powershell
# Start backend
.\start.bat

# OR manual
cd backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### Frontend

```powershell
cd frontend-next
npm run dev
```

---

## 🎯 Typical Workflow

### First Time Ever

```powershell
# 1. Clone/Download project
cd D:\Matrix\smart_task_planner

# 2. Setup backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Setup MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# 4. Configure environment
Copy-Item backend\.env.example backend\.env
notepad backend\.env  # Add your Gemini API key

# 5. Setup frontend
cd frontend-next
npm install

# 6. Start everything (3 terminals)
# Terminal 1: MongoDB already running
# Terminal 2: cd backend && uvicorn main:app --reload
# Terminal 3: cd frontend-next && npm run dev
```

### Every Day After

```powershell
# Terminal 1: Start MongoDB (if stopped)
docker start mongodb

# Terminal 2: Start Backend
cd D:\Matrix\smart_task_planner\backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 3: Start Frontend
cd D:\Matrix\smart_task_planner\frontend-next
npm run dev
```

---

## 🎓 Development Commands

### Backend Development

```powershell
# Watch for changes (auto-reload is on by default with --reload flag)
cd backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --reload

# Run specific module
python -m backend.main

# Check syntax
python -m py_compile main.py
```

### Frontend Development

```powershell
cd frontend-next

# Development server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint

# Type check
npm run type-check
```

---

## 📊 Monitor Logs

### Backend Logs

```powershell
# Logs appear in the terminal where uvicorn is running
# Watch for:
# - "Application startup complete"
# - "Connected to MongoDB"
# - Request logs (GET, POST, etc.)
```

### Frontend Logs

```powershell
# Logs appear in the terminal where npm run dev is running
# Watch for:
# - "Ready on http://localhost:3000"
# - Compilation status
# - Hot reload notifications
```

### MongoDB Logs

```powershell
# View MongoDB logs
docker logs mongodb

# Follow logs in real-time
docker logs -f mongodb
```

---

## 🔒 Environment Variables Reference

### Backend (.env in backend/)

```env
# Required
GEMINI_API_KEY=your-gemini-api-key-here
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner

# Optional
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-1.5-flash
```

### Frontend (.env.local in frontend-next/)

```env
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
```

---

## ✅ Final Checklist Before Running

- [ ] Python 3.9+ installed
- [ ] Node.js & npm installed
- [ ] Docker installed and running
- [ ] MongoDB container started
- [ ] Backend .env file configured with Gemini API key
- [ ] Virtual environment activated
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Ports 8000, 3000, 27017 available

---

## 🎉 Success Indicators

**You know it's working when:**

✅ Backend terminal shows:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
Connected to MongoDB at mongodb://localhost:27017
```

✅ Frontend terminal shows:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

✅ Browser shows working interface at http://localhost:3000

✅ API docs are accessible at http://localhost:8000/docs

---

**Need Help?** Check [README.md](README.md) or [DELIVERABLES.md](DELIVERABLES.md)
