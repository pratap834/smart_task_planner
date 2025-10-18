"""
MongoDB Document Models using Beanie ODM
"""
from beanie import Document, Link
from pydantic import Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    """Task priority enumeration"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class PlanType(str, Enum):
    """Plan type enumeration"""
    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    CONSERVATIVE = "conservative"


class Task(Document):
    """Task document model"""
    plan_id: str  # Reference to Plan
    task_id: str  # T1, T2, T3, etc.
    title: str
    description: str
    duration_days: int
    earliest_start: str  # ISO date string
    latest_finish: str  # ISO date string
    depends_on: List[str] = Field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    status: TaskStatus = TaskStatus.PENDING
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "tasks"
        indexes = [
            "plan_id",
            "task_id",
            "status",
            [("plan_id", 1), ("task_id", 1)],  # Compound index
        ]


class Plan(Document):
    """Plan document model"""
    goal_id: str  # Reference to Goal
    plan_type: PlanType = PlanType.MODERATE
    critical_path: List[str] = Field(default_factory=list)
    plan_summary: str
    total_duration_days: Optional[int] = None
    estimated_completion: Optional[str] = None  # ISO date string
    plan_data: Optional[Dict[str, Any]] = None  # Additional plan metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "plans"
        indexes = [
            "goal_id",
            "created_at",
        ]


class Goal(Document):
    """Goal document model"""
    goal_text: str
    constraints: Optional[Dict[str, Any]] = None  # deadline, max_hours_per_day, etc.
    user_id: Optional[str] = None  # For future authentication
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "goals"
        indexes = [
            "user_id",
            "created_at",
        ]
