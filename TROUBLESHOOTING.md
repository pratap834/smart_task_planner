# 🔧 Troubleshooting Guide

## Quick Fixes for Common Issues

---

## ❌ Error: `ModuleNotFoundError: No module named 'beanie'`

**Problem:** Missing MongoDB dependencies in virtual environment

**Solution:**
```powershell
cd D:\Matrix\smart_task_planner
.\venv\Scripts\Activate.ps1
pip install beanie motor pymongo
```

Or reinstall all dependencies:
```powershell
pip install -r requirements.txt
```

---

## ❌ Error: `docker: Error response from daemon: Conflict. The container name "/mongodb" is already in use`

**Problem:** MongoDB container already exists

**Solution:**
```powershell
# Just start the existing container
docker start mongodb

# Verify it's running
docker ps
```

If you need to remove and recreate:
```powershell
docker stop mongodb
docker rm mongodb
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

---

## ❌ Frontend Error: `Failed to proxy http://localhost:8000/api/...`

**Problem:** Backend is not running or not accessible

**Solution:**

1. **Make sure backend is running:**
```powershell
# In a separate terminal
cd D:\Matrix\smart_task_planner\backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Verify backend is accessible:**
```powershell
# Test in browser or PowerShell
Invoke-RestMethod -Uri http://localhost:8000/health
```

3. **Check if port 8000 is blocked:**
```powershell
netstat -ano | findstr :8000
```

---

## ❌ Text Not Visible in Forms (Dropdowns, Inputs)

**Problem:** Dark mode CSS issues or missing text colors

**Solution:** Already fixed! The changes include:

1. **Updated `frontend-next/app/globals.css`**
   - Disabled dark mode
   - Forced light mode colors
   - Added explicit text colors for inputs

2. **Updated `frontend-next/components/GoalForm.tsx`**
   - Added `text-gray-900 bg-white` to all inputs
   - Added explicit colors to dropdown options

**If still having issues, refresh your browser:**
```
Ctrl + Shift + R (hard refresh)
```

Or clear Next.js cache:
```powershell
cd frontend-next
Remove-Item -Recurse -Force .next
npm run dev
```

---

## ❌ Error: `uvicorn: command not found`

**Problem:** Virtual environment not activated or uvicorn not installed

**Solution:**
```powershell
# Activate virtual environment
cd D:\Matrix\smart_task_planner
.\venv\Scripts\Activate.ps1

# Install uvicorn
pip install uvicorn[standard]
```

---

## ❌ Error: `npm: command not found`

**Problem:** Node.js not installed

**Solution:**
1. Download Node.js from: https://nodejs.org/
2. Install LTS version
3. Restart terminal
4. Verify: `node --version` and `npm --version`

---

## ❌ Frontend Won't Start - `npm run dev` fails

**Problem:** Dependencies not installed

**Solution:**
```powershell
cd D:\Matrix\smart_task_planner\frontend-next

# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install

# Try again
npm run dev
```

---

## ❌ Error: `Port 8000 is already in use`

**Problem:** Another process is using port 8000

**Solution:**

**Find the process:**
```powershell
netstat -ano | findstr :8000
```

**Kill the process (replace PID):**
```powershell
Stop-Process -Id <PID> -Force
```

**Or use a different port:**
```powershell
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Then update `frontend-next/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## ❌ Error: `Port 3000 is already in use`

**Problem:** Another process is using port 3000

**Solution:**

**Find and kill:**
```powershell
netstat -ano | findstr :3000
Stop-Process -Id <PID> -Force
```

**Or use different port:**
```powershell
npm run dev -- -p 3001
```

---

## ❌ MongoDB Connection Error

**Problem:** MongoDB not running or wrong connection string

**Solution:**

1. **Check MongoDB is running:**
```powershell
docker ps | Select-String mongodb
```

2. **Start MongoDB:**
```powershell
docker start mongodb
```

3. **Check connection string in `backend/.env`:**
```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

4. **Test MongoDB connection:**
```powershell
docker exec -it mongodb mongosh
```

---

## ❌ Error: `GEMINI_API_KEY not found`

**Problem:** Missing or incorrect API key configuration

**Solution:**

1. **Create `.env` file in backend folder:**
```powershell
cd D:\Matrix\smart_task_planner\backend
Copy-Item .env.example .env
```

2. **Edit `.env` and add your key:**
```env
GEMINI_API_KEY=your-actual-api-key-here
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

3. **Get API key from:**
https://makersuite.google.com/app/apikey

---

## ❌ Virtual Environment Issues

**Problem:** Virtual environment corrupted or not activating

**Solution:**

**Recreate virtual environment:**
```powershell
cd D:\Matrix\smart_task_planner

# Remove old venv
Remove-Item -Recurse -Force venv

# Create new venv
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

## ❌ Python Version Error

**Problem:** Python version too old

**Solution:**

**Check version:**
```powershell
python --version
```

**Required:** Python 3.9 or higher

**If too old:**
1. Download Python 3.11+ from: https://www.python.org/downloads/
2. Install with "Add to PATH" checked
3. Restart terminal
4. Recreate virtual environment

---

## 🔍 Diagnostic Commands

**Check all services:**
```powershell
# MongoDB
docker ps | Select-String mongodb

# Backend (port 8000)
netstat -ano | findstr :8000

# Frontend (port 3000)
netstat -ano | findstr :3000

# Backend health
Invoke-RestMethod -Uri http://localhost:8000/health
```

---

## 🧹 Clean Start (Nuclear Option)

If nothing works, start fresh:

```powershell
# Stop everything
docker stop mongodb
# Kill any running processes on ports 8000, 3000

# Backend clean
cd D:\Matrix\smart_task_planner
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend clean
cd frontend-next
Remove-Item -Recurse -Force node_modules
Remove-Item -Recurse -Force .next
Remove-Item package-lock.json
npm install

# MongoDB fresh
docker stop mongodb
docker rm mongodb
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Configure .env
notepad backend\.env  # Add GEMINI_API_KEY

# Start backend
cd backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend (new terminal)
cd frontend-next
npm run dev
```

---

## 📞 Still Having Issues?

1. Check [RUN_COMMANDS.md](RUN_COMMANDS.md) for detailed setup
2. Check [README.md](README.md) for configuration
3. Verify all prerequisites are installed:
   - Python 3.9+
   - Node.js 16+
   - Docker Desktop
   - Gemini API key

---

**Last Updated:** October 23, 2025
