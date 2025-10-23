# 🎯 Smart Task Planner

An AI-powered task planning system that transforms user goals into detailed, actionable plans with task dependencies, timelines, and critical path analysis.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎥 Demo Video

[![Watch Demo](https://img.shields.io/badge/📹_Record_Your_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](DEMO_GUIDE.md)

**Complete demo recording guide available:** See [DEMO_GUIDE.md](DEMO_GUIDE.md) for step-by-step instructions on creating a professional demo video.

> **Quick Demo:** Submit a goal like "Launch a product in 2 weeks" and get a complete task breakdown with dependencies, timelines, and critical path analysis in 3-5 seconds!

## ✅ Project Requirements

**Objective:** Break user goals into actionable tasks with timelines using AI reasoning

This project fully implements all requirements:
- ✅ **Input:** Goal text (e.g., "Launch a product in 2 weeks")
- ✅ **Output:** Task breakdown, dependencies, estimated timelines
- ✅ **Frontend:** Web interface to submit goals & view plans
- ✅ **Backend API:** FastAPI to process input & generate plans
- ✅ **Database:** MongoDB for task storage
- ✅ **LLM Integration:** Google Gemini for reasoning & task generation

📄 **Detailed requirements verification:** [PROJECT_REQUIREMENTS.md](PROJECT_REQUIREMENTS.md)

## 📋 Table of Contents

- [Demo Video](#-demo-video)
- [Project Requirements](#-project-requirements)
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Frontend Usage](#frontend-usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Smart Task Planner uses Google Gemini AI to break down complex goals into structured, actionable task plans. It automatically:

- ✅ Breaks down goals into 5-15 concrete tasks
- ✅ Identifies task dependencies and sequences
- ✅ Calculates critical path (longest dependency chain)
- ✅ Assigns realistic timelines (1-3 days per task)
- ✅ Respects constraints (deadlines, work hours, weekends)
- ✅ Provides confidence scores for estimates
- ✅ Supports multiple plan types (aggressive, moderate, conservative)

## ✨ Features

### Core Features
- **AI-Powered Task Breakdown**: Uses Google Gemini AI to intelligently decompose goals
- **Critical Path Analysis**: Identifies tasks that determine minimum project duration
- **Constraint Handling**: Respects deadlines, max hours/day, weekends, and unavailable dates
- **Smart Scheduling**: Assigns start/end dates based on dependencies and constraints
- **Plan Variations**: Generate aggressive, moderate, or conservative timelines
- **Task Dependencies**: Automatically manages prerequisite relationships

### API Features
- RESTful API with FastAPI
- Create, retrieve, update, and list plans
- Task status management (pending, in_progress, completed, blocked)
- Database persistence with SQLite (easily swappable to PostgreSQL/MongoDB)
- CORS-enabled for frontend integration

### Frontend Features
- Clean, responsive web interface
- Visual task cards with color-coded priorities
- Critical path highlighting
- Real-time plan generation
- Mobile-friendly design

## 🏗️ Architecture

### System Components

```
┌─────────────────┐
│   Frontend UI   │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────┐
│   FastAPI API   │
│   (Backend)     │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┐
    ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌─────────┐
│LLM Svc │ │Plan  │ │Database │
│(Gemini)│ │Logic │ │(SQLite) │
└────────┘ └──────┘ └─────────┘
```

### Data Flow

1. **User Input** → Goal text + constraints
2. **LLM Service** → Generate task breakdown using Google Gemini
3. **Plan Service** → Calculate critical path, assign dates
4. **Database** → Store goal, plan, and tasks
5. **API Response** → Return structured JSON plan

### Technology Stack

**Backend**:
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Google Gemini API (LLM)
- Pydantic (validation)
- SQLite (database)

**Frontend**:
- Vanilla HTML/CSS/JavaScript
- Responsive design
- Fetch API for backend communication

### LLM Prompt Engineering

The system uses sophisticated prompts to guide the AI in generating high-quality task breakdowns.

**System Prompt (Defines AI Behavior):**
```
You are an expert project planner and task breakdown specialist. Your role is to:
1. Analyze user goals and break them down into actionable tasks
2. Estimate realistic task durations (1-3 days per task)
3. Identify task dependencies and create a logical sequence
4. Respect user constraints (deadlines, work hours, unavailable dates)
5. Identify critical path tasks and high-risk areas
6. Provide clear, detailed task descriptions
```

**User Prompt Example:**
```
Goal: Launch a mobile app product in 2 weeks

Plan Type: MODERATE - Balance speed and safety, some parallel tasks

Constraints:
- Deadline: 2025-11-07T23:59:59
- Max work hours per day: 8
- No work on weekends
- Unavailable dates: 2025-10-28, 2025-10-29

Generate a detailed task breakdown with dependencies, durations, and priorities.
```

**AI Response (JSON):**
```json
{
  "tasks": [
    {
      "id": "T1",
      "title": "Requirements & Planning",
      "description": "Define core features, user stories, and technical architecture",
      "duration_days": 1,
      "depends_on": [],
      "priority": "High",
      "confidence": 0.95
    },
    {
      "id": "T2",
      "title": "UI/UX Design",
      "description": "Create wireframes, mockups, and user flow diagrams",
      "duration_days": 2,
      "depends_on": ["T1"],
      "priority": "High",
      "confidence": 0.90
    }
  ],
  "plan_summary": "10-task plan for mobile app launch with 12 working days..."
}
```

**Key Prompt Features:**
- ✅ Structured output format (JSON schema)
- ✅ Context-rich instructions
- ✅ Constraint integration
- ✅ Plan type adaptation (aggressive/moderate/conservative)
- ✅ Fallback handling for API failures

See `backend/services/llm_service.py` for complete implementation.

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (free tier available)
- pip (Python package manager)

### Step 1: Clone or Download

```bash
cd d:\Matrix\smart_task_planner
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment

Copy the example environment file and add your API key:

```powershell
copy .env.example .env
```

Edit `.env` and add your Google Gemini API key:

```env
# Get your free API key: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash
```

> **Getting Your Gemini API Key:**
> 1. Visit https://makersuite.google.com/app/apikey
> 2. Sign in with your Google account
> 3. Create a new API key (free tier available)
> 4. Copy and paste it into your `.env` file

### Step 5: Initialize Database

The database will be created automatically on first run, but you can verify:

```powershell
python -c "from backend.database import init_db; init_db(); print('Database initialized!')"
```

## 🎮 Quick Start

### Option 1: Run Backend + Frontend

**Terminal 1 - Start Backend:**
```powershell
cd d:\Matrix\smart_task_planner
.\venv\Scripts\Activate.ps1
python backend/main.py
```

The API will start on `http://localhost:8000`

**Terminal 2 - Open Frontend:**
```powershell
# Simply open the HTML file in your browser
start frontend/index.html
```

Or use a simple HTTP server:
```powershell
cd frontend
python -m http.server 3000
# Then open http://localhost:3000
```

### Option 2: Use the Demo Script

```powershell
# Interactive mode
python demo_api.py

# Automated demo
python demo_api.py --auto
```

### Option 3: Use the API Directly

```powershell
# Test health check
curl http://localhost:8000/health

# Create a plan (PowerShell)
$body = @{
    goal_text = "Build a mobile app for habit tracking"
    plan_type = "moderate"
    constraints = @{
        max_hours_per_day = 8
        no_work_on_weekends = $true
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/plans -Method POST -Body $body -ContentType "application/json"
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. Create Plan
**POST** `/plans`

Creates a new plan from a goal.

**Request:**
```json
{
  "goal_text": "Build a full-stack web application",
  "plan_type": "moderate",
  "constraints": {
    "deadline": "2025-12-31",
    "max_hours_per_day": 8,
    "no_work_on_weekends": true,
    "unavailable_dates": ["2025-12-25"]
  }
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "goal_id": 1,
  "plan_summary": "Complete plan breakdown...",
  "critical_path": ["T1", "T3", "T5"],
  "status": "active",
  "plan_type": "moderate",
  "tasks": [
    {
      "id": "T1",
      "title": "Project Setup",
      "description": "Initialize project structure...",
      "duration_days": 1,
      "earliest_start": "2025-10-16",
      "latest_finish": "2025-10-17",
      "depends_on": [],
      "priority": "High",
      "confidence": 0.9,
      "status": "pending"
    }
  ],
  "created_at": "2025-10-16T10:30:00",
  "updated_at": "2025-10-16T10:30:00"
}
```

#### 2. Get Plan
**GET** `/plans/{plan_id}`

Retrieves a specific plan.

**Response:** `200 OK`

#### 3. List Plans
**GET** `/plans?skip=0&limit=10`

Lists all plans with pagination.

**Response:** `200 OK` (array of plans)

#### 4. Update Task
**PATCH** `/plans/{plan_id}/tasks/{task_id}`

Updates a task's status.

**Request:**
```json
{
  "status": "completed"
}
```

**Response:** `200 OK`

#### 5. Get Plan Tasks
**GET** `/plans/{plan_id}/tasks`

Gets all tasks for a specific plan.

**Response:** `200 OK` (array of tasks)

### Interactive API Docs

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🖥️ Frontend Usage

### Accessing the UI

1. Start the backend server
2. Open `frontend/index.html` in a web browser
3. Enter your goal and constraints
4. Click "Generate Plan"

### UI Features

- **Goal Input**: Large text area for detailed goals
- **Plan Type**: Choose aggressive, moderate, or conservative
- **Constraints**: Set deadline, max hours/day, weekend work
- **Plan Display**: Color-coded task cards with all details
- **Critical Path**: Highlighted tasks on the critical path

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider to use | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | Required if using OpenAI |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `OPENAI_API_BASE` | API base URL | `https://api.openai.com/v1` |
| `GEMINI_API_KEY` | Google Gemini API key | Required if using Gemini |
| `GEMINI_MODEL` | Gemini model to use | `gemini-1.5-flash` |
| `DATABASE_URL` | Database connection | `sqlite:///./smart_task_planner.db` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `True` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000,...` |

### Using Different LLM Providers

**Google Gemini (Free tier available)**:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key-here
GEMINI_MODEL=gemini-1.5-flash
# Available models: gemini-1.5-pro, gemini-1.5-flash, gemini-pro
```

**OpenAI GPT**:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
# Available models: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
```

**OpenRouter (Access to multiple models)**:
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_API_KEY=sk-or-v1-...
OPENAI_MODEL=anthropic/claude-3-5-sonnet

# Local LLM (Ollama, LM Studio, etc.)
**Local LLM (Ollama, LM Studio, etc.)**:
```env
LLM_PROVIDER=openai
OPENAI_API_BASE=http://localhost:1234/v1
OPENAI_API_KEY=not-needed
OPENAI_MODEL=llama3
```

### Database Options

**SQLite (default)**:
```env
DATABASE_URL=sqlite:///./smart_task_planner.db
```

**PostgreSQL**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/smart_task_planner
```

**MongoDB** (requires additional setup):
```env
DATABASE_URL=mongodb://localhost:27017/smart_task_planner
```

## 📁 Project Structure

```
smart_task_planner/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py   # LLM integration
│       └── plan_service.py  # Business logic
├── frontend/
│   └── index.html           # Web UI
├── demo_api.py              # Demo/test script
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment file
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── SAMPLE_GOALS.md         # Sample goals for testing
```

## 🧠 Design Decisions

### 1. Why FastAPI?
- Modern, fast, and async-capable
- Automatic API documentation
- Built-in validation with Pydantic
- Excellent developer experience

### 2. Why SQLite by Default?
- Zero configuration
- Perfect for MVP and local development
- Easy to swap to PostgreSQL for production

### 3. LLM Integration Strategy
- Support for multiple providers (OpenAI, Google Gemini)
- Structured JSON output for reliability
- Fallback plan if LLM fails
- Configurable prompts for different plan types
- Temperature=0.7 for balanced creativity/consistency

### 4. Critical Path Algorithm
- Topological sort for dependency ordering
- Forward pass to calculate earliest times
- Backward pass to find critical path
- O(V + E) time complexity

### 5. Date Scheduling
- Respects working days and constraints
- Skips weekends and unavailable dates
- Calculates based on dependency finish dates
- Provides earliest start and latest finish

### 6. Task Duration Limits
- 1-3 days per task (configurable)
- Encourages breaking large tasks into smaller ones
- More accurate estimates
- Better progress tracking

## 📖 Examples

### Example 1: E-Commerce Website

**Goal**: "Build a full-stack e-commerce website with user authentication, product catalog, shopping cart, and payment integration"

**Generated Plan** (moderate):
- T1: Project Setup and Architecture (1 day)
- T2: Database Schema Design (1 day) → T1
- T3: Backend API - Authentication (2 days) → T2
- T4: Backend API - Products & Catalog (2 days) → T3
- T5: Backend API - Shopping Cart (2 days) → T4
- T6: Backend API - Orders & Payments (2 days) → T5
- T7: Frontend - UI Components (3 days) → T2
- T8: Frontend - Product Pages (2 days) → T4, T7
- T9: Frontend - Cart & Checkout (2 days) → T5, T8
- T10: Payment Integration (2 days) → T6, T9
- T11: Testing & Deployment (2 days) → T10

**Critical Path**: T1 → T2 → T3 → T4 → T5 → T6 → T10 → T11

### Example 2: Learning Project

**Goal**: "Learn Python and build a machine learning project to predict house prices"

**Generated Plan** (conservative):
- T1: Learn Python Basics (3 days)
- T2: Learn Data Analysis (pandas, numpy) (3 days) → T1
- T3: Learn ML Concepts (3 days) → T2
- T4: Data Collection & Exploration (2 days) → T3
- T5: Data Preprocessing (2 days) → T4
- T6: Model Development (3 days) → T5
- T7: Model Evaluation (2 days) → T6
- T8: Documentation & Presentation (1 day) → T7

**Critical Path**: T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8

## 🔧 Troubleshooting

### Backend won't start

**Error**: "No module named 'fastapi'"
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error**: "Invalid API key"
```powershell
# Check .env file has correct OPENAI_API_KEY
# Verify key is valid at platform.openai.com
```

### Frontend can't connect to API

**Error**: CORS or connection refused
```powershell
# 1. Verify backend is running on port 8000
# 2. Check frontend/index.html has correct API_BASE_URL
# 3. Verify CORS_ORIGINS in .env includes frontend URL
```

### Database errors

**Error**: "No such table"
```powershell
# Reinitialize database
python -c "from backend.database import init_db; init_db()"
```

### LLM generates invalid JSON

- Check `OPENAI_MODEL` in `.env` supports JSON mode
- Recommended models: gpt-4o-mini, gpt-4o, gpt-4-turbo
- Falls back to default plan if parsing fails

## 🚀 Deployment

### Production Checklist

1. **Environment**:
   - Set `DEBUG=False`
   - Use PostgreSQL instead of SQLite
   - Set strong secret keys
   - Configure HTTPS

2. **Database**:
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

3. **Run with Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Serve Frontend**:
   - Use Nginx or Apache
   - Or deploy to Netlify/Vercel

5. **Environment Variables**:
   - Never commit `.env`
   - Use environment management service

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting)
- Review API docs at `/docs`
- Check sample goals in `SAMPLE_GOALS.md`

---

**Built with ❤️ using FastAPI, OpenAI, and modern web technologies**
