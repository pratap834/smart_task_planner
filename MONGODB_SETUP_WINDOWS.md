# 🗄️ MongoDB Setup for Windows

Docker Desktop is not running. Here are your options to get MongoDB running:

---

## ⚡ OPTION 1: MongoDB Atlas (Cloud - RECOMMENDED ✅)

**Why this is best:**
- ✅ No installation needed
- ✅ No Docker required
- ✅ FREE forever (512MB)
- ✅ Works immediately
- ✅ 2 minutes setup

### Setup Steps:

**1. Create Account**
```
Visit: https://www.mongodb.com/cloud/atlas/register
Sign up (free)
```

**2. Create Free Cluster**
```
1. Click "Build a Database"
2. Select "FREE" tier (M0)
3. Choose cloud provider: AWS
4. Choose region: Closest to you (e.g., us-east-1)
5. Cluster name: smart-planner (or keep default)
6. Click "Create Cluster" (takes 1-3 minutes)
```

**3. Create Database User**
```
1. Go to "Database Access" (left sidebar)
2. Click "Add New Database User"
3. Authentication Method: Password
4. Username: smartplanner
5. Password: Click "Autogenerate Secure Password" (copy it!)
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"
```

**4. Allow Network Access**
```
1. Go to "Network Access" (left sidebar)
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
   - This adds: 0.0.0.0/0
4. Click "Confirm"
```

**5. Get Connection String**
```
1. Go to "Database" (left sidebar)
2. Click "Connect" button on your cluster
3. Choose "Connect your application"
4. Driver: Python, Version: 3.12 or later
5. Copy the connection string - looks like:
   mongodb+srv://smartplanner:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   
6. Replace <password> with the password you copied earlier
```

**6. Update backend/.env**
```bash
GEMINI_API_KEY=AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0
MONGODB_URL=mongodb+srv://smartplanner:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=smart_task_planner
```

**✅ Done! Skip to "Test Connection" section below**

---

## 🐳 OPTION 2: Start Docker Desktop

If you want to use Docker, you need to start Docker Desktop first.

**1. Start Docker Desktop**
```
1. Press Windows key
2. Search "Docker Desktop"
3. Click to open
4. Wait for Docker to start (whale icon in system tray)
5. Icon should be steady (not animated)
```

**2. Run MongoDB Container**
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

**3. Update backend/.env**
```bash
GEMINI_API_KEY=AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

---

## 💻 OPTION 3: Install MongoDB Locally (Without Docker)

**1. Download MongoDB**
```
Visit: https://www.mongodb.com/try/download/community
Select:
- Version: 7.0.x (latest)
- Platform: Windows
- Package: MSI
Click "Download"
```

**2. Install MongoDB**
```
1. Run the downloaded .msi file
2. Choose "Complete" installation
3. Check "Install MongoDB as a Service"
4. Check "Run service as Network Service user"
5. Uncheck "Install MongoDB Compass" (optional GUI, takes time)
6. Click "Install"
7. Click "Finish"
```

**3. Verify Installation**
```powershell
# Check if MongoDB service is running
Get-Service MongoDB

# Should show: Running
```

**4. Update backend/.env**
```bash
GEMINI_API_KEY=AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

---

## 🔍 Test Connection

After choosing any option above, test if MongoDB works:

```powershell
cd backend
pip install pymongo

# Test connection
python -c "from pymongo import MongoClient; client = MongoClient('YOUR_MONGODB_URL'); print('✅ Connected!'); print(client.server_info()['version'])"
```

Replace `YOUR_MONGODB_URL` with your actual MongoDB URL.

**Expected output:**
```
✅ Connected!
7.0.x
```

---

## 📝 Creating Configuration Files

Let me create the configuration files for you:

### For MongoDB Atlas (Option 1 - RECOMMENDED):

**backend/.env:**
```bash
# Required
GEMINI_API_KEY=AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0
GEMINI_MODEL=gemini-1.5-flash

# MongoDB Atlas (replace with your actual connection string)
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=smart_task_planner

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### For Local MongoDB (Options 2 or 3):

**backend/.env:**
```bash
# Required
GEMINI_API_KEY=AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0
GEMINI_MODEL=gemini-1.5-flash

# MongoDB Local
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Configuration:

**frontend-next/.env.local:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=dev-secret-change-in-production
```

---

## 🎯 My Recommendation

**Use MongoDB Atlas (Option 1)** because:
- ✅ No Docker needed
- ✅ No local installation
- ✅ Works from anywhere
- ✅ FREE forever
- ✅ 2 minutes setup
- ✅ Production-ready

---

## 🚀 Next Steps After MongoDB is Ready

```powershell
# 1. Install dependencies
cd frontend-next
npm install

cd ..\backend
pip install -r requirements.txt

# 2. Run backend
cd backend
python -m uvicorn main:app --reload

# 3. Run frontend (new terminal)
cd frontend-next
npm run dev
```

Visit: http://localhost:3000

---

## ❌ Troubleshooting

### "docker: error during connect"
- Docker Desktop is not running
- Start Docker Desktop or use MongoDB Atlas instead

### "Connection refused"
- MongoDB service not started
- Check: `Get-Service MongoDB` (for local install)
- Or restart Docker container

### "Authentication failed"
- Check username/password in connection string
- Password might need URL encoding (% instead of special chars)

### "Network timeout"
- Check Network Access in MongoDB Atlas
- Add IP: 0.0.0.0/0 (development) or your specific IP

---

## 💡 Pro Tip

**For development:** Use MongoDB Atlas
**For production:** Use AWS DocumentDB (see `README_PRODUCTION.md`)

MongoDB Atlas is perfect for getting started and even handles small production apps!

---

**Ready to proceed? Choose an option above and I'll help you set it up!** 🚀
