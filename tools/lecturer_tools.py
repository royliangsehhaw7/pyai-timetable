from dataclasses import dataclass
from typing import Dict, Set, Tuple, List


@dataclass
class LecturerAvailabilityChecker:
    """Tracks lecturer bookings and respects weekly unavailable days."""
    bookings: Dict[str, Dict[int, Set[Tuple[int, int]]]]  # {lecturer_id: {day_of_week: {(start, end)}}}
    unavailable_days: Dict[str, Set[int]]                  # {lecturer_id: {day_of_week}}

    def is_available(self, lecturer_id: str, day_of_week: int, start_hour: int, end_hour: int) -> bool:
        # Check unavailable days
        if lecturer_id in self.unavailable_days and day_of_week in self.unavailable_days[lecturer_id]:
            return False
            
        # Check existing bookings
        if lecturer_id not in self.bookings or day_of_week not in self.bookings[lecturer_id]:
            return True
            
        return (start_hour, end_hour) not in self.bookings[lecturer_id][day_of_week]

    def reserve(self, lecturer_id: str, day_of_week: int, start_hour: int, end_hour: int) -> None:
        if lecturer_id not in self.bookings:
            self.bookings[lecturer_id] = {}
        if day_of_week not in self.bookings[lecturer_id]:
            self.bookings[lecturer_id][day_of_week] = set()
        self.bookings[lecturer_id][day_of_week].add((start_hour, end_hour))


@dataclass
class LecturerSpecialtyValidator:
    """Validates that lecturers can teach assigned courses."""
    specialties: Dict[str, List[str]]  # {lecturer_id: [course_ids]}

    def can_teach(self, lecturer_id: str, course_id: str) -> bool:
        if lecturer_id not in self.specialties:
            return False
        return course_id in self.specialties[lecturer_id]