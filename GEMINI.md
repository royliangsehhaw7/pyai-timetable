# GEMINI.md — Adaptive School Scheduler

This project is a multi-agent system built with **Pydantic AI** designed to autonomously generate valid, conflict-free weekly school timetables.

## Project Overview
The **Adaptive School Scheduler** uses a Supervisor/Manager Orchestration pattern. An Orchestrator agent proposes timetable slots, which are then validated by a suite of specialized agents (Critique and Specialist) before being committed.

### Core Technologies
- **Framework:** [Pydantic AI](https://ai.pydantic.dev/)
- **LLM:** Google Gemini
- **Integrations:** Google Calendar via MCP (Post-generation), Telegram Bot (Phase 2 query interface)
- **Language:** Python 3.12+

## Architecture & Logic
The system follows a strict **Silo Rule**: Agents do not have shared context or direct communication. The Orchestrator acts as the central hub, carrying rejection context forward to negotiate a valid schedule.

### Agents
| Agent | Role | Responsibility |
|---|---|---|
| **Orchestrator** | Supervisor | Proposes slots, manages negotiation loop, finalizes timetable. |
| **School Policy** | Critique | Validates school hours and lunch blocks. |
| **Academic Dean** | Specialist | Validates course hour requirements. |
| **Registrar** | Specialist | Validates room availability and suitability. |
| **Faculty Head** | Specialist | Validates lecturer availability and specialties. |

## Current Status: Implementation In Progress
The project is currently in the **Implementation** phase.
- [x] Architecture & Design Finalized (`DESIGN.md`)
- [x] Environment Setup (Python venv & Libraries)
- [x] Implement `data/` (Mock registries)
- [x] Implement `schemas/` (Pydantic models)
- [ ] Implement `core/` (Logging & Dependencies)
- [ ] Implement `utilities/` (LLM Factory)
- [ ] Implement Agents & Tools
- [ ] Implement `workflows/` (Orchestration loop)

## Planned Structure
```text
adaptive_school_scheduler/
├── agents/             # Agent definitions and system prompts
├── tools/              # Tool functions and MCP instances
├── schemas/            # Pydantic models (ScheduledClass, WeeklyTimetable, etc.)
├── data/               # Mock data registries (courses, rooms, lecturers)
├── core/               # Shared dependencies and logging configuration
├── workflows/          # Orchestration loop (SchedulingService)
└── utilities/          # LLM factory and provider abstractions
```

## Building and Running
*Note: Implementation is ongoing. Commands below are placeholders.*

### Setup
1. Create a virtual environment: `python -m venv venv`
2. Install dependencies: `pip install pydantic-ai python-dotenv` (TODO: Create requirements.txt)
3. Configure environment: Create a `.env` file with `GEMINI_API_KEY`.

### Running
- **Start Scheduler:** `python app.py` (Planned entry point)

## Development Conventions
- **Latest Documentation Mandate:** When implementing Pydantic AI features (agents, tools, dependencies), you MUST always refer to the [official Pydantic AI documentation](https://pydantic.dev/docs/ai/) for the latest syntax and terminology. For example, use `output_type` for structured agent results, as older parameters like `result_type` are deprecated or replaced.
- **Strict Execution Policy:** DO NOT generate proposed code, implementation, or file content unless specifically and explicitly directed to do so by the user.
- **Clean Architecture:** Strict separation between agents, tools, and business logic.
- **Logging:** First-class citizen via `core/logging.py`.
- **Token Usage Tracking:** Cumulative token usage MUST be tracked across all agent calls using the `GlobalUsage` class in `core/deps.py`.
- **Patterns:** Factory pattern for agents; Dependency Injection for services.
- **No Globals:** Tools passed via `tools=[]` in constructors; configuration via `.env` and `os.getenv()`.
