# Quick Reference Guide - Smart Task Planner

## 🚀 Quick Start Commands

```powershell
# Windows Quick Start
.\run.bat

# Manual Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your OPENAI_API_KEY
python backend/main.py

# Run Tests
pytest test_basic.py -v

# Run Demo
python demo_api.py
```

## 📡 Common API Calls

### Create a Plan
```powershell
$body = @{
    goal_text = "Build a REST API"
    plan_type = "moderate"
    constraints = @{
        max_hours_per_day = 8
        no_work_on_weekends = $true
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/plans -Method POST -Body $body -ContentType "application/json"
```

### Get All Plans
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/plans
```

### Get Specific Plan
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/plans/1
```

### Update Task Status
```powershell
$update = @{ status = "completed" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/api/plans/1/tasks/T1 -Method PATCH -Body $update -ContentType "application/json"
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Choose LLM Provider
LLM_PROVIDER=openai  # or "gemini"

# OpenAI (if LLM_PROVIDER=openai)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini

# Google Gemini (if LLM_PROVIDER=gemini)
GEMINI_API_KEY=your-gemini-key-here
GEMINI_MODEL=gemini-1.5-flash

# Other settings
DATABASE_URL=sqlite:///./smart_task_planner.db
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Use Google Gemini
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash
# Get key at: https://makersuite.google.com/app/apikey
```

### Use OpenAI GPT
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
# Get key at: https://platform.openai.com/api-keys
```

### Use Different LLM
```env
# OpenRouter
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_API_KEY=sk-or-v1-...
OPENAI_MODEL=anthropic/claude-3-5-sonnet

# Local Ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=not-needed
OPENAI_MODEL=llama3
```

### Use PostgreSQL
```env
DATABASE_URL=postgresql://user:password@localhost:5432/smart_task_planner
```

## 📂 File Locations

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI application |
| `backend/models.py` | Database models |
| `backend/schemas.py` | API schemas |
| `backend/services/llm_service.py` | LLM integration |
| `backend/services/plan_service.py` | Business logic |
| `frontend/index.html` | Web UI |
| `demo_api.py` | Demo script |
| `test_basic.py` | Tests |
| `.env` | Configuration |

## 🎯 Sample Goals

### Quick Test Goals
```
1. "Build a REST API for a blog platform"
2. "Learn Python and create a data analysis project"
3. "Migrate application to microservices"
4. "Create a mobile app for habit tracking"
5. "Set up CI/CD pipeline with automated testing"
```

## 🔍 Troubleshooting

### Backend Won't Start
```powershell
# Check virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Check .env file
Get-Content .env
```

### API Key Error
```powershell
# Verify API key in .env
Select-String -Path .env -Pattern "OPENAI_API_KEY"

# Test API key manually
$headers = @{ "Authorization" = "Bearer sk-your-key" }
Invoke-RestMethod -Uri https://api.openai.com/v1/models -Headers $headers
```

### Database Error
```powershell
# Delete and recreate database
Remove-Item smart_task_planner.db
python -c "from backend.database import init_db; init_db()"
```

### Frontend Can't Connect
1. Verify backend is running: http://localhost:8000/health
2. Check CORS_ORIGINS in .env includes frontend URL
3. Check browser console for errors

## 📊 Response Schema

### Plan Response
```json
{
  "id": 1,
  "goal_id": 1,
  "plan_summary": "Plan overview...",
  "critical_path": ["T1", "T3", "T5"],
  "status": "active",
  "plan_type": "moderate",
  "tasks": [
    {
      "id": "T1",
      "title": "Task Title",
      "description": "Description...",
      "duration_days": 2,
      "earliest_start": "2025-10-16",
      "latest_finish": "2025-10-18",
      "depends_on": [],
      "priority": "High",
      "confidence": 0.9,
      "status": "pending"
    }
  ],
  "created_at": "2025-10-16T10:00:00",
  "updated_at": "2025-10-16T10:00:00"
}
```

## 🎨 Customization

### Change Task Duration Range
Edit `backend/services/llm_service.py`:
```python
# Line ~55
"Duration should be 1-3 days for most tasks"
# Change to: "Duration should be 1-5 days for most tasks"
```

### Change Number of Tasks
Edit `backend/services/llm_service.py`:
```python
# Line ~60
"Break complex goals into 5-15 tasks"
# Change to: "Break complex goals into 10-20 tasks"
```

### Add Custom Priority
Edit `backend/schemas.py`:
```python
allowed = ['High', 'Medium', 'Low', 'Critical']
```

### Modify UI Colors
Edit `frontend/index.html` CSS:
```css
/* Line ~30 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🧪 Testing

### Run All Tests
```powershell
pytest test_basic.py -v
```

### Run Specific Test
```powershell
pytest test_basic.py::TestSchemas::test_constraints_creation -v
```

### Test Coverage
```powershell
pytest test_basic.py --cov=backend --cov-report=html
```

## 📈 Performance Tips

### Speed Up Plan Generation
1. Use faster model: `gpt-4o-mini` or `gpt-3.5-turbo`
2. Reduce temperature: `temperature=0.3`
3. Cache common requests

### Database Performance
1. Add indexes on frequently queried fields
2. Use connection pooling
3. Enable query logging to find slow queries

### Frontend Performance
1. Lazy load large plans
2. Paginate task lists
3. Cache API responses

## 🔐 Security Checklist

- [ ] Change DEBUG=False in production
- [ ] Set strong DATABASE_URL password
- [ ] Restrict CORS_ORIGINS to actual domains
- [ ] Keep OPENAI_API_KEY secret
- [ ] Use HTTPS in production
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Sanitize user inputs
- [ ] Regular dependency updates

## 📞 Useful URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000 | API root |
| http://localhost:8000/health | Health check |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc UI |
| frontend/index.html | Web UI |

## 💡 Pro Tips

1. **Use plan types strategically**:
   - `aggressive`: Tight deadlines, high risk
   - `moderate`: Balanced approach (default)
   - `conservative`: Safe timelines, buffer time

2. **Leverage constraints**:
   - Set realistic `max_hours_per_day`
   - Mark `no_work_on_weekends` if applicable
   - Add `unavailable_dates` for holidays

3. **Critical path awareness**:
   - Focus on critical path tasks first
   - Delays here impact overall timeline
   - Non-critical tasks have flexibility

4. **Monitor confidence scores**:
   - Low confidence (<0.7) = higher risk
   - Review and adjust estimates
   - Add buffer for uncertain tasks

5. **Iterative refinement**:
   - Start with moderate plan
   - Review task breakdown
   - Regenerate with adjusted constraints

## 🔄 Common Workflows

### Generate Multiple Plan Types
```python
import requests

goal = "Build a web application"
for plan_type in ["aggressive", "moderate", "conservative"]:
    response = requests.post("http://localhost:8000/api/plans", json={
        "goal_text": goal,
        "plan_type": plan_type
    })
    plan = response.json()
    print(f"{plan_type}: {len(plan['tasks'])} tasks")
```

### Track Progress
```python
plan_id = 1
tasks = requests.get(f"http://localhost:8000/api/plans/{plan_id}/tasks").json()

completed = sum(1 for t in tasks if t['status'] == 'completed')
total = len(tasks)
print(f"Progress: {completed}/{total} ({100*completed//total}%)")
```

### Export to CSV
```python
import csv
import requests

plan = requests.get("http://localhost:8000/api/plans/1").json()

with open('plan.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Title', 'Duration', 'Priority', 'Status'])
    for task in plan['tasks']:
        writer.writerow([
            task['id'],
            task['title'],
            task['duration_days'],
            task['priority'],
            task['status']
        ])
```

## 🎓 Learning Path

1. **Understand the basics**: Read README.md
2. **Try the demo**: Run `demo_api.py`
3. **Explore the API**: Visit /docs
4. **Test sample goals**: Use SAMPLE_GOALS.md
5. **Review architecture**: Read ARCHITECTURE.md
6. **Customize**: Modify prompts, UI, logic
7. **Deploy**: Follow deployment guide

## 📝 Cheat Sheet

```powershell
# Start backend
python backend/main.py

# Check health
curl http://localhost:8000/health

# Create plan
$goal = @{goal_text="Test"} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/api/plans -Method POST -Body $goal -ContentType "application/json"

# List plans
curl http://localhost:8000/api/plans

# Update task
$update = @{status="completed"} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/api/plans/1/tasks/T1 -Method PATCH -Body $update -ContentType "application/json"

# Run tests
pytest test_basic.py -v

# View logs
Get-Content backend.log -Tail 50

# Database shell
sqlite3 smart_task_planner.db
```

---

**Quick Reference - Keep this handy!** 📚
