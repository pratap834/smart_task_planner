"""
Database models for Smart Task Planner
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Goal(Base):
    """
    Represents a user goal to be broken down into tasks
    """
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints as JSON
    constraints = Column(JSON, nullable=True)
    # {
    #   "deadline": "2025-12-31",
    #   "max_hours_per_day": 8,
    #   "no_work_on_weekends": true,
    #   "unavailable_dates": ["2025-12-25", "2025-01-01"]
    # }
    
    # Relationships
    plans = relationship("Plan", back_populates="goal", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Goal(id={self.id}, goal_text='{self.goal_text[:50]}...')>"


class Plan(Base):
    """
    Represents a generated plan for a goal
    """
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    plan_summary = Column(Text, nullable=True)
    critical_path = Column(JSON, nullable=True)  # List of task IDs ["T1", "T3", "T5"]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status: draft, active, completed, archived
    status = Column(String(50), default="active")
    
    # Plan type: moderate, aggressive, conservative
    plan_type = Column(String(50), default="moderate")
    
    # Relationships
    goal = relationship("Goal", back_populates="plans")
    tasks = relationship("Task", back_populates="plan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Plan(id={self.id}, goal_id={self.goal_id}, status='{self.status}')>"


class Task(Base):
    """
    Represents an individual task in a plan
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    
    # Task identification
    task_id = Column(String(50), nullable=False)  # e.g., "T1", "T2"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Duration and scheduling
    duration_days = Column(Integer, nullable=False)
    earliest_start = Column(String(50), nullable=True)  # YYYY-MM-DD
    latest_finish = Column(String(50), nullable=True)   # YYYY-MM-DD
    
    # Dependencies and priority
    depends_on = Column(JSON, nullable=True)  # List of task IDs ["T0", "T1"]
    priority = Column(String(50), default="Medium")  # High, Medium, Low
    confidence = Column(Float, default=1.0)  # 0.0 to 1.0
    
    # Task status
    status = Column(String(50), default="pending")  # pending, in_progress, completed, blocked
    completed_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    plan = relationship("Plan", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, task_id='{self.task_id}', title='{self.title}')>"
