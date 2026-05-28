# INDEX.md

## Purpose of this document

Provide the reading order for the project documentation, explain what each document is for, and prevent implementation from drifting ahead of the system model.

This file is the front door to the docs set. New contributors, AI coding agents, and future maintainers should start here before touching code.

---

## Reading order

### 1. Core project intent and workflow truth

Read these first to understand what the system is trying to do and how the workflow actually operates.

1. `PROJECT_BRIEF.md`
   - High-level problem, target users, operating environment, and what success looks like.

2. `BOOTSTRAP_QUESTIONNAIRE.md`
   - Structured project-definition baseline used to rebuild the docs set from first principles.
   - Helps expose hidden assumptions, workflow edges, and design commitments before coding.

3. `WORKFLOW_TIMELINE.md`
   - Step-by-step lifecycle of a run from creation through publish and controlled re-entry.

4. `DATA_MODEL.md`
   - Canonical entities, key fields, ownership, and relationships.

5. `STATE_CLASSIFICATION.md`
   - What is working state, what is derived state, and what is immutable evidence.

---

### 2. Architecture and decision frame

Read these next to understand what architectural choices have been made and why.

6. `ARCHITECTURE_SELECTION.md`
   - Options considered and the recommended architecture direction.
   - Captures the current stance: workflow-governed Python core, thin presentation layer, persisted truth, immutable publish artifacts, revision-aware re-entry.

7. `ASSUMPTIONS_AND_OPEN_QUESTIONS.md`
   - Tracks what is still being assumed, what has already been resolved, and what remains open.

8. `ADR/ADR-0001 - Use a Thin Presentation Layer with Shared-Storage Deployment as the Near-Term Baseline.md`
   - Current UI/deployment baseline.

9. `ADR/ADR-0002 - Persist Mutable Working State with Version-Aware Rehydration and Keep Published Evidence Separate.md`
   - Persistence, versioning, and rehydration expectations.

10. `ADR/ADR-0003-concurrency-model-single-editor-lock.md`
    - Locking, handoff, timeout, and override policy.

11. `ADR/ADR-0004-published-revision-reentry-policy.md`
    - Immutable publish and reopen-by-new-working-revision policy.

12. `ADR/ADR-0005 - Use Password-Only Admin Challenges as a Near-Term Protected-Action Bootstrap.md`
    - Near-term admin challenge and protected-action constraints.

13. `ADR/ADR-TEMPLATE.md`
    - Template for future architectural decisions.

---

### 3. Build discipline, verification, and release control

Read these before implementation or review work.

14. `AGENTS.md`
    - Project-specific coding rules and documentation-first implementation discipline for coding agents.

15. `TEST_STRATEGY.md`
    - Testing philosophy, required regression surfaces, and critical lifecycle paths.

16. `QUALITY_GATES.md`
    - Minimum gates for merge, acceptance, and release confidence.

---

### 4. Failure memory and project learning

Read these before changing workflow, persistence, routing, publish, or review behavior.

17. `FAILURE_CATALOG.md`
    - Known failure modes, root-cause patterns, detection gaps, and prevention rules.

18. `RETROSPECTIVE.md`
    - Lessons learned from prior failure patterns, documentation drift, retrofit mistakes, and what must be done differently going forward.

---

### 5. Orientation / repo front door

These help a new person understand the repo quickly after the governing docs above.

19. `README.md`
    - Human-readable summary of the project, architecture stance, workflow, and repo purpose.

---

## How to use this docs set

### If you are planning work from scratch

Read the full set in the listed order.

### If you are changing code in an existing workflow area

At minimum, read:
- `INDEX.md`
- `PROJECT_BRIEF.md`
- `WORKFLOW_TIMELINE.md`
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`
- relevant ADRs
- `TEST_STRATEGY.md`
- `QUALITY_GATES.md`
- `FAILURE_CATALOG.md`
- `RETROSPECTIVE.md`

### If you are fixing a bug

Do not jump straight into code. First identify:
- the expected behavior from docs
- the actual commit boundary
- whether the defect is in UI state, working state, persistence, rehydration, routing, lifecycle transitions, or evidence handling
- what regression test proves the repair

### If you are proposing a new feature

Do not implement it until you can answer:
- what entity or state it belongs to
- who owns it
- whether it is working, derived, or evidence state
- what workflow step creates or edits it
- what tests and quality gates must expand to cover it

---

## Document roles summary

| Document | Role |
|---|---|
| `PROJECT_BRIEF.md` | What the system is for |
| `BOOTSTRAP_QUESTIONNAIRE.md` | Structured design baseline |
| `WORKFLOW_TIMELINE.md` | How the lifecycle works |
| `DATA_MODEL.md` | What the core things are |
| `STATE_CLASSIFICATION.md` | What kind of state each thing is |
| `ARCHITECTURE_SELECTION.md` | What architecture best fits the workflow |
| `ASSUMPTIONS_AND_OPEN_QUESTIONS.md` | What is assumed / unresolved |
| `ADR-*` | Accepted key decisions |
| `AGENTS.md` | Implementation discipline |
| `TEST_STRATEGY.md` | What must be tested |
| `QUALITY_GATES.md` | What must be true before merge/release |
| `FAILURE_CATALOG.md` | What has gone wrong and how not to repeat it |
| `RETROSPECTIVE.md` | Broader lessons learned |
| `README.md` | Concise project overview |

---

## Notes for contributors and coding agents

- Do not treat the docs as decorative.
- If the docs and code disagree, surface the conflict.
- If the docs are incomplete for a risky change, fix the docs first.
- If a new lesson emerges from implementation or debugging, update the appropriate doc instead of leaving that knowledge trapped in chat, PR text, or memory.
