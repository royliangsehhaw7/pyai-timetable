
# SPECIFICATIONS.md — Enterprise Adaptive Scheduler

## 1. Project Overview
The **Enterprise Adaptive Scheduler** is a multi-agent system built with **Pydantic AI** designed to autonomously generate valid, conflict-free schedules. This system relies on a strict **Constraint-Based** model, prioritizing state-space reduction, the **Orchestration Pattern**, and the **Reflexion Pattern** to manage domain constraints.

### Core Technologies
*   **Framework:** Pydantic AI (Strict schema validation for LLM outputs).
*   **Language:** Python 3.12+ (Asyncio for parallel validation).
*   **Data Layer:** Abstracted Data Contracts (Agnostic to JSON, SQL, or API backends).

---
## 4.D Architecture Enforcement Rules [NEW]

### **Strict Mediator Pattern Requirements:**

1. **No Direct Agent Communication:**
   - Agents MUST NOT import, reference, or have any awareness of other agents
   - Agent output models MUST NOT be used as input models for other agents
   - All inter-agent data MUST pass through Orchestrator transformation

2. **Orchestrator Sovereignty:**
   - The Orchestrator owns ALL workflow and sequencing logic
   - Agents MUST be stateless regarding workflow position
   - The Orchestrator decides which agents to involve and when

3. **Context Isolation:**
   - Each agent receives ONLY the context it needs from the Orchestrator
   - The Orchestrator MUST transform outputs before sending to next agent
   - No agent should infer workflow state from its input context

4. **Implementation Verification:**
   - Code reviews MUST check for direct agent dependencies
   - Import statements MUST NOT cross agent boundaries
   - All agent communication MUST be traceable through the Orchestrator


## 2. Implementation Philosophy: "Imperative First"
This project adheres to a strict hierarchy of authority and the Single Responsibility Principle (SRP) to ensure system reliability:

*   **Deterministic Guardrails:** Mathematical clashes, temporal availability are handled exclusively by **Python tools**. The AI is never trusted to "calculate" availability.
*   **Heuristic Reasoning:** The AI is reserved for **Strategy and Pedagogy**, deciding which execution paths or time slots are "optimal" based on non-mathematical factors (e.g., preventing subject fatigue).
*   **The "Flavor vs. Fact" Rule:** The Python Engine ensures the **Facts** (the schedule is physically and temporally valid); the AI provides the **Flavor** (the schedule is strategically optimized).


---


## 3. Domain Constraints & Contracts
These represent the immutable "Rules of the Game". The system interacts with these rules via defined schemas, abstracting away the underlying database.

*   **Temporal Scope:** Operations are bounded by defined working hours and operational days (e.g., Monday-Friday, 08:00-17:00), including hard exclusion zones (e.g., mandatory lunch hours).
*   **Workload Fulfillment:** Entities (courses/tasks) possess strict temporal quotas that must be met precisely. Over-scheduling and under-scheduling trigger automatic rejections.
*   **Pedagogical Daily Caps:** To prevent fatigue, no single entity can exceed a defined daily threshold limit.
*   **Zero-Overlap Policy:** A strict constraint ensuring absolute uniqueness for any (Time, Space) coordinate.

---


## 4. Architecture & Design Patterns
The system architecture separates deterministic state management from non-deterministic intelligence using a strict Star (Hub-and-Spoke) Topology. This ensures that the system remains modular and prevents "pipeline" logic from creating brittle dependencies between agents.

### A. Topology Diagram
Plaintext

              [ CRITIC: POLICY ]          [ CRITIC: ROOM ]
                         ^                         ^
                         |        (Audit)          |
                         +-----------+-------------+
                                     |
          +------------+             |            +----------------+
          |  COURSE    | <----[ORCHESTRATOR]----> |   BLACKBOARD   |
          |   AGENT    |                          | (Grid + Memory)|
          |  (Proposer)|                          +----------------+
          +------------+
          


### B. Core Components [UPDATED]
- **The Blackboard (Hub):** The thread-safe, single source of truth. It manages the Grid and the Rejection Ledger. Only the Orchestrator holds write privileges to this state.
- **The Orchestrator (Mediator):** Acts as the **sole coordinator and decision-maker**. It **prevents any agent-to-agent communication** and eliminates pipeline dependencies by enforcing that:
   1. **Agents only communicate with the Orchestrator**, never with each other
   2. **Agents have no knowledge** of other agents' existence or sequence
   3. **Workflow logic resides exclusively in the Orchestrator**, not in agent interactions
- **State Space Reduction (The Strategist):** A pre-processor agent that analyzes workload contracts before the main loop begins. It determines the optimal execution sequence to prevent late-stage deadlocks.
- **The Course Agent (Proposer):** [UPDATED] A specialized agent whose sole responsibility is to suggest Temporal Coordinates (Day/Time) based on course requirements and the current blackboard state.
- **The Room Agent (Auditor):** [UPDATED] A specialized agent that performs high-fidelity audits of room availability and physical constraints for proposed coordinates.

### C. Design Patterns
- **The Generator-Critic Pattern:** The Course Agent proposes a candidate slot, and the Room Agent audits it against domain constraints.
- **The Reflexion Pattern:** If a constraint is violated, the exact failure reason is logged to the Rejection Ledger. The Orchestrator then passes this history back to the Course Agent to prune its future search space.
- **The Mediator Pattern:** The Orchestrator isolates agent conversations, ensuring that agents never communicate directly. This **eliminates pipeline architectures** where agents have implicit dependencies on each other's outputs.
- **Anti-Pipeline Enforcement:** The system **explicitly forbids** any form of sequential pipeline where Agent A's output becomes Agent B's input. Instead, the Orchestrator receives outputs, makes decisions, and provides fresh context to each agent.

---


## 5. Pydantic AI Implementation Guide [NEW]

### A. Agent Definition Protocol
All agents inherit from Pydantic AI's `Agent` class and follow a consistent pattern:

```python
# Example: course_agent.py
class CourseAgent(Agent):
    """Proposes valid scheduling coordinates for courses."""
    
    def __init__(self, deps: AgentDependencies):
        super().__init__(
            system=self._get_system_prompt(),
            tools=[
                deps.tools.get_course_data,
                deps.tools.check_temporal_availability,
                deps.tools.get_working_hours,
            ]
        )
        self.blackboard = deps.blackboard
    
    @agent_session
    async def propose_slot(self, course: CourseModel) -> ProposalModel:
        """Main entry point for course scheduling proposals."""
```

### B. Dependency Injection Pattern
The system uses a centralized dependency injection container (`core/deps.py`) to manage all shared resources:

```python
# core/deps.py
class AgentDependencies(BaseModel):
    """Dependencies injected into all agents."""
    blackboard: BlackboardState
    tools: ToolRegistry
    config: AgentConfig

def get_agent_dependencies() -> AgentDependencies:
    """Factory function providing dependencies to agents."""
    return AgentDependencies(
        blackboard=get_blackboard(),
        tools=get_tool_registry(),
        config=get_agent_config()
    )
```

### C. Mediator-Focused Implementation Example

```python
# CORRECT: Mediator Pattern Implementation
class Orchestrator:
    async def mediate_scheduling(self, course_id: str):
        # 1. Get fresh context from Blackboard (not from previous agent)
        context = self.blackboard.get_scheduling_context(course_id)
        
        # 2. Request proposal FROM SCRATCH (not continuing a conversation)
        proposal = await self.course_agent.propose_slot(context)
        
        # 3. Transform for room validation (Mediator role)
        room_validation_request = RoomValidationRequest(
            room_id=proposal.room_id,
            day=proposal.day,
            time=proposal.time,
            course_size=context.course_size
            # NOTE: Not passing the full proposal or Course Agent reasoning!
        )
        
        # 4. Independent validation request
        validation = await self.room_agent.validate_room(room_validation_request)
        
        # 5. Orchestrator makes final decision
        return self._synthesize_decision(proposal, validation)
```

### C. Message Flow & Schema Contracts
- **Agent Input Schemas:** Each agent accepts strictly typed Pydantic models
- **Agent Output Schemas:** Each agent returns validated Pydantic models
- **Error Handling:** All agent failures produce structured error responses with actionable feedback

---


## 6. Technical Anchors (The Implementation Boundaries)
All components are anchored to these specific Pydantic constructs to enforce strict I/O boundaries.

### **A. Dependency Injection (Agent Tools)**
Agents are prohibited from accessing global state and must use stateless tools injected via the dependency container:

*   **Data Tools:** `tools/get_data.py` - Functions for retrieving course, room, and policy data
*   **Course Tools:** `tools/course_tools.py` - Course-specific validation and calculation logic
*   **Room Tools:** `tools/room_tools.py` - Room-specific availability and constraint checking
*   **Context Tools:** Readers that allow agents to view the `Rejection Ledger` to enable Reflexion

### **B. Schema Contracts (Interface Models)**
| Component | Model Name | Responsibility |
| :--- | :--- | :--- |
| **State** | `BlackboardState` | Defines the structure of the Grid, Fulfillment Counters, and Ledger. |
| **Data** | `EntityModel` | Defines the requirement parameters of a workload item (e.g., Course). |
| **I/O** | `ProposalModel` | Enforces structural validity for proposed Coordinates (Day, Time, Space). |

### **C. Dependency Container Pattern** [NEW]
All shared resources are managed through a centralized dependency container:

```python
# Directory Structure Addition
adaptive_scheduler/
├── core/                    # Dependency injection & configuration
│   ├── deps.py             # Dependency registry (factory functions)
│   └── config.py           # LLM settings, timeouts, environment config
```

Benefits:
- **Single source of truth** for shared resources
- **Easy mocking** for unit testing
- **Consistent configuration** across environments
- **Clean lifecycle management** for stateful components

---


## 7. Directory Structure (Clean Architecture) [UPDATED]
```text
adaptive_scheduler/
├── core/                    # [NEW] Dependency injection & configuration
│   ├── deps.py             # Dependency registry (factory functions)
│   └── config.py           # LLM settings, timeouts, environment config
├── config/                  # Environment-specific settings only
├── data/                    # Data Source Adapters (JSON, SQL, APIs)
├── schemas/
│   ├── communication.py     # Pydantic models for Agent-Orchestrator I/O
│   └── state.py            # Internal Blackboard & Grid schemas
├── domain/
│   └── blackboard.py        # State Manager: Grid & Rejection Ledger
├── services/
│   ├── orchestrator.py      # Mediator: The Master Loop & Reflexion Logic
└── agents/                  # [UPDATED] SRP-based agent names
│   ├── strategist.py        # Optimizer: Determines execution priority
│   ├── course_agent.py      # [UPDATED] Proposer: Suggests valid time coordinates
│   └── room_agent.py        # [UPDATED] Validator: Maps physical space availability
├── tools/                   # [UPDATED] Agent Capabilities (Stateless Functions)
│   ├── get_data.py          # [UPDATED] Data retrieval tools
│   ├── course_tools.py      # [UPDATED] Course-specific validation logic
│   └── room_tools.py        # [UPDATED] Room-specific validation logic
└── main.py                  # Application Bootstrap
```

---


## 8. Message Flow & Agent I/O [NEW]

### A. Agent Communication Protocol
1. **Orchestrator → Course Agent:** "Propose a slot for Course X"
2. **Course Agent → Tools:** Query data and validate constraints
3. **Course Agent → Orchestrator:** Return `ProposalModel` or `RejectionReason`
4. **Orchestrator → Room Agent:** "Validate room availability for Proposal Y"
5. **Room Agent → Tools:** Check room constraints and availability
6. **Room Agent → Orchestrator:** Return `ValidationResult` (pass/fail with details)

### B. Reflexion Loop Implementation
1. **Proposal Rejection:** Details logged to `RejectionLedger` in blackboard
2. **History Injection:** Course Agent receives rejection history via context
3. **Adaptive Behavior:** Course Agent uses history to avoid previously failed patterns
4. **Convergence:** Loop continues until valid proposal or maximum attempts reached

---


## 9. Execution Logic (The State Machine)
1.  **Context Assembly:** The Orchestrator initializes the dependency container and blackboard.
2.  **Strategic Ordering:** The Strategist evaluates the workload and returns a prioritized Execution Queue.
3.  **Negotiation Loop:** For each required quota in the Queue:
    *   **Proposal:** The Course Agent uses injected tools to suggest a slot adhering to domain constraints.
    *   **Validation:** The Room Agent verifies physical feasibility for the proposed slot.
4.  **Resolution:**
    *   **Valid:** Orchestrator commits the coordinate to the Blackboard and advances the state.
    *   **Invalid:** Orchestrator updates the Rejection Ledger; triggers a reflexive retry within the negotiation loop.

---


## 10. Testing & Validation Strategy [NEW]

### A. Unit Testing
- **Deterministic Tools:** Test tools in isolation with mocked data
- **Agent Logic:** Test agents with mocked dependencies from `core/deps.py`

### B. Integration Testing
- **Agent Coordination:** Test Orchestrator with real agents but mocked LLM
- **End-to-End Flow:** Test complete scheduling pipeline with sample data

### C. LLM Testing Strategy
- **Mock Responses:** Use predefined responses for reproducible tests
- **Prompt Testing:** Validate system prompts produce expected behavior
- **Regression Testing:** Capture and replay successful LLM interactions

---


## 11. Development Workflow
1. **Phase 1:** Implement core schemas and dependency container
2. **Phase 2:** Build deterministic tools and validation logic
3. **Phase 3:** Implement agents with mocked LLM responses
4. **Phase 4:** Integrate real LLM providers and refine prompts
5. **Phase 5:** Add reflexion patterns and optimization logic

---


*Document Version: 2.0 - Updated with Pydantic AI patterns, SRP naming, and dependency injection*
