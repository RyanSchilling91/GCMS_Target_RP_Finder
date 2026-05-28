# Failure Catalog

## Purpose
Record important failures so they become reusable engineering memory instead of being forgotten.

This is especially important for AI-assisted development because it prevents repeated mistakes across sessions and projects.

## How to use this file
Before changing risky behavior:
1. Check whether the failure pattern already exists.
2. If it exists, treat it as a regression landmine.
3. If it does not exist, add a new entry once root cause is understood.

## Entry template

### Failure title
#### Symptom
What the user/operator experienced.

#### Root cause
What actually caused it.

#### Detection gap
Why existing tests, docs, or reasoning missed it.

#### Prevention rule
What should change in process, tests, docs, or architecture.

#### Regression test / guardrail
What test or check prevents recurrence.

---

## Seed reusable lessons

### Derived truth persisted as source truth
#### Symptom
Outputs look plausible but no longer reflect current source inputs.
#### Root cause
Recomputable data was stored and later trusted as authoritative.
#### Detection gap
Working, derived, and evidence state were not classified before persistence design.
#### Prevention rule
Use `STATE_CLASSIFICATION.md` before storage design and challenge permanent storage of recomputable values.
#### Regression test / guardrail
Tests must verify recalculation after source-state change and stale-output invalidation.

### UI-owned state mutation breaks workflow
#### Symptom
User edits drift, disappear, duplicate, or behave every-other-click due to UI reruns/session behavior.
#### Root cause
Business state was stored in framework-owned widget/session state instead of an explicit application state model.
#### Detection gap
Tests covered visible happy path but not refresh/rerun/navigation paths.
#### Prevention rule
Keep UI state temporary. Commit only through explicit save/service functions.
#### Regression test / guardrail
Refresh/reload/navigation tests must verify persisted state remains stable.

### Version marker lies about real schema
#### Symptom
System appears migrated but fails because required tables, columns, or indexes are missing.
#### Root cause
Startup trusted metadata/version markers without validating actual structures.
#### Detection gap
Migration tests covered nominal path only.
#### Prevention rule
Validate version markers and required structures before declaring storage ready.
#### Regression test / guardrail
Use damaged/partial migration fixtures.

### Parent state changed while child records remain active
#### Symptom
Valid-looking deactivation/delete/update fails or corrupts workflow because dependent records still reference the parent.
#### Root cause
Mutation order ignored parent/child dependency rules.
#### Detection gap
Tests lacked live dependent-record scenarios.
#### Prevention rule
Document dependency order and test active-child cases before parent mutation.
#### Regression test / guardrail
Parent mutation tests must include active and historical children.

### Duplicate business identity slips past technical ID checks
#### Symptom
System prevents duplicate generated IDs but allows semantically duplicate business records.
#### Root cause
Uniqueness validation focused on technical identifiers instead of user-meaningful identity.
#### Detection gap
Tests did not combine generated ID and business-identity collision cases.
#### Prevention rule
Validate business identity separately from technical identifier uniqueness.
#### Regression test / guardrail
Duplicate business-key tests are required for each major entity.

### Evidence overwritten during rework or reopen
#### Symptom
A published/approved record changes without a clear supersession trail.
#### Root cause
Working state and evidence state were stored together or reopened in place.
#### Detection gap
Workflow tests stopped at publish and did not test reopen/rework.
#### Prevention rule
Published evidence is immutable. Reopen creates new working revision or superseding package.
#### Regression test / guardrail
Publish→reopen→republish tests must preserve original evidence.

### Unsafe persistence change without save/load discovery
#### Symptom
A fix works in one path but breaks reload, resume, export, migration, or another UI entry point.
#### Root cause
Agent edited storage shape without inventorying all save/load/rehydrate paths.
#### Detection gap
No mandatory persistence discovery before changing schema or state flow.
#### Prevention rule
Before persistence changes, locate and summarize all save/load/schema entry points.
#### Regression test / guardrail
Round-trip tests must cover every entry point that writes or reads persisted state.
