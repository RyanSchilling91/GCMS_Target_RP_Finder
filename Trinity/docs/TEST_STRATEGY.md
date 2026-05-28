\# TEST\_STRATEGY.md



\## Purpose of this document

Define how the project will be tested, what confidence levels are required for workflow-critical behavior, and what regression surfaces must remain protected as the system evolves.



The purpose of testing here is not just “does the code run.” It is to prove that the governed workflow behaves correctly across creation, editing, save/resume, review, publish, and controlled re-entry without silent state drift or evidence corruption.



\---



\## Guided fill status

\- Status: Updated

\- Last reviewed by: project owner + AI

\- Last updated: 2026-03-24



\---



\## Testing philosophy



\### 1. Test the workflow contract, not just helper functions

Tests should prove the documented behavior of the system:

\- what a user is allowed to do

\- what the system must persist

\- what must be derived

\- what must remain immutable

\- what transitions are allowed or forbidden



\### 2. Treat state-boundary bugs as first-class defects

This project has already shown that many dangerous bugs are not “bad math” bugs but boundary bugs:

\- UI state vs working state

\- active in-session state vs explicit durable save

\- working truth vs derived truth

\- working truth vs published evidence

\- remembered route vs route derived from persisted truth



Testing must explicitly target those seams.



\### 3. Protect lifecycle correctness

The primary risk is not only field-level mistakes. It is workflow corruption:

\- reopening the wrong step

\- saving the wrong truth

\- mismatched handoff

\- broken review independence

\- published evidence mutation

\- reopen destroying lineage

\- stale locks or bad overrides



\### 4. Prefer targeted regression tests over vague confidence

When a bug is fixed, add a regression that proves the actual failure path no longer reproduces.



\### 5. Be honest about proof level

If a test only covers helper-level logic, do not describe it as full end-to-end proof.

If optional runtime dependencies are missing, say so clearly.



\---



\## Testing layers



\### 1. Unit tests

Use for:

\- normalization logic

\- pure matching helpers

\- route/progress helper functions

\- lock timeout calculations

\- manifest validation

\- criteria validation

\- state classification helpers

\- publish/reopen validation logic



\### 2. Integration tests

Use for:

\- run creation

\- save/resume

\- sample set manager save/load behavior

\- upload/match persistence and rebuild behavior

\- route determination from persisted truth

\- review claim and status transitions

\- publish package assembly

\- reopen from published into new working revision

\- lock acquisition/release/timeout/override behavior



\### 3. Workflow regression tests

Use to reproduce real failure surfaces from the failure catalog:

\- Step 1 navigation loss

\- stale editor save

\- create-new seed corruption

\- route drift after reopen

\- rebuild using stale upstream truth

\- publish/reopen lineage break

\- action-widget state leaking into persistence

\- duplicate run identity confusion

\- missing or stale lock metadata behavior



\### 4. Manual/runtime validation

Use when interactive behavior or environment-specific behavior matters:

\- UI interaction timing

\- reactive editor behavior

\- launcher/open-from-shared-storage behavior

\- workstation identity capture

\- lock heartbeat behavior across multiple workstations

\- publish artifact inspection



Manual validation does not replace automated regression coverage, but some seams still need both.



\---



\## Minimum critical workflow paths that must be tested



\### Path 1: Create New -> Step 1 initialization

Must prove:

\- create new succeeds visibly or fails visibly

\- run identity is created correctly

\- draft status is correct

\- correct route lands on Step 1

\- planned sample set starter state is initialized correctly

\- starter state persists correctly where required



\### Path 2: Step 1 edit -> Save Draft -> Close -> Continue Draft

Must prove:

\- edited planned sample set rows become authoritative working truth only through the documented save boundary

\- reopen restores the same saved rows

\- reopen lands on the correct workflow surface



\### Path 3: Step 1 active navigation away/back

Must prove:

\- active editor state behaves according to the intended contract

\- navigation does not silently destroy the current working truth

\- page-local editor behavior does not create stale overwrite patterns



\### Path 4: Upload raw data -> Exclude rows -> Save raw row drops -> Rebuild matches

Must prove:

\- raw upload creates the correct working-state artifacts

\- saved raw row drops persist correctly

\- rebuild uses the correct upstream saved/planned sample set truth

\- rebuild does not silently clear or replace Step 1 data

\- downstream preview and audit surfaces reflect the actual saved inputs



\### Path 5: Continue Draft routing

Must prove:

\- route is determined from persisted workflow artifacts

\- reopening does not depend on remembered tabs or stale UI route keys

\- partially completed runs reopen at the first incomplete or appropriate governed step



\### Path 6: Submit for Review -> Ready for Review -> Claim Review

Must prove:

\- submit saves before status transition

\- lock behavior follows the documented rules

\- reviewer claim obeys independence requirements

\- the same person cannot both primary-review and secondary-review where prohibited



\### Path 7: In Review -> Needs Rework -> Draft

Must prove:

\- needs-rework transitions preserve audit trail

\- the run returns to editable draft state correctly

\- review outcomes and reasons are not lost



\### Path 8: Approved -> Publish

Must prove:

\- publish prerequisites are enforced

\- the evidence package is assembled correctly

\- manifest, approved snapshot, exports, summary/report, signatures, and criteria provenance are present

\- publish creates immutable evidence artifacts

\- post-publish behavior no longer treats those artifacts as mutable working state



\### Path 9: Published -> Reopen into new working revision

Must prove:

\- published evidence remains unchanged

\- reopen requires the governed protected action path

\- the new working revision records lineage back to the published evidence source

\- the system does not edit the published package in place



\### Path 10: Lock lifecycle

Must prove:

\- lock acquisition works

\- lock release works

\- stale timeout works

\- override requires reason and governed actor path

\- conflicting editor attempts fail visibly



\---



\## State-boundary tests required by design



\### Working state

Tests must prove that mutable workflow truth is persisted correctly and restored correctly.



\### Derived state

Tests must prove that derived artifacts are recomputed from working truth and do not become their own hidden source of truth.



\### Evidence state

Tests must prove that published evidence is immutable and remains distinct from working state.



\### UI buffer boundaries

Tests must prove that reactive/editor surfaces do not silently overwrite committed truth or silently bypass explicit save semantics.



\---



\## Specific regression categories that should exist



\### Sample Set Manager regressions

\- blank starter rows remain blank where documented

\- saved rows survive reopen

\- unsaved edits do not masquerade as saved truth

\- save uses the right authoritative source

\- navigation away/back does not cause stale/default overwrite

\- downstream rebuild reads the correct saved or committed upstream data according to the workflow contract



\### Upload/Match regressions

\- same upload is idempotent where intended

\- different upload reparses where intended

\- raw row exclusions persist correctly

\- rebuild uses correct last-saved or current-governed inputs

\- dropped rows, unmatched rows, and audit summaries remain correct



\### Routing regressions

\- create new routes correctly

\- continue draft routes correctly

\- review claim routes correctly

\- published viewer routes correctly

\- route is derived from persisted truth, not stale page memory



\### Persistence / rehydration regressions

\- schema/app version metadata is validated

\- supported older snapshots migrate or load correctly

\- missing optional scalars restore in canonical form

\- booleans restore as booleans

\- governed sentinel values remain stable



\### Publish / reopen regressions

\- publish package contains required artifacts

\- publish refuses invalid workflow state

\- reopen from published creates a new working revision

\- published artifacts remain unchanged after reopen

\- lineage is preserved in metadata



\### Locking / protected-action regressions

\- stale lock detection works

\- admin override requires reason

\- protected actions record actor path

\- reviewer independence is enforced



\---



\## Dataset strategy



\### 1. Small deterministic fixtures

Use small fixtures to make route, save, and matching behavior obvious.



\### 2. Representative workflow fixtures

Maintain bounded but realistic datasets that reflect actual planning, upload, exclusion, review, and publish flows.



\### 3. Regression fixtures tied to failures

When a real defect is found, preserve a fixture or state shape that reproduces it if practical.



\### 4. Version-compatibility fixtures

Retain older snapshot examples where backward-compatible rehydration is required.



\---



\## Test naming and reporting rules

Tests should make the contract obvious from the name.



Good examples:

\- `test\_create\_new\_run\_initializes\_blank\_step\_one\_state`

\- `test\_continue\_draft\_routes\_from\_persisted\_truth\_not\_ui\_memory`

\- `test\_publish\_creates\_immutable\_evidence\_package`

\- `test\_reopen\_from\_published\_creates\_new\_working\_revision`



When reporting work, distinguish clearly between:

\- unit proof

\- integration proof

\- workflow proof

\- manual/runtime proof



\---



\## Manual validation checklist

Use this when an automated seam is not enough:



\- create a new run

\- edit Step 1

\- save and close

\- reopen from home

\- upload raw data

\- exclude rows

\- save raw row drops

\- rebuild matches

\- verify preview/audit

\- submit for review

\- claim review from a different user identity

\- move to approved

\- publish

\- inspect package contents

\- perform controlled reopen to a new working revision

\- confirm published package remains unchanged

\- test stale lock and override in a multi-workstation scenario if possible



\---



\## Exit criteria for saying a workflow defect is fixed

A workflow bug fix is not complete unless:

1\. the expected behavior is grounded in the docs

2\. the actual root cause is identified

3\. the fix is bounded and does not silently change save semantics or lineage semantics

4\. at least one targeted regression proves the failing path no longer reproduces

5\. any affected docs are updated if the failure exposed a new rule or lesson

6\. remaining unverified surfaces are stated honestly



\---



\## Notes for contributors and coding agents

\- Do not confuse “tests pass” with “workflow is safe.”

\- Do not rely only on helper-level proof for state-boundary bugs.

\- If the real user path is more complex than the test, acknowledge that gap.

\- When in doubt, add the regression. This project has already paid the price for trusting memory and intuition over durable failure coverage.

