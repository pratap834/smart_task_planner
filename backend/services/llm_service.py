"""
LLM service for task generation using Google Gemini API
"""
import json
from typing import Optional
import google.generativeai as genai
from config import settings
from schemas import LLMPlanResponse, LLMTaskResponse, Constraints


class LLMService:
    """Service for interacting with Google Gemini to generate task plans"""
    
    def __init__(self):
        """Initialize Gemini client"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.client = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.model = settings.GEMINI_MODEL
    
    def generate_plan(
        self,
        goal_text: str,
        constraints: Optional[Constraints] = None,
        plan_type: str = "moderate"
    ) -> LLMPlanResponse:
        """
        Generate a task plan using Google Gemini
        
        Args:
            goal_text: The user's goal description
            constraints: Optional constraints (deadline, work hours, etc.)
            plan_type: Type of plan (moderate, aggressive, conservative)
        
        Returns:
            LLMPlanResponse with tasks and plan summary
        """
        # Build the prompt
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_prompt(goal_text, constraints, plan_type)
        
        try:
            return self._generate_with_gemini(system_prompt, user_prompt)
        except Exception as e:
            print(f"Error generating plan with Gemini: {e}")
            # Return a fallback plan
            return self._generate_fallback_plan(goal_text)
    
    def _generate_with_gemini(self, system_prompt: str, user_prompt: str) -> LLMPlanResponse:
        """Generate plan using Google Gemini API"""
        # Combine system and user prompts for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nIMPORTANT: Respond with valid JSON only, no markdown formatting."
        
        # Configure generation parameters
        generation_config = genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=4096,
        )
        
        # Generate response
        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        # Extract and clean the response text
        content = response.text.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        elif content.startswith("```"):
            content = content[3:]  # Remove ```
        if content.endswith("```"):
            content = content[:-3]  # Remove trailing ```
        
        content = content.strip()
        
        # Parse JSON
        plan_data = json.loads(content)
        return LLMPlanResponse(**plan_data)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the LLM"""
        return """You are an expert project planner and task breakdown specialist. Your role is to:

1. Analyze user goals and break them down into actionable tasks
2. Estimate realistic task durations (1-3 days per task)
3. Identify task dependencies and create a logical sequence
4. Respect user constraints (deadlines, work hours, unavailable dates)
5. Identify critical path tasks and high-risk areas
6. Provide clear, detailed task descriptions

Always respond with valid JSON in this exact format:
{
  "tasks": [
    {
      "id": "T1",
      "title": "Short task title",
      "description": "Detailed description of what needs to be done",
      "duration_days": 2,
      "depends_on": [],
      "priority": "High",
      "confidence": 0.9
    }
  ],
  "plan_summary": "Overview of the plan, task sequence, critical path, and timeline."
}

Guidelines:
- Task IDs must be sequential: T1, T2, T3, etc.
- Duration should be 1-3 days for most tasks
- Priority must be: High, Medium, or Low
- Confidence must be 0.0 to 1.0 (lower for uncertain tasks)
- depends_on should list prerequisite task IDs
- First task (T1) should have no dependencies
- Break complex goals into 5-15 tasks
- Identify critical path tasks (longest dependency chain)
"""
    
    def _build_prompt(
        self,
        goal_text: str,
        constraints: Optional[Constraints],
        plan_type: str
    ) -> str:
        """Build the user prompt with goal and constraints"""
        
        prompt_parts = [f"Goal: {goal_text}\n"]
        
        # Add plan type context
        if plan_type == "aggressive":
            prompt_parts.append("\nPlan Type: AGGRESSIVE - Minimize timeline, accept higher risk, parallel tasks where possible.\n")
        elif plan_type == "conservative":
            prompt_parts.append("\nPlan Type: CONSERVATIVE - Allow extra buffer time, minimize risks, sequential approach.\n")
        else:
            prompt_parts.append("\nPlan Type: MODERATE - Balance speed and safety, some parallel tasks.\n")
        
        # Add constraints if provided
        if constraints:
            prompt_parts.append("\nConstraints:")
            
            if constraints.deadline:
                prompt_parts.append(f"- Deadline: {constraints.deadline}")
            
            if constraints.max_hours_per_day:
                prompt_parts.append(f"- Max work hours per day: {constraints.max_hours_per_day}")
            
            if constraints.no_work_on_weekends:
                prompt_parts.append("- No work on weekends")
            
            if constraints.unavailable_dates:
                dates_str = ", ".join(constraints.unavailable_dates)
                prompt_parts.append(f"- Unavailable dates: {dates_str}")
        
        prompt_parts.append("\n\nGenerate a detailed task breakdown with dependencies, durations, and priorities.")
        
        return "\n".join(prompt_parts)
    
    def _generate_fallback_plan(self, goal_text: str) -> LLMPlanResponse:
        """Generate a simple fallback plan if LLM fails"""
        return LLMPlanResponse(
            tasks=[
                LLMTaskResponse(
                    id="T1",
                    title="Research and Planning",
                    description=f"Research and plan approach for: {goal_text}",
                    duration_days=1,
                    depends_on=[],
                    priority="High",
                    confidence=0.8
                ),
                LLMTaskResponse(
                    id="T2",
                    title="Implementation Phase 1",
                    description="Begin implementation of core components",
                    duration_days=2,
                    depends_on=["T1"],
                    priority="High",
                    confidence=0.7
                ),
                LLMTaskResponse(
                    id="T3",
                    title="Testing and Refinement",
                    description="Test implementation and refine based on results",
                    duration_days=1,
                    depends_on=["T2"],
                    priority="Medium",
                    confidence=0.8
                )
            ],
            plan_summary="Basic 3-phase plan: Research → Implementation → Testing. This is a fallback plan generated when the AI service is unavailable."
        )


# Singleton instance
llm_service = LLMService()
