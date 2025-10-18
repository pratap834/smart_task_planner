# Smart Task Planner - Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │                    Frontend (Web UI)                      │    │
│  │  • HTML/CSS/JavaScript                                    │    │
│  │  • Goal Input Form                                        │    │
│  │  • Constraint Configuration                               │    │
│  │  • Plan Visualization                                     │    │
│  │  • Task Management                                        │    │
│  └───────────────────────────────────────────────────────────┘    │
│                                                                     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP/JSON
                               │ REST API
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API LAYER (FastAPI)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Endpoints:                                                         │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ POST   /api/plans          → Create Plan                 │     │
│  │ GET    /api/plans          → List Plans                  │     │
│  │ GET    /api/plans/{id}     → Get Plan                    │     │
│  │ PATCH  /api/plans/{id}/... → Update Task                 │     │
│  │ POST   /api/goals          → Create Goal                 │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Middleware:                                                        │
│  • CORS Handling                                                   │
│  • Request Validation (Pydantic)                                   │
│  • Error Handling                                                  │
│                                                                     │
└──────────────────┬──────────────────────────┬──────────────────────┘
                   │                          │
                   ▼                          ▼
    ┌──────────────────────────┐  ┌─────────────────────────┐
    │   SERVICE LAYER          │  │   DATABASE LAYER        │
    ├──────────────────────────┤  ├─────────────────────────┤
    │                          │  │                         │
    │  ┌────────────────────┐  │  │  ┌──────────────────┐  │
    │  │   LLM Service      │  │  │  │   SQLAlchemy     │  │
    │  │  ────────────      │  │  │  │   ORM Layer      │  │
    │  │  • OpenAI API      │  │  │  │  ──────────      │  │
    │  │  • Prompt Builder  │  │  │  │  • Goal Model    │  │
    │  │  • JSON Parser     │  │  │  │  • Plan Model    │  │
    │  │  • Fallback Logic  │  │  │  │  • Task Model    │  │
    │  └────────────────────┘  │  │  └──────────────────┘  │
    │                          │  │           │             │
    │  ┌────────────────────┐  │  │           ▼             │
    │  │   Plan Service     │  │  │  ┌──────────────────┐  │
    │  │  ────────────      │  │  │  │   Database       │  │
    │  │  • Critical Path   │  │  │  │  ──────────      │  │
    │  │  • Task Scheduling │  │  │  │  SQLite/         │  │
    │  │  • Dependency Mgmt │  │  │  │  PostgreSQL/     │  │
    │  │  • Date Calculation│  │  │  │  MongoDB         │  │
    │  └────────────────────┘  │  │  └──────────────────┘  │
    │                          │  │                         │
    └──────────────────────────┘  └─────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐
│  User    │
│  Input   │
└────┬─────┘
     │
     │ 1. Submit Goal + Constraints
     ▼
┌─────────────────────────────────────────┐
│         API Endpoint Handler            │
│  • Validate request (Pydantic)          │
│  • Create Goal record in DB             │
└────┬────────────────────────────────────┘
     │
     │ 2. Request task breakdown
     ▼
┌─────────────────────────────────────────┐
│          LLM Service                    │
│  • Build context-rich prompt            │
│  • Call OpenAI API                      │
│  • Parse structured JSON response       │
│  • Validate task structure              │
└────┬────────────────────────────────────┘
     │
     │ 3. Tasks with dependencies
     ▼
┌─────────────────────────────────────────┐
│          Plan Service                   │
│  • Topological sort (dependencies)      │
│  • Calculate critical path              │
│  • Assign dates (respect constraints)   │
│  • Validate against constraints         │
└────┬────────────────────────────────────┘
     │
     │ 4. Complete plan structure
     ▼
┌─────────────────────────────────────────┐
│          Database Layer                 │
│  • Save Plan record                     │
│  • Save Task records                    │
│  • Link relationships                   │
└────┬────────────────────────────────────┘
     │
     │ 5. Return plan with tasks
     ▼
┌─────────────────────────────────────────┐
│          API Response                   │
│  • Serialize to JSON                    │
│  • Include all task details             │
│  • Include critical path                │
└────┬────────────────────────────────────┘
     │
     │ 6. Display to user
     ▼
┌──────────┐
│ Frontend │
│ Renders  │
│ Plan     │
└──────────┘
```

## Critical Path Calculation Algorithm

```
Input: List of tasks with dependencies and durations

Step 1: Topological Sort
┌─────────────────────────────────────┐
│ Tasks: T1, T2(→T1), T3(→T2)         │
│                                     │
│ Build adjacency list:               │
│   T1 → [T2]                         │
│   T2 → [T3]                         │
│   T3 → []                           │
│                                     │
│ Calculate in-degrees:               │
│   T1: 0, T2: 1, T3: 1               │
│                                     │
│ Kahn's Algorithm:                   │
│   Queue: [T1]                       │
│   Process T1 → Queue: [T2]          │
│   Process T2 → Queue: [T3]          │
│   Process T3 → Done                 │
│                                     │
│ Result: [T1, T2, T3]                │
└─────────────────────────────────────┘

Step 2: Forward Pass (Earliest Times)
┌─────────────────────────────────────┐
│ For each task in sorted order:     │
│                                     │
│ T1: ES=0, EF=0+2=2                  │
│ T2: ES=max(2)=2, EF=2+3=5           │
│ T3: ES=max(5)=5, EF=5+1=6           │
│                                     │
│ Project Duration: 6 days            │
└─────────────────────────────────────┘

Step 3: Backward Pass (Critical Path)
┌─────────────────────────────────────┐
│ Start from end task (T3):           │
│   T3 is on critical path            │
│                                     │
│ Find predecessor with max EF:       │
│   T3 depends on T2                  │
│   T2's EF = 5 (max)                 │
│   T2 is on critical path            │
│                                     │
│ Continue backtracking:              │
│   T2 depends on T1                  │
│   T1's EF = 2 (max)                 │
│   T1 is on critical path            │
│                                     │
│ Critical Path: [T1, T2, T3]         │
└─────────────────────────────────────┘
```

## Database Schema

```sql
┌─────────────────────────────────────────┐
│              goals                      │
├─────────────────────────────────────────┤
│ PK  id              INTEGER             │
│     goal_text       TEXT                │
│     constraints     JSON                │
│     created_at      DATETIME            │
│     updated_at      DATETIME            │
└──────────────┬──────────────────────────┘
               │
               │ 1:N
               ▼
┌─────────────────────────────────────────┐
│              plans                      │
├─────────────────────────────────────────┤
│ PK  id              INTEGER             │
│ FK  goal_id         INTEGER             │
│     plan_summary    TEXT                │
│     critical_path   JSON                │
│     status          VARCHAR(50)         │
│     plan_type       VARCHAR(50)         │
│     created_at      DATETIME            │
│     updated_at      DATETIME            │
└──────────────┬──────────────────────────┘
               │
               │ 1:N
               ▼
┌─────────────────────────────────────────┐
│              tasks                      │
├─────────────────────────────────────────┤
│ PK  id              INTEGER             │
│ FK  plan_id         INTEGER             │
│     task_id         VARCHAR(50)         │
│     title           VARCHAR(255)        │
│     description     TEXT                │
│     duration_days   INTEGER             │
│     earliest_start  VARCHAR(50)         │
│     latest_finish   VARCHAR(50)         │
│     depends_on      JSON                │
│     priority        VARCHAR(50)         │
│     confidence      FLOAT               │
│     status          VARCHAR(50)         │
│     completed_at    DATETIME            │
│     created_at      DATETIME            │
│     updated_at      DATETIME            │
└─────────────────────────────────────────┘
```

## Component Interaction Sequence

```
User → Frontend → API → Services → Database

Example: Create Plan
────────────────────────────────────────────────

1. User enters goal in frontend
   Frontend: Build request payload

2. Frontend → API: POST /api/plans
   {goal_text, constraints, plan_type}

3. API validates request with Pydantic
   ✓ goal_text length ≥ 10
   ✓ plan_type in [aggressive, moderate, conservative]
   ✓ constraints format valid

4. API creates Goal in database
   Goal(id=1, goal_text=..., constraints=...)

5. API calls LLM Service
   LLMService.generate_plan(goal, constraints, type)
   
6. LLM Service builds prompt
   System: "You are an expert planner..."
   User: "Goal: ... Constraints: ..."

7. LLM Service calls OpenAI API
   Response: {tasks: [...], plan_summary: "..."}

8. LLM Service returns parsed response
   LLMPlanResponse with validated tasks

9. API calls Plan Service
   PlanService.assign_dates(tasks, constraints)
   PlanService.calculate_critical_path(tasks)

10. Plan Service returns enriched tasks
    Tasks with start/end dates and critical path

11. API creates Plan in database
    Plan(id=1, goal_id=1, critical_path=[...])

12. API creates Tasks in database
    Task(id=1, plan_id=1, task_id="T1", ...)
    Task(id=2, plan_id=1, task_id="T2", ...)
    ...

13. API builds response
    PlanDetailResponse with all data

14. API → Frontend: 201 Created
    {id, tasks, critical_path, plan_summary}

15. Frontend displays plan
    Render task cards, highlight critical path
```

## LLM Prompting Strategy

```
System Prompt (Role Definition)
├── Expert Identity
│   "You are an expert project planner..."
│
├── Core Responsibilities
│   • Break down goals into tasks
│   • Estimate durations
│   • Identify dependencies
│   • Respect constraints
│
├── Output Format
│   • Strict JSON schema
│   • Task structure requirements
│   • Field validations
│
└── Quality Guidelines
    • Realistic estimates (1-3 days)
    • Logical sequencing
    • Clear descriptions

User Prompt (Context)
├── Goal Text
│   "Build a full-stack web application..."
│
├── Plan Type
│   • Aggressive: Minimize timeline
│   • Moderate: Balance speed/safety
│   • Conservative: Extra buffer time
│
└── Constraints
    ├── Deadline: "2025-12-31"
    ├── Max Hours/Day: 8
    ├── No Weekends: true
    └── Unavailable Dates: [...]

Response Processing
├── Parse JSON
├── Validate Structure
│   ✓ All required fields present
│   ✓ Task IDs sequential (T1, T2, ...)
│   ✓ Durations in valid range
│   ✓ Dependencies reference valid tasks
│
├── Handle Errors
│   • JSON parse error → Fallback plan
│   • Validation error → Fallback plan
│   • API error → Fallback plan
│
└── Return LLMPlanResponse
```

## Error Handling Flow

```
Request Processing
        │
        ▼
┌───────────────┐
│  Validation   │ → Error → 422 Unprocessable Entity
└───────┬───────┘
        │ ✓
        ▼
┌───────────────┐
│  Database     │ → Error → Rollback → 500 Internal Error
└───────┬───────┘
        │ ✓
        ▼
┌───────────────┐
│  LLM Service  │ → Error → Fallback Plan → Continue
└───────┬───────┘
        │ ✓
        ▼
┌───────────────┐
│  Plan Service │ → Error → 500 Internal Error
└───────┬───────┘
        │ ✓
        ▼
┌───────────────┐
│  Response     │ → Success → 201 Created
└───────────────┘
```

## Deployment Architecture

```
Production Setup
────────────────────────────────────────

┌─────────────────────────────────────┐
│          Load Balancer              │
│          (Nginx/Apache)             │
└───────────┬─────────────────────────┘
            │
            ├─────────────┬─────────────┐
            ▼             ▼             ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  Backend    │ │  Backend    │ │  Backend    │
    │  Instance 1 │ │  Instance 2 │ │  Instance N │
    │  (Gunicorn) │ │  (Gunicorn) │ │  (Gunicorn) │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┴───────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   PostgreSQL    │
                  │   Database      │
                  └─────────────────┘

Static Files
────────────
Frontend → CDN (Netlify/Vercel/S3)
```

## Security Considerations

```
Authentication
├── API Key Authentication
├── JWT Tokens
└── OAuth 2.0

Authorization
├── Role-Based Access Control
├── Resource Ownership
└── Permission Checks

Data Protection
├── HTTPS Only
├── SQL Injection Prevention (ORM)
├── XSS Prevention (Input Validation)
├── CSRF Protection
└── Rate Limiting

API Security
├── CORS Configuration
├── Request Size Limits
├── Timeout Configuration
└── Error Message Sanitization
```

## Monitoring & Observability

```
Metrics to Track
────────────────
• Request rate (req/sec)
• Response time (p50, p95, p99)
• Error rate (4xx, 5xx)
• Database query time
• LLM API latency
• Cache hit rate

Logging
────────
• Structured logging (JSON)
• Request/Response logging
• Error tracking (Sentry)
• Performance monitoring

Health Checks
─────────────
• /health endpoint
• Database connectivity
• LLM API availability
• Dependency status
```

## Scaling Strategies

```
Horizontal Scaling
├── Multiple backend instances
├── Load balancing
├── Stateless design
└── Session management

Vertical Scaling
├── Increase instance resources
├── Database optimization
└── Query optimization

Caching
├── Redis for session data
├── API response caching
├── LLM response caching
└── Database query caching

Database Scaling
├── Read replicas
├── Connection pooling
├── Query optimization
└── Indexing strategy
```

---

**Architecture designed for scalability, maintainability, and extensibility** 🏗️
