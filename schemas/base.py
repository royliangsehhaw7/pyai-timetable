"""
Base models and shared enums for the Enterprise Adaptive Scheduler.

This module defines foundational Pydantic models and enumerations that are used
across all other schema modules. These provide consistent typing and validation
for core domain concepts.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import time
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Shared Enumerations
# ============================================================================

class DayOfWeek(str, Enum):
    """Enumeration for days of the operational week."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class TimeSlot(str, Enum):
    """Standard time slots within operational hours."""
    SLOT_0800_0900 = "08:00-09:00"
    SLOT_0900_1000 = "09:00-10:00"
    SLOT_1000_1100 = "10:00-11:00"
    SLOT_1100_1200 = "11:00-12:00"
    SLOT_1200_1300 = "12:00-13:00"
    SLOT_1300_1400 = "13:00-14:00"
    SLOT_1400_1500 = "14:00-15:00"
    SLOT_1500_1600 = "15:00-16:00"
    SLOT_1600_1700 = "16:00-17:00"


class CourseType(str, Enum):
    """Types of courses based on pedagogical requirements."""
    LECTURE = "lecture"
    LABORATORY = "laboratory"
    SEMINAR = "seminar"
    TUTORIAL = "tutorial"
    WORKSHOP = "workshop"


class RoomType(str, Enum):
    """Types of rooms based on physical characteristics."""
    GENERAL = "general"
    LAB = "lab"
    SEMINAR_ROOM = "seminar_room"
    LECTURE_HALL = "lecture_hall"
    SPECIALIZED = "specialized"


class ValidationStatus(str, Enum):
    """Status of validation operations."""
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"


# ============================================================================
# Base Models
# ============================================================================

class TemporalCoordinate(BaseModel):
    """
    Represents a specific (Day, Time) coordinate in the scheduling grid.
    
    This is the fundamental unit of temporal positioning in the scheduler.
    """
    day: DayOfWeek = Field(..., description="Day of the week")
    time_slot: TimeSlot = Field(..., description="Standard time slot")
    
    model_config = ConfigDict(
        frozen=True,  # Immutable to ensure consistency
        json_schema_extra={
            "example": {
                "day": "monday",
                "time_slot": "09:00-10:00"
            }
        }
    )


class SpatialCoordinate(BaseModel):
    """
    Represents a physical location (room) in the scheduling grid.
    """
    room_id: str = Field(..., min_length=1, description="Unique room identifier")
    building: Optional[str] = Field(None, description="Building name or code")
    floor: Optional[int] = Field(None, ge=0, description="Floor number")
    
    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "room_id": "CS-101",
                "building": "Computer Science",
                "floor": 1
            }
        }
    )


class ScheduleCoordinate(BaseModel):
    """
    Complete coordinate combining temporal and spatial dimensions.
    
    Represents a unique (Time, Space) coordinate in the scheduling grid.
    """
    temporal: TemporalCoordinate = Field(..., description="Temporal dimension")
    spatial: SpatialCoordinate = Field(..., description="Spatial dimension")
    
    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "temporal": {
                    "day": "monday",
                    "time_slot": "09:00-10:00"
                },
                "spatial": {
                    "room_id": "CS-101",
                    "building": "Computer Science",
                    "floor": 1
                }
            }
        }
    )


class BaseEntity(BaseModel):
    """
    Base class for all domain entities with common metadata.
    """
    id: str = Field(..., min_length=1, description="Unique identifier")
    name: str = Field(..., min_length=1, description="Human-readable name")
    description: Optional[str] = Field(None, description="Detailed description")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional flexible metadata"
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "course-101",
                "name": "Introduction to Algorithms",
                "description": "Fundamental algorithms course",
                "metadata": {"department": "Computer Science"}
            }
        }
    )


class ErrorDetail(BaseModel):
    """
    Structured error information for validation failures and rejections.
    """
    code: str = Field(..., description="Error code for programmatic handling")
    message: str = Field(..., description="Human-readable error message")
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context about the error"
    )
    
    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "code": "ROOM_CAPACITY_EXCEEDED",
                "message": "Room capacity insufficient for course size",
                "context": {"room_capacity": 30, "course_size": 45}
            }
        }
    )


# ============================================================================
# Utility Functions
# ============================================================================

def time_slot_to_time_range(time_slot: TimeSlot) -> tuple[time, time]:
    """
    Convert a TimeSlot enum to start and end time objects.
    
    Args:
        time_slot: The TimeSlot enum value
        
    Returns:
        Tuple of (start_time, end_time) as datetime.time objects
    """
    # Parse the time slot string (e.g., "08:00-09:00")
    start_str, end_str = time_slot.value.split("-")
    
    # Convert to time objects
    start_time = time.fromisoformat(start_str)
    end_time = time.fromisoformat(end_str)
    
    return start_time, end_time


def is_weekday(day: DayOfWeek) -> bool:
    """
    Check if a day is within the standard Monday-Friday operational week.
    
    Args:
        day: The day to check
        
    Returns:
        True if the day is Monday through Friday
    """
    weekdays = {
        DayOfWeek.MONDAY,
        DayOfWeek.TUESDAY,
        DayOfWeek.WEDNESDAY,
        DayOfWeek.THURSDAY,
        DayOfWeek.FRIDAY
    }
    return day in weekdays
