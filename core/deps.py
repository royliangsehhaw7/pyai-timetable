from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import date
from typing import Set
from schemas.schedule import ScheduledClass
from tools.room_availability import RoomConflictDetector, RoomCapacityValidator, RoomSpecialtyChecker

@dataclass
class GlobalUsage:
    """
    Tracks cumulative token usage across all agent interactions in a single run.
    """
    request_tokens: int = 0
    response_tokens: int = 0
    total_tokens: int = 0

    def update(self, usage: Any) -> None:
        """
        Updates the global counters using a Pydantic AI Usage object.
        """
        self.request_tokens += getattr(usage, "request_tokens", 0)
        self.response_tokens += getattr(usage, "response_tokens", 0)
        self.total_tokens += getattr(usage, "total_tokens", 0)

    def __str__(self) -> str:
        return (f"Usage(Total: {self.total_tokens}, "
                f"Req: {self.request_tokens}, Res: {self.response_tokens})")

@dataclass
class BaseDeps:
    """Common dependencies shared by all agents."""
    usage: GlobalUsage

@dataclass
class OrchestratorDeps(BaseDeps):
    """Dependencies for the Supervisor agent."""
    # The Orchestrator manages the building of this list
    current_timetable: List[ScheduledClass] = field(default_factory=list)

@dataclass
class PolicyDeps(BaseDeps):
    """Dependencies for the School Policy Agent."""
    policy: Dict[str, Any]

@dataclass
class DeanDeps(BaseDeps):
    """Dependencies for the Academic Dean Agent."""
    courses: List[Dict[str, Any]]
    # Needs current state to calculate remaining hours per course
    current_timetable: List[ScheduledClass] = field(default_factory=list)

@dataclass
class RegistrarDeps(BaseDeps):
    """Dependencies for the Registrar Agent."""
    rooms: List[Dict[str, Any]]
    room_bookings: Dict[str, Dict[date, Set[str]]]
    room_capacities: Dict[str, int]
    room_equipment: Dict[str, List[str]]
    # Needs current state to check room double-booking
    current_timetable: List[ScheduledClass] = field(default_factory=list)

    @property
    def room_availability(self) -> RoomConflictDetector:
        return RoomConflictDetector(self.room_bookings)

    @property
    def room_capacity_validator(self) -> RoomCapacityValidator:
        return RoomCapacityValidator(self.room_capacities)

    @property
    def room_specialty_checker(self) -> RoomSpecialtyChecker:
        return RoomSpecialtyChecker(self.room_equipment)

@dataclass
class FacultyDeps(BaseDeps):
    """Dependencies for the Faculty Head Agent."""
    lecturers: List[Dict[str, Any]]
    # Needs current state to check lecturer double-booking
    current_timetable: List[ScheduledClass] = field(default_factory=list)
