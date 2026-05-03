 ## Phase 1: Core Definitions                                                                                                                                       
 ### Priority: CRITICAL – All other modules depend on these.                                                                                                        
                                                                                                                                                                    
 - [x] **Create `core/log.py`**                                                                                                                                     
     - **Purpose:** Configure and expose a single, project-wide logger, as per `SPECIFICATIONS.md` §6.2.                                                            
 - [x] **Create `core/models.py`**                                                                                                                                  
     - **Purpose:** Define all Pydantic data models for the entire project in one place. This is the single source of truth for data shapes. (§6.2)                 
     - **Models to include:** `Course`, `Room`, `Lecturer`, `Policy` (§3), `TimetableSlot` (§4), `RoomSuggestion`, `LecturerSuggestion`, `SchedulingFailure` (§8).  
 - [x] **Create `core/deps.py`**                                                                                                                                    
     - **Purpose:** Define the `AgentDeps` dataclass for dependency injection into `pydantic-ai` agents. (§8.0)                                                     
     - **Contents:** A single `@dataclass` named `AgentDeps` containing `board: Blackboard`.                                                                        
                                                                                                                                                                    
 ## Phase 2: Data Loading Tools                                                                                                                                     
 ### Priority: HIGH – The application needs data to run.                                                                                                            
                                                                                                                                                                    
 - [ ] **Create `tools/get_courses.py`**                                                                                                                            
     - **Purpose:** Read `database/courses.json` and return `list[Course]`. (§6.2)                                                                                  
 - [ ] **Create `tools/get_rooms.py`**                                                                                                                              
     - **Purpose:** Read `database/rooms.json` and return `list[Room]`. (§6.2)                                                                                      
 - [ ] **Create `tools/get_lecturers.py`**                                                                                                                          
     - **Purpose:** Read `database/lecturers.json` and return `list[Lecturer]`. (§6.2)                                                                              
 - [ ] **Create `tools/get_policy.py`**                                                                                                                             
     - **Purpose:** Read `database/policy.json` and return a `Policy` object. (§6.2)                                                                                
                                                                                                                                                                    
 ## Phase 3: Blackboard State Management                                                                                                                            
 ### Priority: HIGH – The central state manager.                                                                                                                    
                                                                                                                                                                    
 - [x] **Create `blackboard/board.py`**                                                                                                                             
     - **Purpose:** To own and manage all shared, mutable state for the scheduling process. Exposes query methods for the orchestrator and tools. (§5.1, §6.2)      
     - **Key Methods:** `get_next_unscheduled_course()`, `get_available_day()`, `get_used_rooms_on_day(day)`, `get_used_lecturers_on_day(day)`, `is_complete()`,    
 `has_conflicts()`.                                                                                                                                                 
                                                                                                                                                                    
 ## Phase 4: Agent Support Tools                                                                                                                                    
 ### Priority: MEDIUM – Agents need these tools to query state.                                                                                                     
                                                                                                                                                                    
 - [ ] **Create `tools/check_room.py`**                                                                                                                             
     - **Purpose:** Provide a tool for the `RoomAgent`. Answers "is this room free on this day?" by reading from the Blackboard. (§6.2, §8.1)                       
 - [ ] **Create `tools/check_lecturer.py`**                                                                                                                         
     - **Purpose:** Provide a tool for the `LecturerAgent`. Answers "is this lecturer free on this day?" by reading from the Blackboard. (§6.2, §8.2)               
                                                                                                                                                                    
 ## Phase 5: Agent Implementation                                                                                                                                   
 ### Priority: MEDIUM – The LLM-powered components.                                                                                                                 
                                                                                                                                                                    
 - [ ] **Create `agents/room_agent.py`**                                                                                                                            
     - **Purpose:** Define the `pydantic-ai` agent responsible for suggesting a room based on the course and day. Returns a `RoomSuggestion` result. (§6.2, §8.1)   
 - [ ] **Create `agents/lecturer_agent.py`**                                                                                                                        
     - **Purpose:** Define the `pydantic-ai` agent responsible for suggesting a lecturer for a course and day. Returns a `LecturerSuggestion` result. (§6.2, §8.2)  
                                                                                                                                                                    
 ## Phase 6: Orchestration                                                                                                                                          
 ### Priority: CRITICAL – The brain of the application.                                                                                                             
                                                                                                                                                                    
 - [ ] **Create `orchestrator/orchestrator.py`**                                                                                                                    
     - **Purpose:** Implement the main control loop that drives scheduling. This is a plain Python class that acts as the **Mediator** and applies the              
 **Reflexion** pattern. It is **not** an agent. (§7, §6.2)                                                                                                          
     - **Key Responsibilities:**                                                                                                                                    
         1.  **State-driven Loop:** Run the main `while` loop based on `Blackboard.is_complete()`.                                                                  
         2.  **State Query:** Get the next course and an available day from the Blackboard.                                                                         
         3.  **Agent Mediation:** Call the `RoomAgent` and `LecturerAgent` sequentially.                                                                            
         4.  **Result Handling:** Check the `success` flag on agent results. Log failures to the Blackboard via `SchedulingFailure` and loop back.                  
         5.  **State Mutation:** On success, write the new `TimetableSlot` to the Blackboard.                                                                       
         6.  **Reflexion:** After writing, run a conflict check. If conflicts are found, remove the slot, log the conflict, and loop back to self-correct.          
         7.  **Retry Management:** Enforce a retry limit to prevent infinite loops.                                                                                 
                                                                                                                                                                    
 ## Phase 7: Application Bootstrap                                                                                                                                  
 ### Priority: LOW – The entry point that wires everything together.                                                                                                
                                                                                                                                                                    
 - [ ] **Create `main.py`**                                                                                                                                         
     - **Purpose:** The main entry point for the application. (§6.1)                                                                                                
     - **Logic:**                                                                                                                                                   
         1.  Use `core.log` to set up logging.                                                                                                                      
         2.  Use tools from Phase 2 to load all data.                                                                                                               
         3.  Initialize the `Blackboard` with the loaded data.                                                                                                      
         4.  Initialize the `Orchestrator` with the Blackboard and agent instances.                                                                                 
         5.  Call the orchestrator's main run method.                                                                                                               
         6.  Print the final timetable or failure report from the Blackboard.      