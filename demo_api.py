"""
Demo script to test the Smart Task Planner API
Run this after starting the backend server
"""
import requests
import json
from datetime import datetime, timedelta

# API Configuration
API_BASE_URL = "http://localhost:8000/api"


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))


def test_health_check():
    """Test the health check endpoint"""
    print_header("Testing Health Check")
    
    response = requests.get(f"{API_BASE_URL.replace('/api', '')}/health")
    print(f"Status Code: {response.status_code}")
    print_json(response.json())


def test_create_plan(goal_text, constraints=None, plan_type="moderate"):
    """Test creating a new plan"""
    print_header(f"Creating Plan: {goal_text[:50]}...")
    
    payload = {
        "goal_text": goal_text,
        "plan_type": plan_type,
        "constraints": constraints or {
            "max_hours_per_day": 8,
            "no_work_on_weekends": True,
            "unavailable_dates": []
        }
    }
    
    print("Request Payload:")
    print_json(payload)
    print("\nSending request...")
    
    response = requests.post(f"{API_BASE_URL}/plans", json=payload)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 201:
        plan = response.json()
        print("\n✓ Plan created successfully!")
        print(f"\nPlan ID: {plan['id']}")
        print(f"Plan Type: {plan['plan_type']}")
        print(f"Number of Tasks: {len(plan['tasks'])}")
        print(f"\nPlan Summary:\n{plan['plan_summary']}")
        
        if plan['critical_path']:
            print(f"\nCritical Path: {' → '.join(plan['critical_path'])}")
        
        print("\nTasks:")
        for task in plan['tasks']:
            print(f"\n  [{task['id']}] {task['title']}")
            print(f"      Duration: {task['duration_days']} days")
            print(f"      Priority: {task['priority']}")
            if task['depends_on']:
                print(f"      Depends on: {', '.join(task['depends_on'])}")
            if task['earliest_start']:
                print(f"      Start: {task['earliest_start']}")
            if task['latest_finish']:
                print(f"      Finish: {task['latest_finish']}")
        
        return plan
    else:
        print("\n✗ Failed to create plan")
        print_json(response.json())
        return None


def test_get_plan(plan_id):
    """Test retrieving a specific plan"""
    print_header(f"Retrieving Plan {plan_id}")
    
    response = requests.get(f"{API_BASE_URL}/plans/{plan_id}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        plan = response.json()
        print("\n✓ Plan retrieved successfully!")
        print(f"Number of tasks: {len(plan['tasks'])}")
        return plan
    else:
        print("\n✗ Failed to retrieve plan")
        print_json(response.json())
        return None


def test_list_plans():
    """Test listing all plans"""
    print_header("Listing All Plans")
    
    response = requests.get(f"{API_BASE_URL}/plans")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        plans = response.json()
        print(f"\n✓ Found {len(plans)} plan(s)")
        
        for i, plan in enumerate(plans, 1):
            print(f"\n{i}. Plan ID: {plan['id']}")
            print(f"   Type: {plan['plan_type']}")
            print(f"   Tasks: {len(plan['tasks'])}")
            print(f"   Status: {plan['status']}")
        
        return plans
    else:
        print("\n✗ Failed to list plans")
        print_json(response.json())
        return []


def test_update_task(plan_id, task_id, status):
    """Test updating a task status"""
    print_header(f"Updating Task {task_id} in Plan {plan_id}")
    
    payload = {"status": status}
    response = requests.patch(
        f"{API_BASE_URL}/plans/{plan_id}/tasks/{task_id}",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        task = response.json()
        print(f"\n✓ Task updated successfully!")
        print(f"Task: {task['title']}")
        print(f"New Status: {task['status']}")
        return task
    else:
        print("\n✗ Failed to update task")
        print_json(response.json())
        return None


# ============================================================================
# Sample Goals for Testing
# ============================================================================

SAMPLE_GOALS = [
    {
        "goal": "Build a full-stack e-commerce website with user authentication, product catalog, shopping cart, and payment integration",
        "type": "moderate",
        "constraints": {
            "deadline": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "max_hours_per_day": 8,
            "no_work_on_weekends": True,
            "unavailable_dates": []
        }
    },
    {
        "goal": "Learn Python and build a machine learning project to predict house prices",
        "type": "conservative",
        "constraints": {
            "max_hours_per_day": 4,
            "no_work_on_weekends": True,
            "unavailable_dates": []
        }
    },
    {
        "goal": "Write and publish a technical blog with 10 articles about software architecture",
        "type": "aggressive",
        "constraints": {
            "deadline": (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"),
            "max_hours_per_day": 6,
            "no_work_on_weekends": False,
            "unavailable_dates": []
        }
    },
    {
        "goal": "Migrate legacy monolithic application to microservices architecture with Docker and Kubernetes",
        "type": "moderate",
        "constraints": {
            "max_hours_per_day": 8,
            "no_work_on_weekends": True,
            "unavailable_dates": []
        }
    }
]


def run_full_demo():
    """Run a complete demo of all functionality"""
    print("\n" + "=" * 80)
    print("  🎯 SMART TASK PLANNER - DEMO SCRIPT")
    print("=" * 80)
    
    try:
        # Test health check
        test_health_check()
        
        # Create a plan with the first sample goal
        sample = SAMPLE_GOALS[0]
        plan = test_create_plan(
            sample["goal"],
            sample["constraints"],
            sample["type"]
        )
        
        if plan:
            plan_id = plan["id"]
            
            # Test retrieving the plan
            test_get_plan(plan_id)
            
            # Test updating a task
            if plan["tasks"]:
                first_task = plan["tasks"][0]
                test_update_task(plan_id, first_task["id"], "in_progress")
                test_update_task(plan_id, first_task["id"], "completed")
            
            # List all plans
            test_list_plans()
        
        print_header("Demo Completed Successfully! ✓")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to API server")
        print("Make sure the backend server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


def interactive_demo():
    """Interactive demo allowing user to select actions"""
    print("\n" + "=" * 80)
    print("  🎯 SMART TASK PLANNER - INTERACTIVE DEMO")
    print("=" * 80)
    
    while True:
        print("\nOptions:")
        print("1. Create plan with sample goal")
        print("2. List all plans")
        print("3. Run full automated demo")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\nSample Goals:")
            for i, sample in enumerate(SAMPLE_GOALS, 1):
                print(f"{i}. {sample['goal'][:70]}...")
            
            goal_choice = input(f"\nSelect goal (1-{len(SAMPLE_GOALS)}): ").strip()
            try:
                sample = SAMPLE_GOALS[int(goal_choice) - 1]
                test_create_plan(sample["goal"], sample["constraints"], sample["type"])
            except (ValueError, IndexError):
                print("Invalid choice")
        
        elif choice == "2":
            test_list_plans()
        
        elif choice == "3":
            run_full_demo()
        
        elif choice == "4":
            print("\nGoodbye! 👋")
            break
        
        else:
            print("Invalid choice")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_full_demo()
    else:
        interactive_demo()
