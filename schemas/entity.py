"""
Entity models for workload items in the Enterprise Adaptive Scheduler.

This module defines the `EntityModel` – the base workload item that courses,
lecturers, and other scheduling entities extend from. It captures the
essential requirements and constraints that must be satisfied during scheduling.
"""

from typing import Optional, List, Dict, Any
from datetime import timedelta
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .base import BaseEntity, CourseType, DayOfWeek, TimeSlot


class EntityModel(BaseEntity):
    """
    Base model for all workload items that require scheduling.

    This model represents the core requirements of any entity that needs to be
    placed in the schedule (courses, tasks, etc.). It defines the temporal
    quotas, constraints, and metadata that must be respected.

    Attributes:
        required_slots: Number of time slots this entity must occupy.
        max_daily_slots: Maximum number of slots allowed per day (pedagogical cap).
        preferred_days: Optional list of days where scheduling is preferred.
        excluded_days: Optional list of days where scheduling is prohibited.
        preferred_times: Optional list of time slots that are preferred.
        excluded_times: Optional list of time slots that are prohibited.
        duration_per_slot: Duration of each time slot (defaults to 1 hour).
        course_type: Type of course (if applicable).
        dependencies: List of entity IDs that must be scheduled before this one.
        constraints: Additional domain-specific constraints as key-value pairs.
    """

    # Temporal quotas
    required_slots: int = Field(
        ...,
        gt=0,
        description="Number of time slots this entity must occupy in the schedule"
    )
    max_daily_slots: int = Field(
        default=2,
        gt=0,
        le=4,
        description="Maximum number of slots allowed per day (pedagogical cap)"
    )

    # Day preferences and exclusions
    preferred_days: Optional[List[DayOfWeek]] = Field(
        default=None,
        description="Days where scheduling is preferred (soft constraint)"
    )
    excluded_days: Optional[List[DayOfWeek]] = Field(
        default=None,
        description="Days where scheduling is prohibited (hard constraint)"
    )

    # Time slot preferences and exclusions
    preferred_times: Optional[List[TimeSlot]] = Field(
        default=None,
        description="Time slots that are preferred (soft constraint)"
    )
    excluded_times: Optional[List[TimeSlot]] = Field(
        default=None,
        description="Time slots that are prohibited (hard constraint)"
    )

    # Duration and type
    duration_per_slot: timedelta = Field(
        default=timedelta(hours=1),
        description="Duration of each allocated time slot"
    )
    course_type: Optional[CourseType] = Field(
        default=None,
        description="Type of course (if this entity is a course)"
    )

    # Dependencies and constraints
    dependencies: List[str] = Field(
        default_factory=list,
        description="IDs of entities that must be scheduled before this one"
    )
    constraints: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional domain-specific constraints"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "CS-101",
                "name": "Introduction to Algorithms",
                "description": "Fundamental algorithms course",
                "metadata": {"department": "Computer Science"},
                "required_slots": 3,
                "max_daily_slots": 2,
                "preferred_days": ["monday", "wednesday", "friday"],
                "excluded_days": ["saturday", "sunday"],
                "preferred_times": ["09:00-10:00", "10:00-11:00"],
                "excluded_times": ["12:00-13:00"],  # Lunch hour
                "duration_per_slot": "01:00:00",
                "course_type": "lecture",
                "dependencies": ["CS-100"],
                "constraints": {"requires_lab_equipment": False}
            }
        }
    )

    @field_validator("preferred_days", "excluded_days", mode="before")
    @classmethod
    def validate_day_list(cls, v):
        """Ensure day lists are unique and valid."""
        if v is None:
            return v
        if not isinstance(v, list):
            raise TypeError("Must be a list")
        # Remove duplicates while preserving order
        seen = set()
        unique_list = []
        for item in v:
            if item not in seen:
                seen.add(item)
                unique_list.append(item)
        return unique_list

    @field_validator("preferred_times", "excluded_times", mode="before")
    @classmethod
    def validate_time_list(cls, v):
        """Ensure time slot lists are unique and valid."""
        if v is None:
            return v
        if not isinstance(v, list):
            raise TypeError("Must be a list")
        seen = set()
        unique_list = []
        for item in v:
            if item not in seen:
                seen.add(item)
                unique_list.append(item)
        return unique_list

    @field_validator("duration_per_slot", mode="before")
    @classmethod
    def validate_duration(cls, v):
        """Convert string duration to timedelta if needed."""
        if isinstance(v, str):
            # Parse ISO 8601 duration string (e.g., "PT1H" or "01:00:00")
            if v.startswith("PT"):
                # ISO format: PT1H30M
                import isodate
                return isodate.parse_duration(v)
            else:
                # Assume HH:MM:SS format
                parts = list(map(int, v.split(":")))
                if len(parts) == 3:
                    hours, minutes, seconds = parts
                    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
                elif len(parts) == 2:
                    hours, minutes = parts
                    return timedelta(hours=hours, minutes=minutes)
                else:
                    raise ValueError("Duration must be in HH:MM:SS or HH:MM format")
        return v

    @field_validator("max_daily_slots")
    @classmethod
    def validate_max_daily_slots(cls, v, info):
        """Ensure max_daily_slots is reasonable relative to required_slots."""
        if "required_slots" in info.data:
            required = info.data["required_slots"]
            if v > required * 2:
                raise ValueError(
                    f"max_daily_slots ({v}) cannot exceed twice required_slots ({required})"
                )
        return v
