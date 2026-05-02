
# SPECIFICATIONS.md — Enterprise Adaptive Scheduler

## 1. Project Overview
The **Enterprise Adaptive Scheduler** is a multi-agent system built with **Pydantic AI** designed to autonomously generate valid, conflict-free schedules. This system relies on a strict **Constraint-Based** model, prioritizing state-space reduction, the **Orchestration Pattern**, and the **Reflexion Pattern** to manage domain constraints.

### Core Technologies
*   **Framework:** Pydantic AI (Strict schema validation for LLM outputs).
*   **Language:** Python 3.12+ (Asyncio for parallel validation).
*   **Data Layer:** Abstracted Data Contracts (Agnostic to JSON, SQL, or API backends).

---


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

            [ CRITIC: ROOM ]          [ CRITIC: POLICY ]
                       ^                         ^
                       |        (Audit)          |
                       +-----------+-------------+
                                   |
        +------------+             |            +----------------+
        | GENERATOR  | <----[ORCHESTRATOR]----> |   BLACKBOARD   |
        | (Proposer) |                          | (Grid + Memory)|
        +------------+                          +----------------+
                                 


### B. Core Components
- The Blackboard (Hub): The thread-safe, single source of truth. It manages the Grid and the Rejection Ledger. Only the Orchestrator holds write privileges to this state.
- The Orchestrator (Mediator): Acts as the central router and execution engine. It prevents agent-to-agent hallucination cascades by enforcing that all communication must pass through this central hub.
- State Space Reduction (The Strategist): A pre-processor agent that analyzes workload contracts before the main loop begins. It determines the optimal execution sequence to prevent late-stage deadlocks.
- The Generator (Proposer): A specialized agent whose sole responsibility is to suggest Temporal Coordinates (Day/Time) based on the current state and the Rejection Ledger.
- The Critic Agents (Auditors): Specialized agents (e.g., Room, Policy) that perform high-fidelity audits of a single proposal. They provide the heuristic reasoning required for the Reflexion loop.

### C. Design Patterns
- The Generator-Critic Pattern: The Generator proposes a candidate slot, and the Critics audit it against specific domain constraints.
- The Reflexion Pattern: If a constraint is violated, the exact failure reason is logged to the Rejection Ledger. The Orchestrator then passes this history back to the Generator to prune its future search space.
- The Mediator Pattern: The Orchestrator isolates agent conversations, ensuring that a "Critic" never talks to a "Generator" directly. This maintains the integrity of the Star Topology.


---


## 5. Technical Anchors (The Implementation Boundaries)
All components are anchored to these specific Pydantic constructs to enforce strict I/O boundaries.

### **A. Dependency Injection (Agent Tools)**
Agents are prohibited from accessing global state and must use stateless tools injected via `RunContext`:
*   **Validation Tools:** Deterministic functions (e.g., `temporal_tools.py`, `spatial_tools.py`) that represent the *only* mechanisms for checking Grid or Room occupancy.
*   **Context Tools:** Readers that allow agents to view the `Rejection Ledger` to enable Reflexion.

### **B. Schema Contracts (Interface Models)**
| Component | Model Name | Responsibility |
| :--- | :--- | :--- |
| **State** | `BlackboardState` | Defines the structure of the Grid, Fulfillment Counters, and Ledger. |
| **Data** | `EntityModel` | Defines the requirement parameters of a workload item (e.g., Course). |
| **I/O** | `ProposalModel` | Enforces structural validity for proposed Coordinates (Day, Time, Space). |


---


## 6. Directory Structure (Clean Architecture)
```text
adaptive_scheduler/
├── config/                  # Environment, API Keys, LLM settings
├── data/                    # Data Source Adapters (JSON, SQL, APIs)
├── schemas/
│   ├── communication.py     # Pydantic models for Agent-Orchestrator I/O
│   └── state.py             # Internal Blackboard & Grid schemas
├── domain/
│   └── blackboard.py        # State Manager: Grid & Rejection Ledger
├── services/
│   └── orchestrator.py      # Mediator: The Master Loop & Reflexion Logic
├── agents/
│   ├── strategist.py        # Optimizer: Determines execution priority
│   ├── temporal_agent.py    # Proposer: Suggests valid time coordinates
│   └── spatial_agent.py     # Validator: Maps physical space to time coordinates
├── tools/                   # Agent Capabilities (Stateless Functions)
│   ├── temporal.py          # Deterministic logic for time/grid checks
└── main.py                  # Application Bootstrap
```


---


## 7. Execution Logic (The State Machine)
1.  **Context Assembly:** The Orchestrator initializes the Blackboard with configured Data Contracts.
2.  **Strategic Ordering:** The Strategist evaluates the workload and returns a prioritized Execution Queue.
3.  **Negotiation Loop:** For each required quota in the Queue:
    *   **Proposal:** The Temporal Agent queries tools to suggest a slot adhering to domain constraints.
    *   **Validation:** The Spatial Agent verifies physical feasibility for the proposed slot.
4.  **Resolution:**
    *   **Valid:** Orchestrator commits the coordinate to the Blackboard and advances the state.
    *   **Invalid:** Orchestrator updates the Rejection Ledger; triggers a reflexive retry within the negotiation loop.