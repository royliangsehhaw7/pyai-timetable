from dataclasses import dataclass                                                                                                                                                           
from blackboard.board import Blackboard                                                                                                                                                     
                                                                                                                                                                                             
                                                                                                                                                                                             
@dataclass                                                                                                                                                                                  
class AgentDeps:                                                                                                                                                                            
   """Dependency container for agents.                                                                                                                                                     
                                                                                                                                                                                             
   This dataclass holds shared dependencies that are injected into pydantic-ai                                                                                                             
   agents at runtime. It provides a clean, typed way for agents and their tools                                                                                                            
   to access shared state, like the Blackboard, without being tightly coupled                                                                                                              
   to the orchestrator.
   """

   board: Blackboard
