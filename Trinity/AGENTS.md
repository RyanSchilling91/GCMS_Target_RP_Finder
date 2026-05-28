AGENTS.md
This file is the primary contract of engagement for all coding agents working in this repository.
It applies to the entire codebase and governs planning, implementation, documentation, testing, and failure response.

Mission
This repository exists to guide the development of enterprise-grade, workflow-governed software using AI as a primary coding engine.
Software produced under these rules must be:

Modular and maintainable
Testable with clear separation between UI and business logic
Auditable and reproducible where required
Safe for regulated, restricted, or professional environments
Understandable by future engineers who did not build the system
Resistant to architectural drift as features expand
Resistant to silent regression caused by state confusion, persistence confusion, or UI-driven logic shortcuts

Agents must treat these goals as the operating philosophy behind every implementation decision.

Core Project Stance
This project is not "a UI app with some helper modules."
It is a workflow-governed application core with a presentation layer rendered through the chosen UI framework.
That distinction matters:

The UI must remain replaceable.
Workflow logic, persistence rules, routing logic, publish controls, lock handling, review ownership, and evidence semantics must not be owned by the UI layer.


Docs-First Rule (Mandatory)
Before making any code change, debugging a workflow, recommending architecture, or proposing changes related to persistence, session state, routing, concurrency, review, publish, reopen, or locking behavior, the agent must:

Read docs/INDEX.md first.
Follow the reading order and document purpose defined there.
Read the minimum governing docs required for the task before inspecting or editing code.
Interpret the request through the docs before proposing implementation.
State in the response which docs were read and what constraints they impose on the change.

If the docs are missing, weak, contradictory, or no longer match the codebase — stop and call that out. Do not guess. Do not patch around documentation gaps silently.
Minimum Docs by Task Type
For implementation or debugging in workflow areas, read at minimum:

docs/INDEX.md
docs/PROJECT_BRIEF.md
docs/WORKFLOW_TIMELINE.md
docs/DATA_MODEL.md
docs/STATE_CLASSIFICATION.md
Relevant ADRs
docs/TEST_STRATEGY.md
docs/QUALITY_GATES.md

For changes affecting architecture, persistence, rehydration, routing, review flow, publish, reopen, locking, or protected actions — also read:

docs/ARCHITECTURE_SELECTION.md
docs/ASSUMPTIONS_AND_OPEN_QUESTIONS.md
docs/FAILURE_CATALOG.md
docs/RETROSPECTIVE.md

Prompt Contract
If the user says any of the following, treat it as a hard requirement:

"read the docs first"
"use docs/INDEX.md"
"docs-first"
"follow the docs folder before coding"

If the prompt is ambiguous, prefer the docs-first path.

Planning Rules (Mandatory Before Coding)
1. No feature implementation before the data model exists
Do not implement UI or workflow logic until the core data model is defined:

Core entities and fields
Field ownership (who creates/edits each)
Lifecycle state transitions
Persistence boundaries (working vs. derived vs. evidence)
Lineage and evidence boundaries

If this is unclear, do not guess — ask.
2. Define the workflow timeline first
Before implementing, describe the workflow as a step-by-step timeline:

Data enters the system
User edits working truth
System derives downstream outputs
Reviewer verifies governed artifacts
Publish freezes evidence
Re-entry creates a new working revision, not a mutation of published evidence

If the timeline is fuzzy, stop and clarify.
3. Separate editable state from evidence state
Explicitly classify all persisted information into:

Working State — mutable during normal workflow
Derived State — recomputable outputs, must not become source truth
Evidence State — frozen, immutable record

Do not write persistence code until this classification is declared and aligned with the docs.
4. Identify irreversible decisions
Before coding, list decisions that are expensive to change later:

UI stack
Persistence format
Deployment model
ID strategy
Review ownership and sign-off model
Concurrency assumptions
Auth/session approach
Reopen/revision policy

Pause and confirm these with the user before encoding them into implementation.
5. Detect retrofit risk
If a change touches persistence, review logic, workflow routing, or data interpretation and the UI already exists:

Warn that it is a retrofit-risk change.
Recommend modeling first.
Do not quietly patch around architecture gaps in UI code.

6. Pre-coding summary (required for non-trivial tasks)
Before proposing code, the agent must summarize:

Which docs were read and which constraints they impose
What is working truth, derived state, and evidence for this change
What is in scope and what is not
Which downstream surfaces are at risk (routing, save/resume, review, publish, reopen, locks, artifact integrity)
Whether the change is safe to implement without first updating docs
Which layer should own the fix: UI, service, domain, persistence, or docs


Architecture Rules
1. No monolith growth
Do not create or grow monolith files.
2. File size limits

Soft limit: 250 lines
Hard limit: 350 lines unless the user explicitly approves a justified exception

3. Split-first policy

If a touched file is over 250 lines, split before adding features when practical.
If a change would add more than 80 lines to one file, create or split modules first.
Prefer creating new files over appending large blocks to existing files.

4. Thin UI layer
UI files may only:

Render state
Collect input
Call service functions
Show results and operator feedback

UI files must not own:

Workflow state transitions
Persistence rules or schema logic
Lock decisions or lock lifecycle
Publish rules or reopen logic
Review authorization or independence rules
Artifact lineage
Run discovery logic
Scientific or domain business logic

5. Domain/service layer owns behavior
All meaningful workflow logic must live in service, domain, or helper modules that are testable without the UI runtime.
6. Derived state must not become source truth
Anything recomputable from committed working truth is derived state, even if cached.
7. Published evidence is immutable
Published artifacts are evidence. They must not be edited in place. Re-entry must create a new working revision derived from published evidence.
8. Routing must derive from persisted truth
The application must reopen to the correct workflow surface based on persisted truth and governed workflow state — not stale UI tab memory or convenience shortcuts.
9. Locking is a real architectural boundary
Single-editor lock ownership, heartbeat, timeout, and override behavior must be handled as governed system behavior, not casual UI affordances.
10. Architecture guardrail
Do not solve workflow, persistence, routing, publish/reopen, review ownership, or concurrency problems with UI-local patches unless the docs explicitly support that design. Prefer service/domain/persistence fixes over presentation-layer workarounds.

Technology Selection Rules

UI, persistence, deployment, auth/session, and concurrency design must be chosen explicitly and documented before implementation.
Do not treat any single stack as universal.
The agent may recommend a stack based on project constraints but must distinguish:

Mandatory requirements
Recommended patterns
Examples from prior successful projects


When the stack is not yet chosen, compare at least two plausible options and explain tradeoffs.
Prior successful patterns may be referenced but are not defaults unless the user selects them.

Proven pattern examples (not mandatory defaults):

Python service layer + Streamlit presentation layer for internal workflow tools
DuckDB, SQLite, or Postgres depending on concurrency, deployment, and audit needs
Packaged review/archive artifacts using a database snapshot + tabular exports + manifest


Persistence Design Rules

Persistence design must be chosen explicitly and documented before implementation.
Do not treat a single binary database file as sufficient archival evidence when the workflow requires sign-off, handoff, or defensible archive.
All persistence read/write logic belongs in service modules, not UI modules.
UI modules may trigger persistence actions but cannot contain schema or table logic.
Challenge attempts to permanently store data that can and should be recomputed.

Mandatory discovery before recommending persistence changes
Before proposing persistence changes, first locate and list:

Save function(s)
Load/rehydrate function(s)
Every UI or API entry point that calls them

Summarize exactly what each path currently writes and reads. Do not propose migrations or architecture changes until this is complete.
Review/archive package standard
When a workflow requires sign-off, handoff, or defensible archive, prefer a publishable package that includes:

Working-state snapshot (database or equivalent)
Tabular exports of key data
manifest.json containing: app_version, schema_version, storage-engine version, created_at / modified_at, file hashes

Versioning and migration standard

Persist explicit schema_version — never rely only on implicit schema shape.
Persist app_version and storage-engine version in durable metadata when applicable.
Implement forward migrations as discrete steps (vN → vN+1) with documented fallback behavior.
If loading a newer unsupported schema, fail safely with clear operator guidance.

Audit and integrity standard

Use append-only event or audit records for key actions where traceability matters.
Event rows must include actor, timestamp, event type, and structured details.
Signature or sign-off events must be durable in persisted state, not only in volatile session memory.

Concurrency and handoff standard

If review is sequential, enforce single-writer expectations and handoff by immutable published package or equivalent controlled state.
If simultaneous editing is possible, define merge strategy up front (locking, optimistic concurrency, branches, or conflict policy).
Never assume safe concurrent writes without explicitly validating the chosen persistence model.


Testing Rules
1. Regression coverage targets real failure surfaces
Tests must target actual workflow failures, including:

Create new
Step 1 save/reopen
Navigation away and back
Upload/match rebuild behavior
Routing after reopen
Publish/reopen lineage
Lock acquisition, release, timeout, and override
Review claim independence

2. Protect save boundaries
Where explicit save behavior is part of the workflow contract, test both:

Active working-state behavior before save
Durable persisted behavior after save

3. Protect critical lifecycle paths
At minimum, tests must cover:

Create new
Continue draft
Ready-for-review claim
In-review behavior
Needs-rework return
Approved
Publish
Reopen from published into a new working revision

4. Keep bounded tests honest
Do not overclaim end-to-end proof if the test only validates a helper seam. "We'll test manually" is not sufficient for core business logic.
5. Bug fixes require regression tests
No non-trivial workflow bug fix is complete without targeted regression coverage. If a test cannot be added, the reason must be documented.

Anti-Failure Rules
These were learned from real defects in this project. They are not suggestions.

Do not let UI buffers silently become authoritative. If visible editor state and committed working-state can diverge, that is a defect risk and must be handled explicitly.
Do not persist action-widget state as durable truth. Buttons, route requests, open/view flags, and form submit keys must never become part of durable run truth.
Do not let routing depend on remembered page state. Continue/reopen behavior must derive from persisted workflow artifacts and current governed state.
Do not blur active in-session state and durable saved state. If the workflow has an explicit save boundary, preserve it. Do not accidentally autosave where the workflow contract requires explicit commit.
Do not treat publish and reopen as simple status flips. They are lineage and evidence operations, not just route changes.
Do not fix a bug only at the most visible UI seam. Check the persistence layer, route logic, save path, rehydration path, and artifact model for the same defect class.
Do not trust passing tests that miss the real user path. Tests must reflect the actual workflow path, not only helper-level behavior.
Do not claim confidence if runtime validation did not occur. If browser/runtime or dependency-complete verification did not happen, say so directly.


Failure Documentation Rule (Mandatory)
When a bug, regression, unexpected behavior, or architecture defect is discovered and corrected, the agent must update the project learning records before declaring the task complete.
Required actions:

Add an entry to docs/FAILURE_CATALOG.md.
If the issue reveals a repeatable process weakness, also propose an improvement in docs/RETROSPECTIVE.md and a rule update to AGENTS.md when appropriate.
If the issue required code changes, add a regression test whenever feasible.

Failure documentation is part of the fix itself, not optional cleanup.

Contradiction Rule
If two docs conflict, do not silently choose one and continue coding. Stop, identify the conflict, and recommend which documentation decision must be resolved first.

Assumption Blocking Rule
The agent must not silently choose behavior when multiple interpretations exist. It must present the interpretations and ask the user to select one before implementing.

Production Delivery Mode
If the user states the app is in production and does not want immediate code changes, default to:

Fact-finding
Risk assessment
Instruction and process improvements

Do not modify production app code unless explicitly requested after the assessment.

Implementation Style Rules

Prefer explicit names over clever names.
Prefer small pure/helper functions where possible.
Keep contracts visible.
Validate inputs at system and layer boundaries.
Fail loudly and operator-visibly on invalid workflow actions.
Preserve backward-compatible migrations where the docs require them.
Add comments where the workflow contract is non-obvious, but do not narrate trivial code.


What an Agent Must Never Do

Never encode a new architecture assumption without checking the docs.
Never move business logic into the UI layer for convenience.
Never mutate published evidence in place.
Never bypass reviewer independence rules.
Never silently change save semantics.
Never ignore lock semantics when a change touches working revisions.
Never describe a defect as fixed unless bounded regression actually proves the claimed contract.
Never treat the latest patch as authoritative if it conflicts with the docs set.
Never run destructive git commands unless explicitly requested.
Never revert unrelated user changes.


Required Document Set
The following docs govern this project. Agents treat incomplete planning files as blocking conditions for architectural work. Implementation may proceed only after minimum sections are present or explicitly deferred by the user.
docs/PROJECT_BRIEF.md

Problem being solved
Intended users
Non-goals
Operational constraints
Success criteria

docs/WORKFLOW_TIMELINE.md

Stepwise lifecycle from intake to completion
User actions and system actions
Review/sign-off points
Freeze/archive points

docs/DATA_MODEL.md

Entities, fields, and field ownership
Valid state transitions
Invariants and forbidden states

docs/STATE_CLASSIFICATION.md

Working State, Derived State, Evidence State
Persistence boundary for each category

docs/ARCHITECTURE_SELECTION.md

Core requirements affecting architecture
UI, persistence, deployment, auth/session, and concurrency options considered
Recommended direction and deferred decisions

docs/ADR/ (one file per irreversible decision)
Each ADR must contain: Decision, Context, Alternatives considered, Why chosen, Consequences.
Trigger an ADR when decisions affect: UI stack, persistence format, identifiers, sign-off behavior, concurrency, audit model, deployment model, or auth/session model.
docs/ASSUMPTIONS_AND_OPEN_QUESTIONS.md

Assumption, Risk if wrong, Who resolves it, Decision deadline or trigger

docs/TEST_STRATEGY.md

Unit test targets, regression scenarios, required fixtures, definition of correctness

docs/QUALITY_GATES.md

What must pass before merge/release, migration verification, rollback capability, artifact validation

docs/FAILURE_CATALOG.md
Each entry: Symptom, Root cause, Detection gap, Prevention rule
docs/RETROSPECTIVE.md

What worked, what failed, what to standardize, what rule should be added or modified in AGENTS.md


Preferred Output Format for Non-Trivial Coding Tasks
When reporting completed work, use this structure:

Expected behavior from docs
Exact reproduction scenario or bounded contract under repair
Root cause
Files changed
Tests added or updated
What is now proven
Remaining risks or unverified surfaces

This keeps code work aligned with the repository's documentation-first operating model.

Living Document Rule
This file is a living contract. When patterns repeat, when new failure classes emerge, or when a process weakness is identified, the agent must propose targeted additions or amendments to this file as part of the fix. The document should grow smarter with the project, not remain static.