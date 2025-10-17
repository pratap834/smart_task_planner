# 🔑 Setup Requirements Guide

Complete list of what you need to initialize the Smart Task Planner project.

---

## 📋 Quick Summary

### ✅ REQUIRED (Minimum to Run)
1. **Gemini API Key** - For AI-powered task generation
2. **MongoDB** - Database (local or cloud)

### 🔧 OPTIONAL (Enhanced Features)
3. **AWS S3 Credentials** - For plan exports (can skip initially)
4. **NextAuth Secret** - For authentication (auto-generated for dev)

---

## 1️⃣ REQUIRED: Gemini API Key

### What is it?
Google's Gemini AI powers the intelligent task breakdown and critical path analysis.

### How to get it (FREE):
1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Where to add it:
```bash
# backend/.env (create this file)
GEMINI_API_KEY=AIzaSyAcPUeTLYrLNMmntvFaq70BLxlKG05O9v0
```

### Cost:
- **FREE tier:** 15 requests/minute, 1 million tokens/minute
- More than enough for development and small projects

---

## 2️⃣ REQUIRED: MongoDB Database

### What is it?
NoSQL database for storing goals, plans, and tasks.

### Option A: Local MongoDB (Recommended for Dev)

**Using Docker (Easiest):**
```powershell
# Start MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# That's it! MongoDB is running
```

**Configuration:**
```bash
# backend/.env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

**Manual Install (Alternative):**
1. Download: https://www.mongodb.com/try/download/community
2. Install MongoDB Community Edition
3. Start MongoDB service
4. Use same configuration above

### Option B: MongoDB Atlas (Cloud - FREE)

**Why?**
- No local installation needed
- 512MB storage free forever
- Perfect for development and small production

**Setup:**
1. Visit: **https://www.mongodb.com/cloud/atlas/register**
2. Create free account
3. Create a "Free Shared" cluster (M0)
4. Create database user (username + password)
5. Whitelist IP: Add `0.0.0.0/0` (for dev) or your IP
6. Get connection string

**Configuration:**
```bash
# backend/.env
MONGODB_URL=mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=smart_task_planner
```

### Option C: AWS DocumentDB (Production Only)

**When to use:** 
- Large-scale production deployments
- AWS-native architecture

**Cost:** ~$70/month minimum

**Setup:** See `README_PRODUCTION.md`

---

## 3️⃣ OPTIONAL: AWS S3 (For Plan Exports)

### What is it?
Cloud storage for exporting plans as JSON files.

### Do you need it NOW?
**NO** - The app works perfectly without it. S3 is only needed if you want:
- Export plans to cloud storage
- Share plans via presigned URLs
- Backup plans to S3

### How to set up (when ready):

**1. Create AWS Account**
- Visit: https://aws.amazon.com/free
- Free tier: 5GB storage, 20,000 GET requests/month

**2. Create S3 Bucket**
```bash
# Via AWS Console
1. Go to S3 service
2. Click "Create bucket"
3. Name: smart-planner-exports
4. Region: us-east-1
5. Keep defaults
6. Create
```

**3. Create IAM User**
```bash
# Via AWS Console
1. Go to IAM service
2. Create user: smart-planner-app
3. Attach policy: AmazonS3FullAccess
4. Create access key
5. Save Access Key ID and Secret Access Key
```

**4. Add to Configuration**
```bash
# backend/.env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_S3_BUCKET=smart-planner-exports
```

### Skip for now?
Just **leave these variables out** of your `.env` file. The app will work fine without S3.

---

## 4️⃣ OPTIONAL: NextAuth Secret (Frontend)

### What is it?
Secret key for encrypting authentication tokens (NextAuth.js).

### Do you need it NOW?
**Not urgently** - A default will work for local development.

### How to generate:
```powershell
# Generate a random secret
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# Or use OpenSSL
openssl rand -base64 32
```

### Where to add it:
```bash
# frontend-next/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-generated-secret-here
```

---

## 📝 Configuration Files to Create

### Backend Configuration

**File:** `backend/.env`

**Minimum (Required):**
```bash
# Required
GEMINI_API_KEY=your-gemini-api-key-here

# MongoDB (pick one option)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

**Full (With Optional Features):**
```bash
# Required
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner

# AWS S3 (Optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=smart-planner-exports

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Configuration

**File:** `frontend-next/.env.local`

**Minimum:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Full:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
```

---

## 🚀 Quick Setup Steps

### Minimal Setup (Just Run It!)

```powershell
# 1. Start MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# 2. Create backend/.env
@"
GEMINI_API_KEY=your-gemini-key-here
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
"@ | Out-File -FilePath backend\.env -Encoding utf8

# 3. Create frontend-next/.env.local
@"
NEXT_PUBLIC_API_URL=http://localhost:8000
"@ | Out-File -FilePath frontend-next\.env.local -Encoding utf8

# 4. Install dependencies
cd frontend-next
npm install

cd ..\backend
pip install -r requirements.txt

# 5. Run everything
cd ..
.\start.bat
```

### With S3 Features

Follow "Minimal Setup" above, then add to `backend/.env`:
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=smart-planner-exports
```

---

## 🔍 Verification Checklist

### Before Running:
- [ ] `backend/.env` exists with `GEMINI_API_KEY`
- [ ] MongoDB is running (local or Atlas)
- [ ] `MONGODB_URL` is configured
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend dependencies installed (`pip install`)

### After Running:
- [ ] Backend health check: http://localhost:8000/health
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] Frontend loads: http://localhost:3000
- [ ] Can create a goal in the UI
- [ ] Plan generates successfully

---

## 🆘 Troubleshooting

### "GEMINI_API_KEY not set"
```bash
# Check your backend/.env file
# Make sure the key is there and valid
```

### "MongoDB connection failed"
```bash
# Check MongoDB is running
docker ps | grep mongodb

# Or start it
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

### "Connection refused on port 27017"
```bash
# Check if something else is using the port
netstat -an | findstr :27017

# Or use a different port
MONGODB_URL=mongodb://localhost:27018
```

### "AWS credentials not found"
```bash
# S3 is optional! Just skip it for now
# Remove or comment out AWS variables in .env
```

---

## 💰 Cost Summary

### Required (FREE):
- ✅ **Gemini API:** FREE (15 req/min, 1M tokens/min)
- ✅ **MongoDB Local:** FREE (Docker or community edition)
- ✅ **MongoDB Atlas:** FREE (M0 cluster, 512MB)

### Optional (When Needed):
- **AWS S3:** $0.023/GB (~$0.50/month for small usage)
- **AWS DocumentDB:** ~$70/month (production only)
- **AWS ECS/Fargate:** ~$30/month (production deployment)

**Total to start: $0** 🎉

---

## 📚 Where to Get Keys

| Service | URL | Free Tier |
|---------|-----|-----------|
| **Gemini API** | https://makersuite.google.com/app/apikey | ✅ Yes |
| **MongoDB Atlas** | https://www.mongodb.com/cloud/atlas | ✅ Yes (512MB) |
| **AWS Account** | https://aws.amazon.com/free | ✅ Yes (12 months) |
| **MongoDB Community** | https://www.mongodb.com/try/download/community | ✅ Yes (unlimited) |

---

## 🎯 Recommended Setup for Beginners

**Start with this:**
```bash
1. Get Gemini API key (5 minutes)
2. Run MongoDB with Docker (1 command)
3. Create backend/.env with just these two configs
4. Run: .\start.bat
```

**Add later when needed:**
```bash
5. MongoDB Atlas (when sharing with team)
6. AWS S3 (when need export feature)
7. AWS deployment (when going to production)
```

---

## ✅ Summary: What You Actually Need

### To Run Locally (Development):
```
✅ REQUIRED:
1. Gemini API Key (FREE)
2. MongoDB (Docker or local - FREE)

❌ NOT REQUIRED:
3. AWS S3 (optional feature)
4. NextAuth Secret (auto-generated for dev)
```

### Minimum .env File:
```bash
# backend/.env
GEMINI_API_KEY=AIzaSy...your-key
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
```

**That's literally all you need to start! 🚀**

---

**Questions? Check:**
- `README_PRODUCTION.md` - Full production setup
- `BUILD_SUMMARY.md` - Architecture details
- `QUICKSTART.md` - Quick reference
