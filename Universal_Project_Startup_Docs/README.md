# Universal Project Startup Docs Kit

This folder is a reusable project-start framework for AI-assisted software development.

It exists to prevent:
- hallucinated requirements
- spaghetti code
- UI-owned business logic
- stale derived state
- unsafe persistence changes
- weak testing claims
- forgotten failure lessons

## Operating intent
Inject this folder into every new project before coding begins. Fill the project-specific files, record major decisions in ADRs, then let AI coding agents work inside the documented boundaries.

After the project ends or after a major incident, generalize the lessons back into this kit so the next project starts stronger.

## Fixed framework files
These files define the reusable method and should remain mostly stable:
- `INDEX.md`
- `AGENTS.md`
- `BOOTSTRAP_QUESTIONNAIRE.md`
- `QUALITY_GATES.md`
- `FAILURE_CATALOG.md`
- `RETROSPECTIVE.md`
- `ADR/ADR-TEMPLATE.md`

## Project-specific files to fill each time
These must be completed or explicitly deferred for each project:
- `PROJECT_BRIEF.md`
- `WORKFLOW_TIMELINE.md`
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`
- `ARCHITECTURE_SELECTION.md`
- `ASSUMPTIONS_AND_OPEN_QUESTIONS.md`
- `TEST_STRATEGY.md`
- project-specific ADRs under `ADR/`

## Use pattern
1. Start with `BOOTSTRAP_QUESTIONNAIRE.md`.
2. Fill `PROJECT_BRIEF.md`.
3. Fill `WORKFLOW_TIMELINE.md`.
4. Fill `DATA_MODEL.md`.
5. Fill `STATE_CLASSIFICATION.md`.
6. Complete `ARCHITECTURE_SELECTION.md`.
7. Record accepted architecture choices as ADRs.
8. Complete `TEST_STRATEGY.md` and `QUALITY_GATES.md`.
9. During development, update `FAILURE_CATALOG.md` and `RETROSPECTIVE.md` as part of the work, not afterthought cleanup.

## Core rule
Clarity before code. Structure before speed. Evidence before confidence.
