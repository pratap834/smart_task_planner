"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


# ============================================================================
# Constraint Schemas
# ============================================================================

class Constraints(BaseModel):
    """User constraints for plan generation"""
    deadline: Optional[str] = Field(default=None, description="Final deadline (YYYY-MM-DD)")
    max_hours_per_day: Optional[int] = Field(default=8, description="Maximum work hours per day", ge=1, le=24)
    no_work_on_weekends: Optional[bool] = Field(default=True, description="Whether to exclude weekends")
    unavailable_dates: Optional[List[str]] = Field(default_factory=list, description="List of unavailable dates (YYYY-MM-DD)")


# ============================================================================
# Goal Schemas
# ============================================================================

class GoalCreate(BaseModel):
    """Schema for creating a new goal"""
    goal_text: str = Field(..., description="The user's goal description", min_length=10)
    constraints: Optional[Constraints] = Field(None, description="Optional constraints")


class GoalResponse(BaseModel):
    """Schema for goal response"""
    id: int
    goal_text: str
    constraints: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Task Schemas
# ============================================================================

class TaskResponse(BaseModel):
    """Schema for task in API response"""
    id: str = Field(..., description="Task ID (e.g., T1)")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed description")
    duration_days: int = Field(..., description="Estimated duration in days", ge=1, le=30)
    earliest_start: Optional[str] = Field(default=None, description="Earliest start date (YYYY-MM-DD)")
    latest_finish: Optional[str] = Field(default=None, description="Latest finish date (YYYY-MM-DD)")
    depends_on: List[str] = Field(default_factory=list, description="List of dependency task IDs")
    priority: str = Field(default="Medium", description="Priority level (High/Medium/Low)")
    confidence: float = Field(default=1.0, description="Confidence score (0-1)", ge=0.0, le=1.0)
    status: str = Field(default="pending", description="Task status")
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        allowed = ['High', 'Medium', 'Low']
        if v not in allowed:
            raise ValueError(f'Priority must be one of {allowed}')
        return v


class TaskUpdateRequest(BaseModel):
    """Schema for updating a task"""
    status: Optional[str] = Field(None, description="New status (pending/in_progress/completed/blocked)")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None:
            allowed = ['pending', 'in_progress', 'completed', 'blocked']
            if v not in allowed:
                raise ValueError(f'Status must be one of {allowed}')
        return v


# ============================================================================
# Plan Schemas
# ============================================================================

class PlanResponse(BaseModel):
    """Schema for plan response"""
    tasks: List[TaskResponse]
    critical_path: List[str] = Field(default_factory=list, description="Critical path task IDs")
    plan_summary: str = Field(..., description="High-level explanation of the plan")


class PlanCreateRequest(BaseModel):
    """Schema for creating a plan from a goal"""
    goal_text: str = Field(..., description="The user's goal", min_length=10)
    constraints: Optional[Constraints] = Field(default=None, description="Optional constraints")
    plan_type: Optional[str] = Field(default="moderate", description="Plan type (moderate/aggressive/conservative)")
    
    @field_validator('plan_type')
    @classmethod
    def validate_plan_type(cls, v):
        allowed = ['moderate', 'aggressive', 'conservative']
        if v not in allowed:
            raise ValueError(f'Plan type must be one of {allowed}')
        return v


class PlanDetailResponse(BaseModel):
    """Schema for detailed plan response with metadata"""
    id: int
    goal_id: int
    plan_summary: str
    critical_path: List[str]
    status: str
    plan_type: str
    tasks: List[TaskResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# LLM Response Schema (Internal)
# ============================================================================

class LLMTaskResponse(BaseModel):
    """Schema for task generated by LLM"""
    id: str
    title: str
    description: str
    duration_days: int
    depends_on: List[str] = Field(default_factory=list)
    priority: str = "Medium"
    confidence: float = 1.0


class LLMPlanResponse(BaseModel):
    """Schema for complete plan generated by LLM"""
    tasks: List[LLMTaskResponse]
    plan_summary: str
