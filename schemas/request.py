from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ScheduleRequest(BaseModel):
    """
    Input model for requesting a new weekly timetable generation.

    Usage:
    - Entry Point: The primary input to the SchedulingService to initiate a run.
    - Configuration: Defines constraints like max iterations and course priorities.
    """
    semester_id: str = Field(description="The identifier for the semester (e.g., 'Spring 2026')")
    priority_courses: Optional[List[str]] = Field(
        None, 
        description="Optional list of course IDs that should be prioritized in scheduling"
    )
    max_iterations: int = Field(
        50, 
        description="Maximum number of negotiation iterations for the orchestration loop"
    )
    notes: Optional[str] = Field(None, description="Any additional instructions for the scheduler")
    constraints: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional scheduling constraints"
    )
