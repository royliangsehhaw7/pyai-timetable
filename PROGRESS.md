## Current Status: Implementation In Progress
The project is currently in the **Foundation Implementation** phase (Phase 1).
                                                                                                      
## Phase 0: Infrastructure & Core Setup
- [x] Environment Setup (Python venv & Libraries)
- [x] Project structure created
- [x] `SPECIFICATIONS.md` finalized
                                                                                                      
## Phase 1: Core Schemas & Dependency Injection (START HERE)
### Priority: HIGH – All agents depend on these

#### A. Schema Contracts (`schemas/`)
- [ ] **Create `schemas/__init__.py`**
- [ ] **Create `schemas/base.py`** – Base models and shared enums
- [ ] **Create `schemas/entity.py`** – `EntityModel` (base workload item)
- [ ] **Create `schemas/proposal.py`** – `ProposalModel` (Course Agent output)
- [ ] **Create `schemas/validation.py`** – `ValidationResult`, `RejectionReason` (validation outputs)
- [ ] **Create `schemas/scheduling_request.py`** – Agent input models
- [ ] **Create `schemas/state.py`** – Internal state models (BlackboardState, GridCell, RejectionLedgerEntry)

#### B. Dependency Injection (`core/`) - NEXT
- [ ] **Create `core/__init__.py`**
- [ ] **Create `core/config.py`** – LLM settings, timeouts, environment config
  - [ ] `AgentConfig` model with LLM provider settings
  - [ ] `get_agent_config()` factory function
- [ ] **Create `core/deps.py`** – Dependency registry (CRITICAL)
  - [ ] `AgentDependencies` model (blackboard, tools, config)
  - [ ] `ToolRegistry` model for organizing tools
  - [ ] `get_agent_dependencies()` factory function
  - [ ] `get_tool_registry()` factory function

#### C. Data Layer (`data/`) – Mock implementations first
- [x] `data/` exists
- [ ] **Update `data/__init__.py`**
- [ ] **Create `data/mock_registries.py`** – Mock data for development
  - [ ] Mock courses, rooms, lecturers
  - [ ] Mock availability schedules
  - [ ] Simple in-memory storage

## Phase 2: Deterministic Tools (Stateless Functions)

#### A. Data Retrieval Tools (`tools/get_data.py`)
- [ ] **Create `tools/__init__.py`**
- [ ] **Create `tools/get_data.py`** – Pure data access functions
  - [ ] `get_course_by_id(course_id) → CourseModel`
  - [ ] `get_room_by_id(room_id) → RoomModel`
  - [ ] `get_lecturer_by_id(lecturer_id) → LecturerModel`
  - [ ] `get_available_rooms(day, time) → List[RoomModel]`

#### B. Course-Specific Tools (`tools/course_tools.py`)
- [ ] **Create `tools/course_tools.py`** – Course validation logic
  - [ ] `check_course_requirements(course, day, time) → bool`
  - [ ] `validate_course_duration(course, start_time, duration) → bool`
  - [ ] `check_daily_course_cap(course_id, day, grid) → bool`

#### C. Room-Specific Tools (`tools/room_tools.py`)
- [ ] **Create `tools/room_tools.py`** – Room validation logic
  - [ ] `check_room_availability(room_id, day, time) → bool`
  - [ ] `validate_room_capacity(room_id, course_size) → bool`
  - [ ] `check_room_specialty(room_id, course_type) → bool`
  - [ ] `detect_room_conflicts(room_id, day, time, grid) → bool`

#### D. Temporal Validation Tools (`tools/temporal_tools.py`)
- [ ] **Create `tools/temporal_tools.py`** – Time-based validation
  - [ ] `check_temporal_availability(day, time, grid) → bool`
  - [ ] `validate_working_hours(day, time) → bool`
  - [ ] `enforce_lunch_break(day, time) → bool`
  - [ ] `check_daily_workload_cap(day, course_id, grid) → bool`

## Phase 3: Domain Layer – Blackboard State Management

#### A. Blackboard Implementation (`domain/blackboard.py`)
- [ ] **Create `domain/__init__.py`**
- [ ] **Create `domain/blackboard.py`** – Thread-safe state manager
  - [ ] `Blackboard` class with thread locks
  - [ ] `get_state() → BlackboardState` (read-only)
  - [ ] `update_grid(proposal: ProposalModel) → None` (orchestrator only)
  - [ ] `add_rejection(entry: RejectionLedgerEntry) → None`
  - [ ] `get_rejection_history(course_id) → List[RejectionLedgerEntry]`

## Phase 4: Agent Implementation (Pydantic AI Agents)

#### A. Strategist Agent (`agents/strategist.py`)
- [ ] **Create `agents/__init__.py`**
- [ ] **Create `agents/strategist.py`** – State space reduction
  - [ ] `Strategist` class inheriting from `Agent`
  - [ ] Tools: `get_course_data`, `analyze_workload_patterns`
  - [ ] Method: `analyze_and_prioritize(courses: List[CourseModel]) → ExecutionQueue`

#### B. Course Agent (`agents/course_agent.py`)
- [ ] **Create `agents/course_agent.py`** – Generator/Proposer
  - [ ] `CourseAgent` class inheriting from `Agent`
  - [ ] Tools: `get_course_data`, `check_temporal_availability`, `get_working_hours`, `get_rejection_history`
  - [ ] Method: `propose_slot(course: CourseModel) → ProposalModel`

#### C. Room Agent (`agents/room_agent.py`)
- [ ] **Create `agents/room_agent.py`** – Critic/Validator
  - [ ] `RoomAgent` class inheriting from `Agent`
  - [ ] Tools: `check_room_availability`, `validate_room_capacity`, `check_room_specialty`
  - [ ] Method: `validate_room(proposal: ProposalModel) → ValidationResult`

## Phase 5: Services Layer – Orchestration

#### A. Orchestrator (`services/orchestrator.py`)
- [ ] **Create `services/__init__.py`**
- [ ] **Create `services/orchestrator.py`** – Mediator & main loop
  - [ ] `Orchestrator` class managing agent instances
  - [ ] `initialize_agents(deps: AgentDependencies) → Dict[str, Agent]`
  - [ ] `run_scheduling_loop(courses: List[CourseModel]) → BlackboardState`
  - [ ] Reflexion logic: update ledger on failures, retry with feedback

## Phase 6: Application Bootstrap & Integration

#### A. Main Application (`main.py`)
- [ ] **Create `main.py`** – Application entry point
  - [ ] Initialize dependency container (`core/deps.py`)
  - [ ] Load mock data from `data/mock_registries.py`
  - [ ] Create orchestrator instance
  - [ ] Run scheduling loop with sample courses
  - [ ] Output final schedule or failure analysis

#### B. Configuration (`config/`)
- [ ] **Create `config/__init__.py`**
- [ ] **Create `config/settings.py`** – Environment-specific settings
  - [ ] LLM API keys (from environment variables)
  - [ ] Timeout configurations
  - [ ] Logging setup

## Phase 7: Testing & Validation
*(To be implemented after core functionality)*
- [ ] Unit tests for deterministic tools
- [ ] Integration tests for agent coordination
- [ ] End-to-end tests with mocked LLM responses
- [ ] Performance testing with larger datasets

## Phase 8: Documentation & Polish
- [ ] API documentation (docstrings)
- [ ] User guide for running the scheduler
- [ ] Deployment instructions
- [ ] Performance optimization if needed

---

## Development Workflow Instructions:
1. **Follow the phase order strictly** – Each phase depends on the previous
2. **Implement schemas first** – All other components need these models
3. **Build tools before agents** – Agents depend on injected tools
4. **Test incrementally** – Verify each component before moving to dependent ones
5. **Use dependency injection** – All agents get dependencies via `core/deps.py`

**Next Action:** Start with Phase 1A: Create `schemas/communication.py` with `ProposalModel`, `ValidationResult`, etc.
