// API Request Types
export interface GoalCreateRequest {
  goal_text: string;
  deadline?: string;
  max_hours_per_day?: number;
  no_work_on_weekends?: boolean;
  unavailable_dates?: string[];
  plan_type?: 'aggressive' | 'moderate' | 'conservative';
}

export interface TaskUpdateRequest {
  is_completed?: boolean;
  status?: 'pending' | 'in_progress' | 'completed' | 'blocked';
}

// API Response Types
export interface Task {
  id: number;
  plan_id: number;
  task_id: string;
  title: string;
  description: string;
  duration_days: number;
  earliest_start: string;
  latest_finish: string;
  depends_on: string[];
  priority: 'High' | 'Medium' | 'Low';
  confidence: number;
  status: 'pending' | 'in_progress' | 'completed' | 'blocked';
  is_completed: boolean;
  completed_at?: string;
  is_critical?: boolean;
}

export interface Plan {
  id: number;
  goal_id: number;
  plan_type: string;
  critical_path: string[];
  plan_summary: string;
  total_duration_days?: number;
  estimated_completion?: string;
  created_at: string;
  tasks: Task[];
}

export interface Goal {
  id: number;
  goal_text: string;
  constraints?: {
    deadline?: string;
    max_hours_per_day?: number;
    no_work_on_weekends?: boolean;
    unavailable_dates?: string[];
  };
  created_at: string;
  plans?: Plan[];
}

export interface PlanGenerateResponse {
  goal_id: number;
  plan_id: number;
  tasks: Task[];
  critical_path: string[];
  plan_summary: string;
  total_duration_days: number;
  estimated_completion: string;
}

export interface HealthCheck {
  status: string;
  database: string;
  llm_configured: boolean;
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// Error Response
export interface APIError {
  detail: string;
  status_code?: number;
}
