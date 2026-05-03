from core.log import logger                                                                                                                                    
from core.models import (                                                                                                                                      
    Course,                                                                                                                                                    
    Lecturer,                                                                                                                                                  
    Policy,                                                                                                                                                    
    Room,                                                                                                                                                      
    SchedulingFailure,                                                                                                                                         
    TimetableSlot,                                                                                                                                             
)                                                                                                                                                              
                                                                                                                                                                
                                                                                                                                                                
class Blackboard:                                                                                                                                              
    """Manages the shared state of the timetable generation process.                                                                                           
                                                                                                                                                                
    This class acts as a central repository for all data related to scheduling,                                                                                
    including the initial entities (courses, rooms, etc.), the work-in-progress                                                                                
    timetable (draft_slots), and any conflicts or failures encountered.                                                                                        
                                                                                                                                                                
    It is the single source of truth for the state of the schedule. The orchestrator                                                                           
    is the only component that writes to the Blackboard, while agents' tools can                                                                               
    read from it to inform their decisions.                                                                                                                    
    """                                                                                                                                                        
                                                                                                                                                                
    def __init__(                                                                                                                          
        self,                                                                                                                                                  
        courses: list[Course],                                                                                                                                 
        rooms: list[Room],                                                                                                                                     
        lecturers: list[Lecturer],                                                                                                                             
        policy: Policy,                                                                                                                                        
    ):                                                                                                                                                         
        # Initial data - considered immutable during the run                                                                                                   
        self.courses = courses                                                                                                                                 
        self.rooms = rooms                                                                                                                                     
        self.lecturers = lecturers                                                                                                                             
        self.policy = policy                                                                                                                                   
                                                                                                                                                                
        # Mutable state - managed during the scheduling process                                                                                                
        self.draft_slots: list[TimetableSlot] = []                                                                                                             
        self.conflicts: list[str] = []                                                                                                                         
        self.failures: list[SchedulingFailure] = []                                                                                                            
                                                                                                                                                               
        logger.info(                                                                                                                                           
            f"Blackboard initialized with {len(courses)} courses, "                                                                                            
            f"{len(rooms)} rooms, and {len(lecturers)} lecturers."                                                                                             
        )                                                                                                                                                      
                                                                                                                                                                
    def is_complete(self) -> bool:                                                                                                                             
        """Checks if all courses have been scheduled."""                                                                                                       
        return len(self.draft_slots) == len(self.courses)                                                                                                      
                                                                                                                                                               
    def has_conflicts(self) -> bool:                                                                                                                           
        """Checks if there are any unresolved conflicts."""                                                                                                    
        return len(self.conflicts) > 0                                                                                                                         
                                                                                                                                                                
    def get_next_unscheduled_course(self) -> Course | None:                                                                                                    
        """Finds the next course that does not have a slot yet."""                                                                                             
        scheduled_course_names = set()                                                                                                                         
        for slot in self.draft_slots:                                                                                                                          
            scheduled_course_names.add(slot.course)                                                                                                            
                                                                                                                                                                
        for course in self.courses:                                                                                                                            
            if course.name not in scheduled_course_names:                                                                                                      
                logger.debug(f"Next unscheduled course: {course.name}")                                                                                        
                return course                                                                                                                                  
                                                                                                                                                               
        logger.debug("No unscheduled courses remaining.")                                                                                                      
        return None                                                                                                                                            
                                                                                                                                                                
    def get_used_rooms_on_day(self, day: str) -> list[str]:                                                                                                    
        """Returns a list of room names already in use on a given day."""                                                                                      
        used_rooms = []                                                                                                                                        
        for slot in self.draft_slots:                                                                                                                          
            if slot.day == day:                                                                                                                                
                used_rooms.append(slot.room)                                                                                                                   
        return used_rooms                                                                                                                                      
                                                                                                                                                                
    def get_used_lecturers_on_day(self, day: str) -> list[str]:                                                                                                
        """Returns a list of lecturer names already in use on a given day."""                                                                                  
        used_lecturers = []                                                                                                                                    
        for slot in self.draft_slots:                                                                                                                          
            if slot.day == day:                                                                                                                                
                used_lecturers.append(slot.lecturer)                                                                                                           
        return used_lecturers                                                                                                                                  
                                                                                                                                                                
    def get_available_day(self) -> str | None:                                                                                                                 
        """Finds the first valid day with at least one free room and lecturer."""                                                                              
        num_total_rooms = len(self.rooms)                                                                                                                      
        num_total_lecturers = len(self.lecturers)                                                                                                              
                                                                                                                                                               
        for day in self.policy.school_days:                                                                                                                    
            num_used_rooms = len(self.get_used_rooms_on_day(day))                                                                                              
            num_used_lecturers = len(self.get_used_lecturers_on_day(day))                                                                                      
                                                                                                                                                               
            has_free_room = num_used_rooms < num_total_rooms                                                                                                   
            has_free_lecturer = num_used_lecturers < num_total_lecturers                                                                                       
                                                                                                                                                               
            if has_free_room and has_free_lecturer:                                                                                                            
                logger.debug(f"Found available day: {day}")                                                                                                    
                return day                                                                                                                                     
                                                                                                                                                               
        logger.warning("No available day found with free rooms and lecturers.")                                                                                
        return None                                                                                                                                            
                                                                                                                                                               
    def add_slot(self, slot: TimetableSlot):                                                                                                                   
        """Adds a new timetable slot to the draft."""                                                                                                          
        self.draft_slots.append(slot)                                                                                                                          
        logger.info(                                                                                                                                           
            f"Added slot: {slot.day}, {slot.course}, {slot.room}, {slot.lecturer}"                                                                             
        )                                                                                                                                                      
                                                                                                                                                               
    def remove_slot_for_course(self, course_name: str):                                                                                                        
        """Removes a timetable slot associated with a given course."""                                                                                         
        slot_to_remove = None                                                                                                                                  
        for slot in self.draft_slots:                                                                                                                          
            if slot.course == course_name:                                                                                                                     
                slot_to_remove = slot                                                                                                                          
                break                                                                                                                                          
                                                                                                                                                               
        if slot_to_remove:                                                                                                                                     
            self.draft_slots.remove(slot_to_remove)                                                                                                            
            logger.warning(                                                                                                                                    
                f"Removed slot for course '{course_name}' due to conflict."                                                                                    
            )                                                                                                                                                  
        else:                                                                                                                                                  
            logger.error(                                                                                                                                      
                f"Attempted to remove slot for non-existent course: {course_name}"                                                                             
            )                                                                                                                                                  
                                                                                                                                                               
    def add_conflict(self, reason: str):                                                                                                                       
        """Records a scheduling conflict."""                                                                                                                   
        self.conflicts.append(reason)                                                                                                                          
        logger.warning(f"Conflict detected: {reason}")                                                                                                         
                                                                                                                                                               
    def clear_conflicts(self):                                                                                                                                 
        """Clears all recorded conflicts."""                                                                                                                   
        if self.conflicts:                                                                                                                                     
            logger.debug(f"Clearing {len(self.conflicts)} conflicts.")                                                                                         
            self.conflicts.clear()                                                                                                                             
                                                                                                                                                               
    def add_failure(self, failure: SchedulingFailure):                                                                                                         
        """Records a failure reported by an agent."""                                                                                                          
        self.failures.append(failure)                                                                                                                          
        logger.error(                                                                                                                                          
            f"Agent '{failure.agent}' failed to schedule '{failure.course}' "                                                                                  
            f"on {failure.day}: {failure.reason}"                                                                                                              
        )   