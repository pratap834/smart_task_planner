"""
FastAPI application for Smart Task Planner with MongoDB
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from config import settings
from database_mongo import connect_to_mongodb, close_mongodb_connection
from models_mongo import Goal, Plan, Task, PlanType, TaskStatus, TaskPriority
from services.llm_service import llm_service
from services.plan_service import plan_generator


# ============================================================================
# Request/Response Models
# ============================================================================

class ConstraintsRequest(BaseModel):
    """Constraints for plan generation"""
    deadline: Optional[datetime] = None
    max_hours_per_day: Optional[int] = Field(default=8, ge=1, le=24)
    no_work_on_weekends: bool = False
    unavailable_dates: List[str] = Field(default_factory=list)


class PlanCreateRequest(BaseModel):
    """Request to create a new plan"""
    goal_text: str = Field(..., min_length=10, max_length=1000)
    plan_type: PlanType = PlanType.MODERATE
    constraints: Optional[ConstraintsRequest] = None


class TaskResponse(BaseModel):
    """Task response model"""
    id: str
    plan_id: Optional[str] = None
    task_id: str
    title: str
    description: str
    duration_days: int
    earliest_start: Optional[datetime] = None
    latest_finish: Optional[datetime] = None
    depends_on: List[str] = Field(default_factory=list)
    priority: TaskPriority
    confidence: float
    status: TaskStatus = TaskStatus.PENDING
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PlanDetailResponse(BaseModel):
    """Detailed plan response with tasks"""
    id: str
    goal_id: str
    plan_type: PlanType
    critical_path: List[str] = Field(default_factory=list)
    plan_summary: str
    total_duration_days: Optional[int] = None
    estimated_completion: Optional[datetime] = None
    plan_data: Optional[Dict[str, Any]] = None
    tasks: List[TaskResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GoalResponse(BaseModel):
    """Goal response model"""
    id: str
    goal_text: str
    constraints: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskUpdateRequest(BaseModel):
    """Request to update a task"""
    status: Optional[TaskStatus] = None
    is_completed: Optional[bool] = None


# ============================================================================
# Initialize FastAPI App
# ============================================================================

app = FastAPI(
    title="Smart Task Planner API",
    description="API for generating actionable task plans from user goals using AI",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    await connect_to_mongodb()
    print("✓ MongoDB connected")
    print(f"✓ Server running on {settings.HOST}:{settings.PORT}")
    print(f"✓ LLM Provider: Google Gemini ({settings.GEMINI_MODEL})")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongodb_connection()
    print("✓ MongoDB disconnected")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "ok",
        "message": "Smart Task Planner API is running",
        "version": "2.0.0",
        "database": "MongoDB"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        await Goal.find_one()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "llm_provider": "gemini",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Plan Generation Endpoints
# ============================================================================

@app.post("/api/plans", response_model=PlanDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(request: PlanCreateRequest):
    """
    Create a new plan from a goal
    
    This endpoint:
    1. Creates a Goal document
    2. Calls LLM (Gemini) to generate task breakdown
    3. Calculates critical path
    4. Assigns dates based on constraints
    5. Stores Plan and Tasks in MongoDB
    6. Returns complete plan with tasks
    """
    try:
        # Create goal document
        goal = Goal(
            goal_text=request.goal_text,
            constraints=request.constraints.model_dump() if request.constraints else {}
        )
        await goal.insert()
        
        # Generate plan using LLM (Gemini)
        llm_response = await llm_service.generate_plan(
            goal_text=request.goal_text,
            constraints=request.constraints,
            plan_type=request.plan_type
        )
        
        # Convert LLM tasks to task objects
        task_list = []
        for llm_task in llm_response.tasks:
            task_list.append({
                "task_id": llm_task.id,
                "title": llm_task.title,
                "description": llm_task.description,
                "duration_days": llm_task.duration_days,
                "depends_on": llm_task.depends_on,
                "priority": llm_task.priority,
                "confidence": llm_task.confidence,
                "status": TaskStatus.PENDING
            })
        
        # Assign dates to tasks
        task_list = plan_generator.assign_dates(
            task_list,
            request.constraints,
            datetime.now()
        )
        
        # Calculate critical path
        critical_path = plan_generator.calculate_critical_path(task_list)
        
        # Calculate total duration and estimated completion
        total_duration = max([t.get("duration_days", 0) for t in task_list], default=0)
        estimated_completion = None
        if task_list:
            latest_finish_dates = [t.get("latest_finish") for t in task_list if t.get("latest_finish")]
            if latest_finish_dates:
                estimated_completion = max(latest_finish_dates)
        
        # Create plan document
        plan = Plan(
            goal_id=str(goal.id),
            plan_type=request.plan_type,
            critical_path=critical_path,
            plan_summary=llm_response.plan_summary,
            total_duration_days=total_duration,
            estimated_completion=estimated_completion,
            plan_data={"llm_metadata": llm_response.metadata if hasattr(llm_response, 'metadata') else {}}
        )
        await plan.insert()
        
        # Create task documents
        tasks = []
        for task_data in task_list:
            task = Task(
                plan_id=str(plan.id),
                task_id=task_data["task_id"],
                title=task_data["title"],
                description=task_data["description"],
                duration_days=task_data["duration_days"],
                earliest_start=task_data.get("earliest_start"),
                latest_finish=task_data.get("latest_finish"),
                depends_on=task_data["depends_on"],
                priority=task_data["priority"],
                confidence=task_data["confidence"],
                status=TaskStatus.PENDING
            )
            await task.insert()
            tasks.append(task)
        
        # Build response
        task_responses = [
            TaskResponse(
                id=str(task.id),
                plan_id=str(task.plan_id),
                task_id=task.task_id,
                title=task.title,
                description=task.description,
                duration_days=task.duration_days,
                earliest_start=task.earliest_start,
                latest_finish=task.latest_finish,
                depends_on=task.depends_on,
                priority=task.priority,
                confidence=task.confidence,
                status=task.status,
                is_completed=task.is_completed,
                completed_at=task.completed_at,
                created_at=task.created_at
            )
            for task in tasks
        ]
        
        return PlanDetailResponse(
            id=str(plan.id),
            goal_id=str(plan.goal_id),
            plan_type=plan.plan_type,
            critical_path=plan.critical_path,
            plan_summary=plan.plan_summary,
            total_duration_days=plan.total_duration_days,
            estimated_completion=plan.estimated_completion,
            plan_data=plan.plan_data,
            tasks=task_responses,
            created_at=plan.created_at,
            updated_at=plan.updated_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create plan: {str(e)}"
        )


@app.get("/api/plans", response_model=List[PlanDetailResponse])
async def list_plans(skip: int = 0, limit: int = 10):
    """
    List all plans with pagination
    """
    plans = await Plan.find_all().skip(skip).limit(limit).to_list()
    
    result = []
    for plan in plans:
        # Get tasks for this plan
        tasks = await Task.find(Task.plan_id == str(plan.id)).to_list()
        
        task_responses = [
            TaskResponse(
                id=str(task.id),
                plan_id=str(task.plan_id),
                task_id=task.task_id,
                title=task.title,
                description=task.description,
                duration_days=task.duration_days,
                earliest_start=task.earliest_start,
                latest_finish=task.latest_finish,
                depends_on=task.depends_on,
                priority=task.priority,
                confidence=task.confidence,
                status=task.status,
                is_completed=task.is_completed,
                completed_at=task.completed_at,
                created_at=task.created_at
            )
            for task in tasks
        ]
        
        result.append(PlanDetailResponse(
            id=str(plan.id),
            goal_id=str(plan.goal_id),
            plan_type=plan.plan_type,
            critical_path=plan.critical_path,
            plan_summary=plan.plan_summary,
            total_duration_days=plan.total_duration_days,
            estimated_completion=plan.estimated_completion,
            plan_data=plan.plan_data,
            tasks=task_responses,
            created_at=plan.created_at,
            updated_at=plan.updated_at
        ))
    
    return result


@app.get("/api/plans/{plan_id}", response_model=PlanDetailResponse)
async def get_plan(plan_id: str):
    """
    Get a specific plan by ID
    """
    try:
        plan = await Plan.get(PydanticObjectId(plan_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    # Get tasks
    tasks = await Task.find(Task.plan_id == plan_id).to_list()
    
    task_responses = [
        TaskResponse(
            id=str(task.id),
            plan_id=str(task.plan_id),
            task_id=task.task_id,
            title=task.title,
            description=task.description,
            duration_days=task.duration_days,
            earliest_start=task.earliest_start,
            latest_finish=task.latest_finish,
            depends_on=task.depends_on,
            priority=task.priority,
            confidence=task.confidence,
            status=task.status,
            is_completed=task.is_completed,
            completed_at=task.completed_at,
            created_at=task.created_at
        )
        for task in tasks
    ]
    
    return PlanDetailResponse(
        id=str(plan.id),
        goal_id=str(plan.goal_id),
        plan_type=plan.plan_type,
        critical_path=plan.critical_path,
        plan_summary=plan.plan_summary,
        total_duration_days=plan.total_duration_days,
        estimated_completion=plan.estimated_completion,
        plan_data=plan.plan_data,
        tasks=task_responses,
        created_at=plan.created_at,
        updated_at=plan.updated_at
    )


@app.delete("/api/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(plan_id: str):
    """
    Delete a plan and all its tasks
    """
    try:
        plan = await Plan.get(PydanticObjectId(plan_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    # Delete all tasks for this plan
    await Task.find(Task.plan_id == plan_id).delete()
    
    # Delete the plan
    await plan.delete()
    
    return None


# ============================================================================
# Task Management Endpoints
# ============================================================================

@app.patch("/api/plans/{plan_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(plan_id: str, task_id: str, update: TaskUpdateRequest):
    """
    Update a task (e.g., mark as completed)
    """
    # Find the task
    task = await Task.find_one(Task.plan_id == plan_id, Task.task_id == task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found in plan {plan_id}"
        )
    
    # Update fields
    if update.status is not None:
        task.status = update.status
        
        # Auto-set is_completed based on status
        if update.status == TaskStatus.COMPLETED:
            task.is_completed = True
            if not task.completed_at:
                task.completed_at = datetime.utcnow()
        else:
            task.is_completed = False
            task.completed_at = None
    
    if update.is_completed is not None:
        task.is_completed = update.is_completed
        if update.is_completed:
            task.status = TaskStatus.COMPLETED
            if not task.completed_at:
                task.completed_at = datetime.utcnow()
        else:
            if task.status == TaskStatus.COMPLETED:
                task.status = TaskStatus.PENDING
            task.completed_at = None
    
    task.updated_at = datetime.utcnow()
    await task.save()
    
    return TaskResponse(
        id=str(task.id),
        plan_id=str(task.plan_id),
        task_id=task.task_id,
        title=task.title,
        description=task.description,
        duration_days=task.duration_days,
        earliest_start=task.earliest_start,
        latest_finish=task.latest_finish,
        depends_on=task.depends_on,
        priority=task.priority,
        confidence=task.confidence,
        status=task.status,
        is_completed=task.is_completed,
        completed_at=task.completed_at,
        created_at=task.created_at
    )


@app.get("/api/plans/{plan_id}/tasks", response_model=List[TaskResponse])
async def get_plan_tasks(plan_id: str):
    """
    Get all tasks for a specific plan
    """
    # Verify plan exists
    try:
        plan = await Plan.get(PydanticObjectId(plan_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found"
        )
    
    # Get tasks
    tasks = await Task.find(Task.plan_id == plan_id).to_list()
    
    return [
        TaskResponse(
            id=str(task.id),
            plan_id=str(task.plan_id),
            task_id=task.task_id,
            title=task.title,
            description=task.description,
            duration_days=task.duration_days,
            earliest_start=task.earliest_start,
            latest_finish=task.latest_finish,
            depends_on=task.depends_on,
            priority=task.priority,
            confidence=task.confidence,
            status=task.status,
            is_completed=task.is_completed,
            completed_at=task.completed_at,
            created_at=task.created_at
        )
        for task in tasks
    ]


# ============================================================================
# Goal Endpoints
# ============================================================================

@app.post("/api/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(goal_text: str, constraints: Optional[Dict[str, Any]] = None):
    """
    Create a new goal (without generating a plan)
    """
    goal = Goal(
        goal_text=goal_text,
        constraints=constraints or {}
    )
    await goal.insert()
    
    return GoalResponse(
        id=str(goal.id),
        goal_text=goal.goal_text,
        constraints=goal.constraints,
        created_at=goal.created_at,
        updated_at=goal.updated_at
    )


@app.get("/api/goals", response_model=List[GoalResponse])
async def list_goals(skip: int = 0, limit: int = 10):
    """
    List all goals
    """
    goals = await Goal.find_all().skip(skip).limit(limit).to_list()
    
    return [
        GoalResponse(
            id=str(goal.id),
            goal_text=goal.goal_text,
            constraints=goal.constraints,
            created_at=goal.created_at,
            updated_at=goal.updated_at
        )
        for goal in goals
    ]


@app.get("/api/goals/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: str):
    """
    Get a specific goal by ID
    """
    try:
        goal = await Goal.get(PydanticObjectId(goal_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goal {goal_id} not found"
        )
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goal {goal_id} not found"
        )
    
    return GoalResponse(
        id=str(goal.id),
        goal_text=goal.goal_text,
        constraints=goal.constraints,
        created_at=goal.created_at,
        updated_at=goal.updated_at
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
