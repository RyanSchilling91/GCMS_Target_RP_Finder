# Docs Index — Required Agent Entrypoint

## Purpose
This file is the required entrypoint for any AI agent, assistant, or developer working on the project.

The docs are the planning source of truth. The code is the implementation. If the code and docs conflict, stop and identify the conflict before changing behavior.

## Mandatory reading order
For debugging, new features, refactors, architecture, persistence, locking, permissions, sessions, deployment, UI behavior, release readiness, or production incidents, read in this order:

1. `AGENTS.md`
2. `PROJECT_BRIEF.md`
3. `WORKFLOW_TIMELINE.md`
4. `ARCHITECTURE_SELECTION.md`
5. ADRs in `ADR/`
6. `DATA_MODEL.md`
7. `STATE_CLASSIFICATION.md`
8. `ASSUMPTIONS_AND_OPEN_QUESTIONS.md`
9. `TEST_STRATEGY.md`
10. `QUALITY_GATES.md`
11. `FAILURE_CATALOG.md`
12. `RETROSPECTIVE.md`

## Guided fill status labels
Use these labels when evaluating each planning file:
- **Complete** — enough detail to guide implementation.
- **Present but weak** — direction exists but risk remains.
- **Missing / blocking** — do not make architectural or risky implementation changes.

## Task fast-paths
After reading the core order above, focus especially on these docs:

### New project or architecture recommendation
- `PROJECT_BRIEF.md`
- `WORKFLOW_TIMELINE.md`
- `ARCHITECTURE_SELECTION.md`
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`

### UI or workflow implementation
- `WORKFLOW_TIMELINE.md`
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`
- relevant ADRs

### Persistence, migrations, schema, metadata, recovery
- `ARCHITECTURE_SELECTION.md`
- persistence ADRs
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`
- `TEST_STRATEGY.md`
- `FAILURE_CATALOG.md`

### Auth, users, roles, sessions, permissions
- `PROJECT_BRIEF.md`
- `ARCHITECTURE_SELECTION.md`
- auth/session ADRs
- `DATA_MODEL.md`
- `TEST_STRATEGY.md`

### Concurrency, locking, collaboration, handoff
- `ARCHITECTURE_SELECTION.md`
- locking/concurrency ADRs
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`
- `FAILURE_CATALOG.md`

### Debugging and regression fixes
- `FAILURE_CATALOG.md`
- `RETROSPECTIVE.md`
- `TEST_STRATEGY.md`
- `QUALITY_GATES.md`
- affected planning docs

## Blocking rule
If a required planning file is missing, weak, or mostly blank, the agent must identify the missing surface and either:
1. guide the user to fill it, or
2. record an explicit deferral with risk in `ASSUMPTIONS_AND_OPEN_QUESTIONS.md`.

The agent must not silently invent requirements.

## Completion rule
A task is not complete unless implementation, tests, and docs agree.
