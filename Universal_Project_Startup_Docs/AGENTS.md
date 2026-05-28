# AGENTS.md — AI Coding Agent Rules

## Mission
Build professional-grade, maintainable, auditable software with AI as a coding partner without allowing the AI to invent the architecture.

The agent must optimize for:
- modularity
- testability
- traceability
- explicit state ownership
- thin presentation layers
- durable persistence boundaries
- clear recovery and release criteria
- prevention of repeated failure patterns

## Non-negotiable startup behavior
Before coding, the agent must read `INDEX.md` and follow the required reading order.

If the project is new or architecture is not settled, the agent must help complete the planning docs before implementation.

## Planning gates before implementation
The following must exist or be explicitly deferred before risky code begins:

1. **Project brief** — problem, users, scope, non-goals, constraints, success criteria.
2. **Workflow timeline** — chronological real-world sequence from intake to completion.
3. **Data model** — entities, fields, ownership, identifiers, lifecycle states, invariants, forbidden states.
4. **State classification** — working, derived, and evidence state separated.
5. **Architecture selection** — UI, persistence, deployment, auth/session, and concurrency options compared.
6. **ADRs** — irreversible choices recorded.
7. **Test strategy** — unit, integration, regression, fixture, migration, and edge-case plan.
8. **Quality gates** — objective completion/release bar.

## Architecture rules
1. UI files are presentation only: layout, widget wiring, display, and calls to services.
2. Business rules live in domain/service modules, not UI files.
3. Persistence/schema logic lives in persistence modules, not UI files.
4. Parsing/import logic lives in parser modules, not UI files.
5. Validation and authorization rules must not depend on a specific UI framework.
6. The UI framework should be replaceable without rewriting the core workflow.
7. Do not create or grow monolith files.
8. Soft file limit: 250 lines. Hard file limit: 350 lines unless justified and accepted.
9. Prefer small focused modules over appending large blocks to existing files.

## State rules
1. Working state is mutable and resumable.
2. Derived state is recomputable and must not become hidden source truth.
3. Evidence state is frozen, versioned, publishable, or defensible.
4. Do not persist derived values permanently unless the docs justify why this is safe.
5. Published/evidence data must never be silently overwritten.
6. Reopen/rework flows must create a new working revision or superseding record, not mutate evidence in place.

## Persistence rules
Before changing persistence, the agent must locate and summarize:
- save functions
- load/rehydrate functions
- schema/migration functions
- every UI/API entry point that calls them
- exactly what each path writes and reads

The agent must not propose migrations or storage changes until this discovery is complete.

Persistence design must document:
- source of truth
- schema versioning
- migration behavior
- unsupported-newer-version behavior
- backup/recovery expectations
- artifact/evidence expectations
- concurrency assumptions

## Concurrency and locking rules
1. Do not assume safe concurrent writes.
2. Define the collaboration model explicitly: single writer, record lock, optimistic concurrency, branch/merge, or immutable handoff.
3. Separate host/process locking from record edit locking.
4. Record locks need owner, timestamp, heartbeat/expiry or explicit release behavior.
5. Stale lock behavior must be documented and tested.

## Audit and evidence rules
When traceability matters, key actions should create append-only audit/event records with:
- actor
- timestamp
- event type
- target record
- structured details

Sign-off, publish, reopen, restore, migration, role/permission changes, and destructive actions must be durable events, not volatile session state.

## Review / archive package rule
When a workflow requires sign-off, handoff, or defensible archive, prefer a publishable package appropriate to the project. It may include:
- working-state snapshot
- tabular exports
- rendered reports
- manifest with app version, schema version, created timestamp, file hashes, and package contents

Exact contents must be documented in project docs or ADRs.

## Testing rules
1. New business rules require automated tests.
2. Bug fixes require regression tests whenever feasible.
3. Core logic cannot rely only on manual testing.
4. Tests must include realistic persisted-state and edge-case fixtures, not only happy paths.
5. If a regression test cannot be added, document why in `TEST_STRATEGY.md` or the fix summary.

## Failure catalog rule
When a bug, regression, unexpected behavior, or architecture defect is discovered and corrected, the fix is incomplete until:
1. `FAILURE_CATALOG.md` has symptom, root cause, detection gap, and prevention rule.
2. A regression test is added or the reason is documented.
3. If the issue reveals process weakness, `RETROSPECTIVE.md` proposes a standard/rule update.
4. If needed, `AGENTS.md` or a project ADR is updated.

## Architecture selection rules
1. Do not treat prior project stacks as universal defaults.
2. Compare at least two plausible options for UI, persistence, deployment, auth/session, and concurrency when not already decided.
3. Clearly separate mandatory requirements, recommendations, and prior successful patterns.
4. Record accepted irreversible decisions as ADRs.

## Assumption blocking rule
The agent must not silently choose behavior when multiple valid interpretations exist.

If uncertainty affects architecture, persistence, security, workflow correctness, auditability, or release behavior, log it in `ASSUMPTIONS_AND_OPEN_QUESTIONS.md` and ask for resolution or explicit deferral.

## Production safety rules
1. Do not run destructive commands unless explicitly requested.
2. Do not revert unrelated user changes.
3. Do not modify production code when the user asked for assessment only.
4. In production mode, prioritize fact-finding, risk assessment, and process improvements before code edits.
5. Keep changes scoped and reversible.

## End-of-task report
The agent must report:
- files changed/created
- why each changed
- tests run and results
- docs updated
- known risks or deferrals
- whether quality gates are met
