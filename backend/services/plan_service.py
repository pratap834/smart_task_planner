"""
Core business logic for plan generation and management
"""
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime, timedelta
from dateutil import parser
from schemas import Constraints, TaskResponse, LLMPlanResponse


class PlanGenerator:
    """Handles plan generation, scheduling, and critical path calculation"""
    
    @staticmethod
    def calculate_critical_path(tasks: List[TaskResponse]) -> List[str]:
        """
        Calculate the critical path through the task network
        
        The critical path is the longest sequence of dependent tasks
        that determines the minimum project duration.
        
        Args:
            tasks: List of TaskResponse objects
        
        Returns:
            List of task IDs in the critical path
        """
        if not tasks:
            return []
        
        # Build task dictionary for quick lookup
        task_dict = {task.id: task for task in tasks}
        
        # Calculate earliest start and finish times
        earliest_start = {}
        earliest_finish = {}
        
        # Sort tasks topologically (dependencies first)
        sorted_tasks = PlanGenerator._topological_sort(tasks)
        
        for task_id in sorted_tasks:
            task = task_dict[task_id]
            
            # Calculate earliest start time
            if not task.depends_on:
                earliest_start[task_id] = 0
            else:
                # Start after all dependencies finish
                max_finish = max(
                    earliest_finish.get(dep_id, 0)
                    for dep_id in task.depends_on
                    if dep_id in task_dict
                )
                earliest_start[task_id] = max_finish
            
            # Calculate earliest finish time
            earliest_finish[task_id] = earliest_start[task_id] + task.duration_days
        
        # Find the final task (longest finish time)
        if not earliest_finish:
            return []
        
        final_task_id = max(earliest_finish.keys(), key=lambda k: earliest_finish[k])
        
        # Backtrack to find critical path
        critical_path = []
        current_task_id = final_task_id
        
        while current_task_id:
            critical_path.insert(0, current_task_id)
            current_task = task_dict[current_task_id]
            
            # Find the predecessor on the critical path
            if not current_task.depends_on:
                break
            
            # Find dependency with latest finish time
            current_task_id = None
            max_finish_time = -1
            
            for dep_id in current_task.depends_on:
                if dep_id in earliest_finish:
                    if earliest_finish[dep_id] > max_finish_time:
                        max_finish_time = earliest_finish[dep_id]
                        current_task_id = dep_id
        
        return critical_path
    
    @staticmethod
    def _topological_sort(tasks: List[TaskResponse]) -> List[str]:
        """
        Sort tasks in topological order (dependencies before dependents)
        
        Args:
            tasks: List of TaskResponse objects
        
        Returns:
            List of task IDs in topological order
        """
        # Build adjacency list and in-degree count
        task_dict = {task.id: task for task in tasks}
        in_degree = {task.id: 0 for task in tasks}
        adjacency = {task.id: [] for task in tasks}
        
        for task in tasks:
            for dep_id in task.depends_on:
                if dep_id in task_dict:
                    adjacency[dep_id].append(task.id)
                    in_degree[task.id] += 1
        
        # Kahn's algorithm for topological sort
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        sorted_tasks = []
        
        while queue:
            current = queue.pop(0)
            sorted_tasks.append(current)
            
            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return sorted_tasks
    
    @staticmethod
    def assign_dates(
        tasks: List[TaskResponse],
        constraints: Optional[Constraints] = None,
        start_date: Optional[datetime] = None
    ) -> List[TaskResponse]:
        """
        Assign earliest_start and latest_finish dates to tasks
        
        Args:
            tasks: List of TaskResponse objects
            constraints: Optional constraints (weekends, unavailable dates)
            start_date: Project start date (defaults to today)
        
        Returns:
            Updated list of tasks with dates assigned
        """
        if not tasks:
            return tasks
        
        if start_date is None:
            start_date = datetime.now()
        
        # Parse unavailable dates
        unavailable_dates = set()
        if constraints and constraints.unavailable_dates:
            for date_str in constraints.unavailable_dates:
                try:
                    unavailable_dates.add(parser.parse(date_str).date())
                except:
                    pass
        
        # Whether to skip weekends
        skip_weekends = constraints.no_work_on_weekends if constraints else True
        
        # Build task dictionary
        task_dict = {task.id: task for task in tasks}
        
        # Calculate dates for each task
        task_dates = {}
        sorted_tasks = PlanGenerator._topological_sort(tasks)
        
        for task_id in sorted_tasks:
            task = task_dict[task_id]
            
            # Determine earliest start date
            if not task.depends_on:
                earliest_start = start_date
            else:
                # Start after all dependencies finish
                max_finish = start_date
                for dep_id in task.depends_on:
                    if dep_id in task_dates:
                        dep_finish = task_dates[dep_id]['finish']
                        if dep_finish > max_finish:
                            max_finish = dep_finish
                earliest_start = max_finish
            
            # Calculate finish date considering working days
            finish_date = PlanGenerator._add_working_days(
                earliest_start,
                task.duration_days,
                skip_weekends,
                unavailable_dates
            )
            
            task_dates[task_id] = {
                'start': earliest_start,
                'finish': finish_date
            }
            
            # Update task with dates
            task.earliest_start = earliest_start.strftime('%Y-%m-%d')
            task.latest_finish = finish_date.strftime('%Y-%m-%d')
        
        return tasks
    
    @staticmethod
    def _add_working_days(
        start_date: datetime,
        days: int,
        skip_weekends: bool,
        unavailable_dates: Set
    ) -> datetime:
        """
        Add working days to a start date, skipping weekends and unavailable dates
        
        Args:
            start_date: Starting date
            days: Number of working days to add
            skip_weekends: Whether to skip weekends
            unavailable_dates: Set of dates to skip
        
        Returns:
            End date
        """
        current_date = start_date
        days_added = 0
        
        while days_added < days:
            current_date += timedelta(days=1)
            
            # Skip weekends if required
            if skip_weekends and current_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                continue
            
            # Skip unavailable dates
            if current_date.date() in unavailable_dates:
                continue
            
            days_added += 1
        
        return current_date
    
    @staticmethod
    def validate_constraints(
        tasks: List[TaskResponse],
        constraints: Optional[Constraints],
        start_date: Optional[datetime] = None
    ) -> Tuple[bool, List[str]]:
        """
        Validate that the plan meets the specified constraints
        
        Args:
            tasks: List of tasks
            constraints: User constraints
            start_date: Project start date
        
        Returns:
            Tuple of (is_valid, list of warning messages)
        """
        warnings = []
        
        if not constraints:
            return True, warnings
        
        if start_date is None:
            start_date = datetime.now()
        
        # Assign dates to tasks
        tasks_with_dates = PlanGenerator.assign_dates(tasks, constraints, start_date)
        
        # Check deadline constraint
        if constraints.deadline:
            try:
                deadline = parser.parse(constraints.deadline)
                
                # Find latest task finish date
                latest_finish = start_date
                for task in tasks_with_dates:
                    if task.latest_finish:
                        task_finish = parser.parse(task.latest_finish)
                        if task_finish > latest_finish:
                            latest_finish = task_finish
                
                if latest_finish > deadline:
                    days_over = (latest_finish - deadline).days
                    warnings.append(
                        f"Project will finish {days_over} days after deadline. "
                        f"Expected finish: {latest_finish.strftime('%Y-%m-%d')}, "
                        f"Deadline: {constraints.deadline}"
                    )
            except Exception as e:
                warnings.append(f"Invalid deadline format: {constraints.deadline}")
        
        return len(warnings) == 0, warnings


# Singleton instance
plan_generator = PlanGenerator()
