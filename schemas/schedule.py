from datetime import datetime, time
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class SessionType(str, Enum):
    LECTURE = "Lecture"
    LAB = "Lab"
    TUTORIAL = "Tutorial"

class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"

class ScheduledClass(BaseModel):
    """
    A single scheduled session within the timetable.
    
    Usage:
    - Propose: Created by the Orchestrator when suggesting a slot.
    - Validate: Passed to worker agents (Registrar, Faculty Head, etc.) for conflict checking.
    - Finalize: The building block of the final WeeklyTimetable.
    """
    course_id: str = Field(description="The ID of the course (e.g., 'CS101')")
    session_type: SessionType = Field(description="The type of session (Lecture, Lab, or Tutorial)")
    day: DayOfWeek = Field(description="The day of the week for the session")
    start_time: time = Field(description="The start time of the session (HH:MM)")
    duration_hours: float = Field(description="Duration of the session in hours")
    room_id: str = Field(description="The ID of the assigned room")
    lecturer_id: str = Field(description="The ID of the assigned lecturer")

class WeeklyTimetable(BaseModel):
    """
    The complete weekly timetable for the school.
    
    Usage:
    - Output: The final 'output_type' for the Orchestrator agent.
    - Integration: Passed to the Google Calendar MCP for post-generation export.
    """
    timetable: List[ScheduledClass] = Field(default_factory=list, description="List of all scheduled sessions")
    generated_at: datetime = Field(default_factory=datetime.now, description="Timestamp of when the timetable was generated")
    total_sessions: int = Field(0, description="Total number of sessions scheduled")
    status: str = Field("Draft", description="Current status of the timetable (e.g., 'Draft', 'Finalized')")

class ValidationResult(BaseModel):
    """
    The structured result of a validation check by a specialist agent.
    
    Usage:
    - Result: The standard 'output_type' for all worker agents (Policy, Dean, Registrar, Faculty).
    - Feedback: If 'approved' is False, the 'reason' is used by the Orchestrator to re-propose.
    """
    approved: bool = Field(description="Whether the proposed slot is valid according to the agent's criteria")
    reason: Optional[str] = Field(None, description="Detailed reason for rejection if approved is False")
