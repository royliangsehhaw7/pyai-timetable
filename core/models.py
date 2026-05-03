from pydantic import BaseModel
from typing import Optional

# ===== Source Entities =====                                                                                   
# These are the primary INPUT models. They represent the raw data that the system
# will use to generate the timetable. They are loaded once at the start of the
# application and placed on the Blackboard

class Course(BaseModel):                                                                                                                                           
    """                                                                                                                                                            
    [INPUT MODEL]                                                                                                                                                  
    Represents a single course that needs to be scheduled.                                                                                                         
    - Loaded from: `database/courses.json`                                                                                                                         
    - Used by: The Orchestrator reads these from the Blackboard to decide which course to schedule next.                                                           
    """                                                                                                                                                            
    name: str                                                                                                                                                      
                                                                                                                                                                    
class Room(BaseModel):                                                                                                                                             
    """                                                                                                                                                            
    [INPUT MODEL]                                                                                                                                                  
    Represents a physical room where a course can be held.                                                                                                         
    - Loaded from: `database/rooms.json`                                                                                                                           
    - Used by: The RoomAgent's tools will check availability against the list of all available rooms.                                                              
    """                                                                                                                                                            
    name: str                                                                                                                                                      
                                                                                                                                                                    
class Lecturer(BaseModel):                                                                                                                                         
    """                                                                                                                                                            
    [INPUT MODEL]                                                                                                                                                  
    Represents a lecturer who can teach a course.                                                                                                                  
    - Loaded from: `database/lecturers.json`                                                                                                                       
    - Used by: The LecturerAgent's tools will check availability against the list of all available lecturers.                                                      
    """                                                                                                                                                            
    name: str                                                                                                                                                      
                                                                                                                                                                    
class Policy(BaseModel):                                                                                                                                           
    """                                                                                                                                                            
    [INPUT MODEL]                                                                                                                                                  
    Defines the global rules and constraints for the entire scheduling process, like valid                                                                         
    school days and hours.                                                                                                                                         
    - Loaded from: `database/policy.json`                                                                                                                          
    - Used by: The Blackboard reads `school_days` to provide valid days for scheduling.                                                                            
      The Orchestrator will use the hours to check for policy violations.                                                                                          
    """                                                                                                                                                            
    school_days: list[str]                                                                                                                                         
    school_start_hour: int                                                                                                                                         
    school_end_hour: int                                                                                                                                           
    lunch_start_hour: int                                                                                                                                          
    lunch_end_hour: int             


# ===== Final Output Model (§4) =====                                                                                                                              
# This model defines the structure of the final, desired output of the system.                                                                                     
                                                                                                                                                                    
class TimetableSlot(BaseModel):                                                                                                                                    
    """                                                                                                                                                            
    [FINAL OUTPUT MODEL]                                                                                                                                           
    Represents a single, successfully scheduled slot in the final timetable. A complete                                                                            
    schedule is a list of these objects.                                                                                                                           
    - Created by: The Orchestrator, after successfully getting suggestions from all agents.                                                                        
    - Stored on: The Blackboard's `draft_slots` list.                                                                                                              
    """                                                                                                                                                            
    day: str                                                                                                                                                       
    course: str                                                                                                                                                    
    room: str                                                                                                                                                      
    lecturer: str                                                                                                                                                  
                                                                                                                                                                    
                                                                                                                                                                    
# ===== Agent Contracts: Intermediate & Internal Models (§8) =====                                                                                                 
# These models are used for communication between agents and the orchestrator, and                                                                                 
# for internal state management. They are not part of the initial input or the final output.                                                                       
                                                                                                                                                                    
class RoomSuggestion(BaseModel):                                                                                                                                   
    """                                                                                                                                                            
    [INTERMEDIATE DATA TRANSFER MODEL]                                                                                                                             
    This is the structured response returned by the RoomAgent. It follows the Agent                                                                                
    Result Contract (success bool, reason string).                                                                                                                 
    - Created by: `RoomAgent`                                                                                                                                      
    - Used by: The Orchestrator reads this to decide whether to proceed with scheduling or                                                                         
      to handle a failure.                                                                                                                                         
    """                                                                                                                                                            
    success: bool                                                                                                                                                  
    room: Optional[str] = None                                                                                                                                     
    day: Optional[str] = None                                                                                                                                      
    reason: str                                                                                                                                                    
                                                                                                                                                                    
class LecturerSuggestion(BaseModel):                                                                                                                               
    """                                                                                                                                                            
    [INTERMEDIATE DATA TRANSFER MODEL]                                                                                                                             
    This is the structured response returned by the LecturerAgent. It follows the Agent                                                                            
    Result Contract.                                                                                                                                               
    - Created by: `LecturerAgent`                                                                                                                                  
    - Used by: The Orchestrator reads this to decide whether to create a `TimetableSlot` or                                                                        
      to handle a failure.                                                                                                                                         
    """                                                                                                                                                            
    success: bool                                                                                                                                                  
    lecturer: Optional[str] = None                                                                                                                                 
    day: Optional[str] = None                                                                                                                                      
    reason: str                                                                                                                                                    
                                                                                                                                                                    
class SchedulingFailure(BaseModel):                                                                                                                                
    """                                                                                                                                                            
    [INTERNAL STATE MODEL]                                                                                                                                         
    A record created by the Orchestrator when an agent fails to provide a valid                                                                                    
    suggestion (e.g., returns `success=False`). It's a way for the system to remember                                                                              
    its failures.                                                                                                                                                  
    - Created by: The Orchestrator.                                                                                                                                
    - Stored on: The Blackboard's `failures` list for final reporting.                                                                                             
    """                                                                                                                                                            
    course: str                                                                                                                                                    
    agent: str # e.g., "room_agent" or "lecturer_agent"                                                                                                            
    day: str
    reason: str
