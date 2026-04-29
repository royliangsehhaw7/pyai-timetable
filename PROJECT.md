# PROGRESS.md — Adaptive School Scheduler

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
