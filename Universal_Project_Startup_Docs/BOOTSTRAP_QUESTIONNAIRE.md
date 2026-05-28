# Bootstrap Questionnaire — AI-Guided Project Intake

## Purpose
This is the entry point for new projects. It turns a vague idea into enough documented structure to let AI agents code safely.

The goal is not speed. The goal is to prevent architectural drift, hidden assumptions, and premature coding.

## Agent rules
1. Do not start coding in this phase.
2. Work in phases.
3. Classify each phase as Complete, Present but weak, or Missing / blocking.
4. Guide the user with examples when needed.
5. Do not assume. Log uncertainty.
6. Map each phase to the document it feeds.

## Phase 1 — Project purpose
Target: `PROJECT_BRIEF.md`

Ask:
- What problem are we solving?
- Who are the users?
- What do they do today without this tool?
- What is painful, slow, risky, inconsistent, or hard to audit?
- What decision/workflow/control point should this tool improve?
- What is out of scope for version 1?
- What would prove the project worked?

Output check:
- problem clarity
- user clarity
- scope boundaries
- measurable success criteria

## Phase 2 — Workflow reality
Target: `WORKFLOW_TIMELINE.md`

Ask:
- What enters the system first?
- Where does it come from?
- Who touches it first?
- What happens next, step by step?
- Which steps are manual?
- Which are automated?
- Where do decisions happen?
- What gets reviewed?
- Who approves or rejects?
- What leaves the system at the end?

Output check:
- clear start
- clear sequence
- human vs system actions separated
- review and end state defined

## Phase 3 — Data model / truth layer
Target: `DATA_MODEL.md`

Ask:
- What are the main entities?
- What identifies each entity?
- What fields does each entity have?
- Which fields are required?
- Who owns each field: user, system, reviewer, external source?
- Which fields change over time?
- What lifecycle states are valid?
- What states must never happen?

Output check:
- entities defined
- ownership assigned
- identifiers clear
- lifecycle states logical
- forbidden states captured

## Phase 4 — State classification
Target: `STATE_CLASSIFICATION.md`

Ask:
- What is editable working state?
- What can be recomputed as derived state?
- What must become immutable evidence state?
- What survives refresh, restart, reprocessing, publication, and archive?
- What may be overwritten, versioned, superseded, or reconstructed?

Output check:
- no duplicated truth
- derived data not casually persisted
- evidence protected from silent overwrite

## Phase 5 — Architecture selection
Target: `ARCHITECTURE_SELECTION.md` and ADRs

Ask before suggesting tools:
- single-user or multi-user?
- simultaneous users?
- local, on-prem, cloud, offline, or hybrid?
- browser, desktop, API, or mixed?
- restricted IT environment?
- auditability requirements?
- expected data size and performance needs?
- recovery and retention needs?

Then compare options for:
- UI layer
- persistence
- deployment
- auth/session
- concurrency/collaboration

Output check:
- no default stack assumption
- tradeoffs compared
- recommendation justified
- ADR candidates identified

## Phase 6 — Assumptions and unknowns
Target: `ASSUMPTIONS_AND_OPEN_QUESTIONS.md`

Ask:
- What are we assuming?
- What could break if wrong?
- Who can resolve it?
- What needs validation?
- What is intentionally deferred?

Output check:
- assumptions explicit
- risks real
- unknowns tracked
- architecture-affecting unknowns resolved or deferred

## Phase 7 — Verification and completion
Target: `TEST_STRATEGY.md` and `QUALITY_GATES.md`

Ask:
- What absolutely must work?
- What edge cases matter?
- What failure would be unacceptable?
- What fixtures are needed?
- What must pass before merge/release?
- What rollback or recovery path is required?

Output check:
- tests concrete
- completion criteria measurable
- release bar objective

## Readiness statement
Before coding begins, the agent must state whether the project is ready:

- PROJECT_BRIEF: Complete / Present but weak / Missing
- WORKFLOW_TIMELINE: Complete / Present but weak / Missing
- DATA_MODEL: Complete / Present but weak / Missing
- STATE_CLASSIFICATION: Complete / Present but weak / Missing
- ARCHITECTURE_SELECTION: Complete / Present but weak / Missing
- ASSUMPTIONS_AND_OPEN_QUESTIONS: Complete / Present but weak / Missing
- TEST_STRATEGY: Complete / Present but weak / Missing
- QUALITY_GATES: Complete / Present but weak / Missing

If any are weak or missing, block or explicitly defer before coding.
