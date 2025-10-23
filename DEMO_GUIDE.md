# 🎥 Demo Video Recording Guide

## Overview
This guide helps you create a professional demo video showcasing the Smart Task Planner project.

**Target Duration:** 3-5 minutes  
**Format:** MP4 (1920x1080 recommended)  
**Tools:** OBS Studio, Loom, or any screen recorder

---

## 📝 Demo Script

### **1. Introduction (30 seconds)**
**What to show:**
- Open README.md in VS Code
- Briefly show project structure

**What to say:**
```
"Hi! This is Smart Task Planner - an AI-powered system that breaks down user goals 
into actionable tasks with timelines and dependencies. Let me show you how it works."
```

---

### **2. Architecture Overview (30 seconds)**
**What to show:**
- Scroll through ARCHITECTURE.md
- Show the system architecture diagram

**What to say:**
```
"The system uses FastAPI backend, MongoDB database, Google Gemini AI for reasoning, 
and a Next.js frontend. When a user submits a goal, the AI analyzes it and generates 
a complete task breakdown with dependencies and timelines."
```

---

### **3. Backend API Demo (60 seconds)**
**What to show:**
- Open terminal
- Start backend: `cd backend && uvicorn main:app --reload`
- Open browser: `http://localhost:8000/docs`
- Show API endpoints list

**What to say:**
```
"The backend provides RESTful APIs. Here's the Swagger documentation showing all endpoints.
We have endpoints for creating plans, retrieving tasks, and updating task status."
```

**Actions:**
- Scroll through API endpoints
- Click on "POST /api/plans" to expand
- Show the request schema

---

### **4. Live API Request (90 seconds)**
**What to show:**
- Use the Swagger "Try it out" feature OR use Postman
- Create a plan with goal: "Launch a product in 2 weeks"

**Sample Request:**
```json
{
  "goal_text": "Launch a mobile app product in 2 weeks",
  "plan_type": "MODERATE",
  "constraints": {
    "deadline": "2025-11-07T23:59:59",
    "max_hours_per_day": 8,
    "no_work_on_weekends": true
  }
}
```

**What to say:**
```
"Let me submit a real goal: 'Launch a mobile app product in 2 weeks' with constraints 
like a deadline and no work on weekends. The AI will break this down into actionable tasks."
```

**Actions:**
- Click "Execute"
- Wait 3-5 seconds for response
- Show the response with tasks

**Point out in response:**
```
"Look at the response - the AI generated 10 tasks with:
- Clear titles and descriptions
- Duration estimates for each task
- Dependencies between tasks (T2 depends on T1, etc.)
- Priority levels (High, Medium, Low)
- A critical path identifying the longest task chain
- Specific start and end dates respecting our constraints"
```

---

### **5. Frontend Demo (60 seconds)**
**What to show:**
- Open new terminal
- Start frontend: `cd frontend-next && npm run dev`
- Open browser: `http://localhost:3000`
- Show the dashboard

**What to say:**
```
"Now let's use the web interface. This is the dashboard where users can submit goals
and view their generated plans."
```

**Actions:**
1. **Fill the goal form:**
   - Enter goal: "Build a REST API for expense tracking"
   - Set deadline: 15 days from now
   - Enable "No work on weekends"
   - Click "Generate Plan"

2. **Show loading state** (2-3 seconds)

3. **Show results:**
   - Scroll through task cards
   - Point out color coding (red = critical path, blue = normal)
   - Click on a task to show details
   - Show task dependencies
   - Point out the timeline summary

**What to say:**
```
"The plan is generated in seconds. Tasks are color-coded - red borders indicate critical 
path tasks that directly impact the deadline. We can see dependencies, durations, and 
estimated completion dates. Users can update task status as they progress."
```

---

### **6. Key Features Highlight (30 seconds)**
**What to show:**
- Split screen showing both API docs and frontend

**What to say:**
```
"Key features include:
- AI-powered task breakdown using Google Gemini
- Critical path calculation to identify bottleneck tasks
- Constraint-aware scheduling that respects deadlines and working hours
- Task dependency management
- RESTful API with complete documentation
- Modern responsive frontend"
```

---

### **7. Code Architecture (30 seconds)**
**What to show:**
- Back to VS Code
- Show project structure in sidebar
- Open `backend/services/llm_service.py`
- Scroll to the `_get_system_prompt()` method

**What to say:**
```
"The LLM integration uses carefully crafted prompts. Here's the system prompt that 
instructs the AI on how to break down goals, estimate durations, identify dependencies, 
and respect constraints. The prompt engineering is key to getting high-quality results."
```

---

### **8. Database Verification (20 seconds)**
**What to show:**
- Show MongoDB connection in terminal logs OR
- Use MongoDB Compass to show stored data

**What to say:**
```
"All plans and tasks are persisted in MongoDB. This allows users to retrieve their 
plans later and track progress over time."
```

---

### **9. Testing & Code Quality (20 seconds)**
**What to show:**
- Open terminal
- Run tests: `pytest backend/tests/ -v` (if tests exist) OR
- Show `demo_api.py` script

**What to say:**
```
"The project includes automated tests and a demo script for quick validation."
```

---

### **10. Conclusion (20 seconds)**
**What to show:**
- Back to README.md
- Scroll to "Features" section

**What to say:**
```
"This project demonstrates a complete full-stack AI application with proper API design, 
database integration, LLM reasoning, and a production-ready frontend. All code is 
available on GitHub with comprehensive documentation. Thank you for watching!"
```

---

## 🎬 Recording Tips

### **Setup Checklist:**
- [ ] Close unnecessary applications
- [ ] Clear browser history/cache
- [ ] Zoom browser to 125% for readability
- [ ] Use dark theme in VS Code (easier on eyes)
- [ ] Test audio quality
- [ ] Have example goals ready
- [ ] Backend and MongoDB running
- [ ] Frontend dependencies installed

### **During Recording:**
- Speak clearly and at moderate pace
- Avoid "umm" and long pauses (can edit later)
- Show results, don't just talk about them
- Zoom in on important code sections
- Keep mouse movements smooth
- Highlight critical information

### **Technical Settings:**
- Resolution: 1920x1080 (1080p)
- Frame rate: 30fps minimum
- Audio: 48kHz, stereo
- Format: MP4 (H.264 codec)

### **Recommended Tools:**
1. **OBS Studio** (Free, professional)
   - Download: https://obsproject.com/
   - Best for high-quality recordings
   
2. **Loom** (Free tier available)
   - Easy to use
   - Automatic upload and sharing
   
3. **Windows Game Bar** (Built-in)
   - Press Win+G
   - Quick and simple

4. **Mac QuickTime** (Built-in)
   - File → New Screen Recording
   - Simple and effective

---

## 📤 Video Publishing

### **Where to Upload:**
1. **YouTube** (Recommended)
   - Set as "Unlisted" if you want only link-holders to view
   - Add to README.md: `[![Demo Video](thumbnail.jpg)](https://youtube.com/...)`

2. **Google Drive**
   - Upload MP4
   - Set sharing to "Anyone with link"
   - Add link to README.md

3. **Loom**
   - Automatic hosting
   - Easy sharing link
   - Add to README.md

### **Add to README:**
```markdown
## 🎥 Demo Video

Watch the complete demo: [Demo Video Link](https://your-video-url)

[![Demo Thumbnail](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtube.com/watch?v=VIDEO_ID)
```

---

## 🎯 Key Points to Emphasize

### **1. Input/Output Flow**
✅ **Input:** "Launch a product in 2 weeks"  
✅ **Output:** 10 tasks with dependencies, timelines, critical path

### **2. LLM Reasoning**
✅ Show how AI understands context  
✅ Demonstrates intelligent task breakdown  
✅ Respects constraints in reasoning

### **3. API Design**
✅ RESTful endpoints  
✅ Clean request/response models  
✅ Proper error handling  
✅ Interactive documentation

### **4. Database Integration**
✅ MongoDB for persistence  
✅ Proper data models  
✅ Relationships between entities

### **5. Frontend Quality**
✅ Responsive design  
✅ Real-time updates  
✅ Visual task management  
✅ User-friendly interface

---

## 📋 Quick Recording Checklist

Before hitting record:

- [ ] Backend running on port 8000
- [ ] MongoDB running and connected
- [ ] Frontend running on port 3000
- [ ] Browser open to localhost:3000
- [ ] Swagger docs open in another tab
- [ ] VS Code open with project
- [ ] Terminal windows ready
- [ ] Example goals prepared
- [ ] Audio test completed
- [ ] Screen resolution set
- [ ] Recording software configured
- [ ] Notifications disabled
- [ ] Phone on silent

---

## 🎬 Sample Timeline (5-minute video)

| Time | Section | Action |
|------|---------|--------|
| 0:00-0:30 | Intro | Project overview, show README |
| 0:30-1:00 | Architecture | System design, components |
| 1:00-2:00 | Backend API | Swagger docs, API request demo |
| 2:00-3:30 | Frontend | Dashboard, create plan, view results |
| 3:30-4:00 | Code | Show LLM prompt, architecture |
| 4:00-4:30 | Database | Show stored data |
| 4:30-5:00 | Conclusion | Recap features, GitHub link |

---

## 💡 Alternative: Screenshots + Voice-over

If live demo is challenging, create a narrated slideshow:

1. Take screenshots of each step
2. Create slides in PowerPoint/Google Slides
3. Add annotations and highlights
4. Record voice narration
5. Export as video

---

## ✅ Deliverable

**Final Output:**
- Video file: `demo_smart_task_planner.mp4`
- Upload to YouTube/Drive
- Add link to README.md
- Optionally create a thumbnail image

**README Update:**
```markdown
## 🎥 Demo Video

[![Watch Demo](https://img.shields.io/badge/▶️_Watch_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](YOUR_VIDEO_LINK)

See the complete walkthrough of features, API, and frontend in action!
```

---

Good luck with your demo recording! 🎬✨
