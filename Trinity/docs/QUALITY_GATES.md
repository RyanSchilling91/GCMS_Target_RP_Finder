# QUALITY_GATES.md

## Purpose of this document
Define the minimum quality gates required before a change can be considered safe to merge, safe to hand off, or safe to release.

The goal is not perfection. The goal is to prevent the project from reintroducing known workflow, persistence, routing, publish, and audit failures through overly narrow fixes or documentation drift.

---

## Guided fill status
- Status: Updated
- Last reviewed by: project owner + AI
- Last updated: 2026-03-24

---

## Gate categories
This project uses three practical gate levels:

1. **Change gate**
   - Minimum bar before a bug fix or bounded feature change is considered acceptable.

2. **Merge gate**
   - Minimum bar before the branch should be merged into the main working line.

3. **Release / hardening gate**
   - Minimum bar before the system should be treated as operationally trustworthy for governed workflow use.

---

## 1. Change gate
A non-trivial change should not be considered complete unless all of the following are true:

### Contract gate
- The expected behavior is grounded in the docs set, not only inferred from code.

### Scope gate
- The change is clearly bounded.
- The report states what was in scope and what was not.

### State-boundary gate
- The change identifies whether it touches:
  - working state
  - derived state
  - evidence state
  - active UI/editor state
  - explicit save boundaries
  - route derivation
  - lock behavior
  - review status logic
  - publish/reopen lineage

### Regression gate
- At least one targeted regression exists for the actual failing path or contract being repaired.

### Documentation gate
- If the defect revealed a missing rule, missing failure memory, or changed workflow expectation, the relevant docs are updated.

### Honesty gate
- Any unverified runtime surfaces are stated plainly.

---

## 2. Merge gate
Do not merge unless all of the following are true:

### A. Documentation alignment
The change is consistent with:
- `PROJECT_BRIEF.md`
- `BOOTSTRAP_QUESTIONNAIRE.md`
- `WORKFLOW_TIMELINE.md`
- `DATA_MODEL.md`
- `STATE_CLASSIFICATION.md`
- relevant ADRs
- `TEST_STRATEGY.md`
- `FAILURE_CATALOG.md`

If the change conflicts with those docs, either update the docs first or stop and surface the conflict.

### B. No architectural backsliding
The change must not:
- move business logic into the UI for convenience
- let derived state become hidden source truth
- mutate published evidence in place
- bypass lock semantics
- bypass reviewer independence
- rely on remembered page state instead of persisted truth
- quietly change explicit save behavior without documentation and tests

### C. Regression protection
At least the affected workflow surface must be covered by tests appropriate to the change:
- unit tests for pure logic
- integration tests for state/persistence/routing behavior
- workflow regressions for real defect paths

### D. Operator-visible failure handling
If the change introduces or touches invalid workflow actions, they must fail visibly rather than silently.

### E. No unresolved merge artifacts or drift markers
The codebase and docs must be free of:
- merge conflict markers
- contradictory temporary comments
- stale TODO logic that changes behavior
- duplicate route sources of truth

---

## 3. Release / hardening gate
Before a release is treated as operationally trustworthy, all of the following should be true:

### Workflow lifecycle gate
The system has passing or otherwise validated coverage for the critical lifecycle:
- create new
- Step 1 save/reopen
- upload/match
- continue draft routing
- submit for review
- review claim
- needs rework
- approved
- publish
- reopen from published into a new working revision

### Persistence gate
- Working truth persists correctly
- Rehydration is deterministic
- Supported versions load correctly or fail clearly
- Canonical restore behavior is preserved for governed fields and sentinel values

### Routing gate
- Continue/reopen routing derives from persisted truth
- Stale UI route memory does not control reopening

### Concurrency gate
- Single-editor lock lifecycle is validated
- Stale timeout is validated
- Override path is validated
- Conflicting opens fail visibly
- Reviewer claim rules enforce independence

### Publish/evidence gate
- Publish produces the required immutable evidence package
- Required artifacts are present
- Published artifacts remain unchanged after publish
- Reopen creates a new working revision instead of mutating evidence in place
- Lineage metadata is preserved

### Review/control gate
- Reviewer independence rules are enforced
- Protected actions require the governed challenge path
- Actor and reason logging exists where required

### Documentation gate
- Core docs reflect actual behavior
- Failure memory is up to date for newly discovered defect classes
- Retrospective lessons that should become guardrails have been captured

### Manual validation gate
For critical workflow releases, a human should have executed a bounded manual validation path covering the major lifecycle, especially where interactive UI behavior matters.

---

## Required gates for specific risky change classes

### If a change touches persistence
Must also confirm:
- schema/app version handling
- save/resume behavior
- no hidden migration break
- no path or manifest identity corruption

### If a change touches routing
Must also confirm:
- route derivation remains persisted-truth-driven
- no remembered-tab shortcuts reappear
- correct surface opens after create/reopen/continue

### If a change touches Step 1 / Sample Set Manager
Must also confirm:
- starter rows remain correct
- saved values persist correctly
- navigation away/back behavior follows the intended contract
- downstream upload/match uses the right upstream state source
- explicit save semantics are preserved if documented

### If a change touches upload/match rebuild
Must also confirm:
- saved sample set truth is used correctly
- raw row exclusion persistence remains correct
- rebuild outputs are operator-visible and not silently empty due to state loss
- downstream preview/audit reflects the real governed inputs

### If a change touches publish or reopen
Must also confirm:
- publish prerequisites are enforced
- evidence package integrity holds
- reopen creates a new working revision
- source published evidence remains unchanged
- lineage and audit fields are written

### If a change touches locks or protected actions
Must also confirm:
- lock metadata is correct
- stale lock handling works
- override requires reason
- actor logging exists
- review independence is still enforced

---

## Evidence required to clear a gate
Acceptable evidence includes:
- targeted automated tests
- integration/workflow test results
- bounded manual validation notes
- docs updates that encode the lesson
- code inspection for structural rules like no UI-owned business logic

Unacceptable evidence includes:
- “it seems fine”
- helper-only proof for a workflow defect
- passing tests that do not exercise the real failure path
- undocumented behavior changes

---

## Red flags that should block merge or release
Block immediately if you find:
- merge conflict markers
- contradictory route logic in multiple places
- action-widget keys restored into durable state
- published artifacts being reused as mutable working state
- tests passing only because they avoid the real lifecycle path
- docs saying one thing while implementation does another on a critical workflow seam
- silent failure on create, save, reopen, submit, publish, or review claim
- new logic that treats UI memory as authoritative over persisted truth

---

## Final acceptance question
Before calling a change good enough, ask:

**Does this change make the workflow more governed, more explicit, and less likely to repeat known state/routing/evidence failures?**

If the answer is not clearly yes, the change is not ready.