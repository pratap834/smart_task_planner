# API Examples - Smart Task Planner

This document provides practical examples of using the Smart Task Planner API.

## Table of Contents
- [Authentication](#authentication)
- [Creating Plans](#creating-plans)
- [Retrieving Plans](#retrieving-plans)
- [Managing Tasks](#managing-tasks)
- [Example Workflows](#example-workflows)

## Authentication

Currently, the API doesn't require authentication (MVP). In production, add:
- API keys
- JWT tokens
- OAuth 2.0

## Creating Plans

### Basic Plan Creation

```bash
curl -X POST http://localhost:8000/api/plans \
  -H "Content-Type: application/json" \
  -d '{
    "goal_text": "Build a REST API for a blog platform with authentication",
    "plan_type": "moderate"
  }'
```

### Plan with Constraints

```bash
curl -X POST http://localhost:8000/api/plans \
  -H "Content-Type: application/json" \
  -d '{
    "goal_text": "Learn React and build a portfolio website",
    "plan_type": "conservative",
    "constraints": {
      "deadline": "2025-11-30",
      "max_hours_per_day": 4,
      "no_work_on_weekends": true,
      "unavailable_dates": ["2025-11-25", "2025-11-26"]
    }
  }'
```

### PowerShell Example

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    goal_text = "Migrate application to microservices"
    plan_type = "moderate"
    constraints = @{
        max_hours_per_day = 8
        no_work_on_weekends = $true
        unavailable_dates = @()
    }
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/plans" `
    -Method POST `
    -Headers $headers `
    -Body $body

$response | ConvertTo-Json -Depth 10
```

### Python Example

```python
import requests

url = "http://localhost:8000/api/plans"
payload = {
    "goal_text": "Build a machine learning model for image classification",
    "plan_type": "aggressive",
    "constraints": {
        "deadline": "2025-11-15",
        "max_hours_per_day": 10,
        "no_work_on_weekends": False
    }
}

response = requests.post(url, json=payload)
plan = response.json()

print(f"Plan ID: {plan['id']}")
print(f"Number of tasks: {len(plan['tasks'])}")
print(f"Critical path: {' → '.join(plan['critical_path'])}")
```

### JavaScript Example

```javascript
const createPlan = async () => {
  const response = await fetch('http://localhost:8000/api/plans', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      goal_text: 'Create a mobile app for expense tracking',
      plan_type: 'moderate',
      constraints: {
        max_hours_per_day: 6,
        no_work_on_weekends: true
      }
    })
  });

  const plan = await response.json();
  console.log('Plan created:', plan);
  return plan;
};

createPlan();
```

## Retrieving Plans

### Get Specific Plan

```bash
curl http://localhost:8000/api/plans/1
```

### List All Plans

```bash
# Get first 10 plans
curl http://localhost:8000/api/plans

# Get plans with pagination
curl "http://localhost:8000/api/plans?skip=10&limit=5"
```

### Get Plan Tasks

```bash
curl http://localhost:8000/api/plans/1/tasks
```

## Managing Tasks

### Update Task Status

#### Mark as In Progress

```bash
curl -X PATCH http://localhost:8000/api/plans/1/tasks/T1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

#### Mark as Completed

```bash
curl -X PATCH http://localhost:8000/api/plans/1/tasks/T1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

#### Mark as Blocked

```bash
curl -X PATCH http://localhost:8000/api/plans/1/tasks/T3 \
  -H "Content-Type: application/json" \
  -d '{"status": "blocked"}'
```

### PowerShell Task Update

```powershell
$taskUpdate = @{
    status = "completed"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:8000/api/plans/1/tasks/T1" `
    -Method PATCH `
    -Headers @{"Content-Type"="application/json"} `
    -Body $taskUpdate
```

## Example Workflows

### Workflow 1: Complete Plan Lifecycle

```python
import requests
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000/api"

# 1. Create a plan
plan_response = requests.post(f"{API_BASE}/plans", json={
    "goal_text": "Build a REST API with authentication and CRUD operations",
    "plan_type": "moderate",
    "constraints": {
        "deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        "max_hours_per_day": 8,
        "no_work_on_weekends": True
    }
})

plan = plan_response.json()
plan_id = plan['id']
print(f"✓ Created plan {plan_id} with {len(plan['tasks'])} tasks")

# 2. Display tasks
print("\nTasks:")
for task in plan['tasks']:
    print(f"  [{task['id']}] {task['title']} ({task['duration_days']} days)")

# 3. Start first task
first_task_id = plan['tasks'][0]['id']
requests.patch(
    f"{API_BASE}/plans/{plan_id}/tasks/{first_task_id}",
    json={"status": "in_progress"}
)
print(f"\n✓ Started task {first_task_id}")

# 4. Complete first task
requests.patch(
    f"{API_BASE}/plans/{plan_id}/tasks/{first_task_id}",
    json={"status": "completed"}
)
print(f"✓ Completed task {first_task_id}")

# 5. Retrieve updated plan
updated_plan = requests.get(f"{API_BASE}/plans/{plan_id}").json()
completed_tasks = [t for t in updated_plan['tasks'] if t['status'] == 'completed']
print(f"\n✓ Progress: {len(completed_tasks)}/{len(updated_plan['tasks'])} tasks completed")
```

### Workflow 2: Compare Plan Types

```python
import requests

API_BASE = "http://localhost:8000/api"
goal = "Develop a mobile app for fitness tracking"

plan_types = ["aggressive", "moderate", "conservative"]
results = {}

for plan_type in plan_types:
    response = requests.post(f"{API_BASE}/plans", json={
        "goal_text": goal,
        "plan_type": plan_type
    })
    
    plan = response.json()
    results[plan_type] = {
        "tasks": len(plan['tasks']),
        "critical_path_length": len(plan['critical_path']),
        "total_days": sum(t['duration_days'] for t in plan['tasks'])
    }

print("Plan Type Comparison:")
for plan_type, stats in results.items():
    print(f"\n{plan_type.upper()}:")
    print(f"  Tasks: {stats['tasks']}")
    print(f"  Critical path: {stats['critical_path_length']} tasks")
    print(f"  Total duration: {stats['total_days']} days")
```

### Workflow 3: Batch Task Updates

```python
import requests

API_BASE = "http://localhost:8000/api"
plan_id = 1

# Get all tasks
plan = requests.get(f"{API_BASE}/plans/{plan_id}").json()

# Complete tasks in order
for task in plan['tasks']:
    # Skip if has incomplete dependencies
    if task['depends_on']:
        incomplete_deps = [
            dep for dep in task['depends_on']
            if any(t['id'] == dep and t['status'] != 'completed' 
                   for t in plan['tasks'])
        ]
        if incomplete_deps:
            print(f"⏸ Skipping {task['id']} (waiting on {incomplete_deps})")
            continue
    
    # Mark as completed
    requests.patch(
        f"{API_BASE}/plans/{plan_id}/tasks/{task['id']}",
        json={"status": "completed"}
    )
    print(f"✓ Completed {task['id']}: {task['title']}")
```

## Response Examples

### Successful Plan Creation

```json
{
  "id": 1,
  "goal_id": 1,
  "plan_summary": "This plan breaks down the goal into 8 sequential tasks...",
  "critical_path": ["T1", "T2", "T4", "T6", "T8"],
  "status": "active",
  "plan_type": "moderate",
  "tasks": [
    {
      "id": "T1",
      "title": "Project Setup and Requirements",
      "description": "Set up development environment, define requirements...",
      "duration_days": 1,
      "earliest_start": "2025-10-16",
      "latest_finish": "2025-10-17",
      "depends_on": [],
      "priority": "High",
      "confidence": 0.95,
      "status": "pending"
    },
    {
      "id": "T2",
      "title": "Database Design",
      "description": "Design database schema, create ER diagrams...",
      "duration_days": 2,
      "earliest_start": "2025-10-17",
      "latest_finish": "2025-10-21",
      "depends_on": ["T1"],
      "priority": "High",
      "confidence": 0.9,
      "status": "pending"
    }
  ],
  "created_at": "2025-10-16T10:30:00.000Z",
  "updated_at": "2025-10-16T10:30:00.000Z"
}
```

### Error Response

```json
{
  "detail": "Failed to create plan: Invalid goal text"
}
```

## Testing with cURL

### Full cURL Test Suite

```bash
#!/bin/bash

API_BASE="http://localhost:8000/api"

# Test 1: Health check
echo "=== Health Check ==="
curl -s http://localhost:8000/health | jq

# Test 2: Create plan
echo -e "\n=== Create Plan ==="
PLAN_ID=$(curl -s -X POST $API_BASE/plans \
  -H "Content-Type: application/json" \
  -d '{
    "goal_text": "Build a blog platform",
    "plan_type": "moderate"
  }' | jq -r '.id')

echo "Created plan ID: $PLAN_ID"

# Test 3: Get plan
echo -e "\n=== Get Plan ==="
curl -s $API_BASE/plans/$PLAN_ID | jq '.plan_summary'

# Test 4: Update first task
echo -e "\n=== Update Task ==="
curl -s -X PATCH $API_BASE/plans/$PLAN_ID/tasks/T1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}' | jq '.status'

# Test 5: List all plans
echo -e "\n=== List Plans ==="
curl -s $API_BASE/plans | jq 'length'
```

## Rate Limiting Considerations

The current MVP doesn't implement rate limiting, but for production:

```python
# Example with rate limiting
from time import sleep

def create_plans_with_rate_limit(goals, requests_per_minute=10):
    delay = 60 / requests_per_minute
    results = []
    
    for goal in goals:
        response = requests.post(f"{API_BASE}/plans", json={
            "goal_text": goal
        })
        results.append(response.json())
        sleep(delay)
    
    return results
```

## WebSocket Support (Future)

For real-time updates, consider implementing WebSockets:

```javascript
// Example future implementation
const ws = new WebSocket('ws://localhost:8000/ws/plan/1');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Task updated:', update);
};

// Update task
ws.send(JSON.stringify({
  action: 'update_task',
  task_id: 'T1',
  status: 'completed'
}));
```

---

For more examples, see:
- `demo_api.py` - Python demo script
- `SAMPLE_GOALS.md` - Sample goals to test
- `/docs` - Interactive API documentation
