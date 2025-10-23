"""
Basic tests for Smart Task Planner API
Run with: pytest test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llm_provider" in data


def test_create_plan_basic():
    """Test creating a basic plan without constraints"""
    request_data = {
        "goal_text": "Build a simple REST API for task management",
        "plan_type": "MODERATE"
    }
    
    response = client.post("/api/plans", json=request_data)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert "tasks" in data
    assert len(data["tasks"]) >= 3  # Should have at least 3 tasks
    assert "critical_path" in data
    assert "plan_summary" in data


def test_create_plan_with_constraints():
    """Test creating a plan with constraints"""
    request_data = {
        "goal_text": "Launch a mobile app in 2 weeks",
        "plan_type": "MODERATE",
        "constraints": {
            "deadline": "2025-11-07T23:59:59",
            "max_hours_per_day": 8,
            "no_work_on_weekends": True
        }
    }
    
    response = client.post("/api/plans", json=request_data)
    assert response.status_code == 201
    
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 5
    
    # Check task structure
    first_task = data["tasks"][0]
    assert "task_id" in first_task
    assert "title" in first_task
    assert "description" in first_task
    assert "duration_days" in first_task
    assert "depends_on" in first_task
    assert "priority" in first_task
    assert "earliest_start" in first_task
    assert "latest_finish" in first_task


def test_create_plan_validation():
    """Test validation - goal text too short"""
    request_data = {
        "goal_text": "Test",  # Too short (min 10 chars)
        "plan_type": "MODERATE"
    }
    
    response = client.post("/api/plans", json=request_data)
    assert response.status_code == 422  # Validation error


def test_list_plans():
    """Test listing all plans"""
    # First create a plan
    request_data = {
        "goal_text": "Build a simple web application",
        "plan_type": "MODERATE"
    }
    client.post("/api/plans", json=request_data)
    
    # Then list plans
    response = client.get("/api/plans")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_plan_by_id():
    """Test retrieving a specific plan"""
    # Create a plan first
    request_data = {
        "goal_text": "Develop a machine learning model",
        "plan_type": "MODERATE"
    }
    create_response = client.post("/api/plans", json=request_data)
    plan_id = create_response.json()["id"]
    
    # Get the plan
    response = client.get(f"/api/plans/{plan_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == plan_id
    assert "tasks" in data
    assert "goal_id" in data


def test_get_nonexistent_plan():
    """Test getting a plan that doesn't exist"""
    response = client.get("/api/plans/nonexistent_id_12345")
    assert response.status_code == 404


def test_task_dependencies():
    """Test that task dependencies are properly structured"""
    request_data = {
        "goal_text": "Build a full-stack e-commerce website",
        "plan_type": "MODERATE"
    }
    
    response = client.post("/api/plans", json=request_data)
    data = response.json()
    
    tasks = data["tasks"]
    task_ids = {task["task_id"] for task in tasks}
    
    # Verify all dependency references are valid
    for task in tasks:
        for dep_id in task["depends_on"]:
            assert dep_id in task_ids, f"Invalid dependency: {dep_id}"
    
    # First task should have no dependencies
    first_task = next(t for t in tasks if t["task_id"] == "T1")
    assert len(first_task["depends_on"]) == 0


def test_critical_path_exists():
    """Test that critical path is calculated"""
    request_data = {
        "goal_text": "Launch a SaaS product in 30 days",
        "plan_type": "MODERATE"
    }
    
    response = client.post("/api/plans", json=request_data)
    data = response.json()
    
    assert "critical_path" in data
    assert isinstance(data["critical_path"], list)
    assert len(data["critical_path"]) > 0
    
    # Critical path should contain valid task IDs
    task_ids = {task["task_id"] for task in data["tasks"]}
    for cp_task_id in data["critical_path"]:
        assert cp_task_id in task_ids


def test_plan_types():
    """Test different plan types"""
    goal = "Build a mobile app for expense tracking"
    
    for plan_type in ["AGGRESSIVE", "MODERATE", "CONSERVATIVE"]:
        request_data = {
            "goal_text": goal,
            "plan_type": plan_type
        }
        
        response = client.post("/api/plans", json=request_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["plan_type"] == plan_type


def test_task_priorities():
    """Test that tasks have valid priorities"""
    request_data = {
        "goal_text": "Create a data pipeline for analytics",
        "plan_type": "MODERATE"
    }
    
    response = client.post("/api/plans", json=request_data)
    data = response.json()
    
    valid_priorities = ["HIGH", "MEDIUM", "LOW"]
    for task in data["tasks"]:
        assert task["priority"] in valid_priorities


def test_timeline_calculation():
    """Test that timelines are properly calculated"""
    request_data = {
        "goal_text": "Develop a REST API with authentication",
        "plan_type": "MODERATE",
        "constraints": {
            "max_hours_per_day": 8,
            "no_work_on_weekends": True
        }
    }
    
    response = client.post("/api/plans", json=request_data)
    data = response.json()
    
    # Check that dates are assigned
    for task in data["tasks"]:
        assert task["earliest_start"] is not None
        assert task["latest_finish"] is not None
        
        # Verify date format (should be ISO format)
        assert "T" in task["earliest_start"]
        assert "T" in task["latest_finish"]
    
    # Check total duration
    assert "total_duration_days" in data
    assert data["total_duration_days"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
