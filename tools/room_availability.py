from typing import Dict, Set, List, Optional
from datetime import date, time
from dataclasses import dataclass
from schemas.schedule import ScheduledClass

"""
    Structured as a class (rather than standalone functions) to:
    1. Maintain booking state across multiple validations
    2. Comply with Pydantic AI's tool injection pattern
    3. Enable clean dependency injection via RegistrarDeps

    The @dataclass decorator auto-generates __init__() while allowing us to
    add custom validation methods that operate on the instance data.
"""


@dataclass
class RoomConflictDetector:
    """Tracks and validates room bookings to prevent double-booking."""
    bookings: Dict[str, Dict[date, Set[str]]]  # {room_id: {date: {timeslots}}}

    def is_available(self, room_id: str, day: date, start_time: time, end_time: time) -> bool:
        """Check if a room is available for a given timeslot."""
        if room_id not in self.bookings or day not in self.bookings[room_id]:
            return True
            
        timeslot = f"{start_time}-{end_time}"
        return timeslot not in self.bookings[room_id][day]

    def reserve(self, room_id: str, day: date, start_time: time, end_time: time) -> None:
        """Reserve a room for a specific timeslot."""
        if room_id not in self.bookings:
            self.bookings[room_id] = {}
        if day not in self.bookings[room_id]:
            self.bookings[room_id][day] = set()
            
        timeslot = f"{start_time}-{end_time}"
        self.bookings[room_id][day].add(timeslot)

@dataclass
class RoomCapacityValidator:
    """Validates that rooms can accommodate the expected student count."""
    capacities: Dict[str, int]  # {room_id: max_capacity}

    def validate(self, room_id: str, expected_attendance: int) -> bool:
        """Check if room can accommodate the expected students."""
        if room_id not in self.capacities:
            return False
        return expected_attendance <= self.capacities[room_id]

@dataclass
class RoomSpecialtyChecker:
    """Validates that rooms have required equipment for specific courses."""
    equipment: Dict[str, List[str]]  # {room_id: [equipment_list]}

    def has_required_equipment(self, room_id: str, required_equipment: List[str]) -> bool:
        """Check if room has all required equipment."""
        if room_id not in self.equipment:
            return False
        return all(item in self.equipment[room_id] for item in required_equipment)
