\# PROJECT\_BRIEF



\## Purpose of this document

Define the business purpose, users, scope boundaries, operating constraints, and success conditions for the project.



This brief is written from the new bootstrap questionnaire and is intended to reset the project on clearer foundations. It does not assume the prior app design is the final answer. It preserves proven workflow lessons while removing the ambiguity that made the earlier build fragile under continued feature work.



\---



\## Guided fill status

\- Status: Complete

\- Last reviewed by: project owner + AI

\- Source of truth for this draft: latest `BOOTSTRAP\_QUESTIONNAIRE.md`



\---



\## Problem being solved

The project is not simply trying to replace a spreadsheet.



The real problem is that the current chlorophyll workflow depends on brittle spreadsheet-driven run handling and loosely governed application behavior. The spreadsheet interrupts work when protected equation cells are disturbed, forces manager intervention for routine recovery, and provides weak support for searchable history, structured review handoff, and defensible traceability. The earlier app improved this by introducing a guided workflow and save/resume behavior, but it still exposed deeper instability in workflow truth, route/open behavior, persistence semantics, and revision control.



The system being built now must solve the larger problem:



\- replace brittle spreadsheet-based workflow control

\- protect calculation integrity without relying on fragile sheet locking

\- support deterministic save/resume across sessions

\- centralize run truth, review history, and evidence outputs

\- enforce reviewer independence and governed handoff

\- make publish, reopen, and recovery behavior auditable and safe



This is a workflow-governance and lifecycle-correctness project, not just a UI replacement.



\---



\## Intended users

Primary users of the system are:



\- \*\*Primary analyst / operator\*\*

&#x20; - creates or opens a run

&#x20; - prepares the planned sample set before upload

&#x20; - uploads raw instrument data

&#x20; - resolves exclusions, mismatches, and metadata issues

&#x20; - performs primary QA

&#x20; - saves draft work or submits for review



\- \*\*Secondary reviewer\*\*

&#x20; - independently claims eligible work

&#x20; - reviews matching, calculations, metadata, and final outputs

&#x20; - returns work for rework or approves it

&#x20; - must be different from the primary analyst on that run



\- \*\*Project lead / admin\*\*

&#x20; - governs workflow rules and protected actions

&#x20; - manages controlled recovery, unlock, reopen, and criteria/config changes

&#x20; - maintains oversight of auditability and release safety



\- \*\*Support owner / recovery operator\*\*

&#x20; - helps recover from stale locks, damaged metadata, or workflow interruptions

&#x20; - relies on documented recovery paths rather than ad hoc fixes



\---



\## What users do today without this system

Today the workflow begins outside the application.



Users pull the sample set from LIMS, determine the run order, and manually work through spreadsheet-based setup and calculation steps. After instrument execution, they receive basic raw output, paste or align it into the spreadsheet, and rely on protected formulas plus manual alignment to generate final results.



This process leaves users dependent on:



\- manual alignment and copy/paste operations

\- post-run entry of metadata that could have been planned earlier

\- spreadsheet cell protection as the mechanism for equation safety

\- weak recall of prior work for review or recheck

\- inconsistent evidence of who changed what, when, and why



\---



\## What is painful, slow, risky, or confusing today

The pain is larger than inconvenience.



Current risks and workflow weaknesses include:



\- spreadsheet lock/unlock interruptions when formulas or alignment are disturbed

\- post-run metadata entry that should be captured earlier in a stable planning step

\- no reliable centralized path for looking up past runs, outputs, or review state

\- weak chain of custody for actor, timestamp, and workflow-stage history

\- nondeterministic or fragile save/resume behavior

\- route/open drift between displayed workflow state and persisted truth

\- stale session behavior overriding saved truth

\- duplicate or ambiguous run identity behavior

\- fragile publish/reopen behavior

\- lack of controlled draft disposal before publish

\- lack of governed reload/re-entry paths when published work must re-enter workflow



These are workflow integrity failures, not merely UX annoyances.



\---



\## Objective / purpose

The objective of version 1 is to build a dependable governed lab workflow application that preserves the operational value already proven by the earlier app while rebuilding the project around clearer truth boundaries and safer lifecycle control.



The system should:



1\. begin from the real operational start point: the planned sample set

2\. guide the analyst through upload, match, audit, review, and publish

3\. treat working state, derived state, and evidence state differently

4\. support deterministic save/resume and safe save-and-close behavior

5\. make review handoff, approval, and publish actions explicit

6\. preserve published evidence as immutable

7\. support controlled reopen-by-new-revision only

8\. keep business logic and persistence behavior outside the UI layer so the UI can later be replaced if needed



\---



\## Release boundary for version 1

Version 1 covers the governed workflow from run creation through immutable published evidence package creation, plus controlled reopen into a new working revision.



Included in scope:



\- run creation and run identity protection

\- pre-run planned sample set setup

\- raw upload/import

\- deterministic matching between uploaded rows and the pre-run plan

\- exclusions and mismatch handling

\- matching audit and calculation audit

\- primary QA workflow

\- explicit draft save, save-and-close, and submit-for-review behavior

\- independent secondary review

\- approval and publish controls

\- immutable evidence packaging

\- controlled reopen from published evidence into a new working revision

\- audited recovery and lock-management paths

\- searchable historical runs and outputs through the governed application structure



\---



\## Non-goals / explicitly out of scope

Out of scope for version 1:



\- simultaneous co-editing of the same working revision

\- enterprise SSO as a prerequisite

\- internet-hosted SaaS deployment

\- direct instrument-to-app integration as a required feature

\- major redesign of the scientific method itself

\- editing published evidence in place

\- broad enterprise collaboration features beyond the first governed workflow

\- large-scale replatforming before the core workflow is dependable



Nice-to-have but not required:



\- future portability to a different UI layer

\- richer admin tooling

\- more advanced analytics

\- broader cross-project reuse after first successful implementation

\- eventual direct instrument data piping into the workflow



\---



\## Operational constraints

The project operates under real restrictions that affect design:



\- restricted / governed IT environment

\- offline or local-network-capable operation required

\- no dependency on public internet hosting

\- shared storage is acceptable and practical

\- app launch is expected from workstation shortcuts

\- many users may use the system over time

\- one active editor per working revision is the accepted version 1 collaboration rule

\- auditability, traceability, and recoverability are mandatory

\- workflow truth must not primarily live in UI session state

\- business logic must remain portable outside the current UI framework



\---



\## Success criteria

This project is successful when:



1\. the workflow is easier to perform consistently than the spreadsheet process

2\. pre-run planning is captured in a structured way before raw upload

3\. save/resume is deterministic and safe across sessions

4\. save-and-close releases ownership cleanly without losing work

5\. the home/open flow routes users based on persisted workflow truth, not stale UI memory

6\. review handoff is stable and reviewer independence is enforced

7\. users can search, open, and understand past runs from centralized governed records

8\. publish produces a defensible immutable evidence package

9\. published work can re-enter workflow only through controlled new-revision reopen

10\. actor history, signoff history, criteria provenance, and recovery actions are auditable

11\. release gates catch lifecycle regressions before merge

12\. the system improves speed, consistency, traceability, auditability, and user confidence



\---



\## What improves if this works

Expected improvements include:



\- speed

\- consistency

\- traceability

\- auditability

\- recovery safety

\- equation protection without spreadsheet fragility

\- easier reviewer lookup and signoff workflow

\- clearer separation of mutable work vs frozen evidence

\- reduced dependence on ad hoc manual fixes



\---



\## Production readiness standard for this version

This version is ready for continued development and eventual release when the workflow is documented tightly enough that coding can proceed without guessing core truths.



That means:



\- the workflow is complete end-to-end

\- the data model is explicit enough to prevent vague implementation

\- working, derived, and evidence state are clearly separated

\- architecture recommendations are justified

\- ADR candidates are identified

\- assumptions and unknowns are explicit

\- verification scenarios are concrete

\- the resulting docs are strong enough to block premature coding and prevent architecture drift



\---



\## Directional system shape

The system should be understood around these major objects:



\- Run

\- Working Revision

\- Planned Sample Set Line

\- Raw Instrument Row

\- Match Mapping

\- Resolved Sample Row

\- Derived Result Set

\- Review / Signoff Event

\- Published Evidence Package

\- Lock Record

\- Criteria Configuration

\- User Identity

\- Audit Event



Directionally, the system should keep the UI thin and treat workflow logic, persistence, validation, review controls, and lifecycle governance as application-core concerns rather than page concerns.



\---



\## Notes for the agent

\- Treat this project as a fresh planning-led rebuild informed by prior lessons, not as permission to freestyle from the existing app.

\- Do not reduce the project to “CSV in, report out.”

\- Protect lifecycle truth first.

\- Preserve immutable evidence and governed reopen behavior.

\- Keep this brief aligned with `WORKFLOW\_TIMELINE.md`, `DATA\_MODEL.md`, `STATE\_CLASSIFICATION.md`, `ARCHITECTURE\_SELECTION.md`, ADRs, and test/quality documents.

