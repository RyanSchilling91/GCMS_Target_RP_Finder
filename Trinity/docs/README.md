\# README.md



\## Project overview

This repository documents and supports the design of a \*\*workflow-governed laboratory application\*\* intended for restricted or professional environments where correctness, traceability, controlled review, and publish integrity matter more than fast prototype convenience.



The project’s current implementation posture is:



\- a \*\*Python application core\*\* that owns workflow logic, persistence rules, and governance behavior

\- a \*\*thin presentation layer\*\* currently rendered through Streamlit

\- \*\*file-backed embedded persistence\*\* suitable for shared-storage deployment in constrained environments

\- \*\*single-editor working revision locking\*\*

\- \*\*immutable published evidence packages\*\*

\- \*\*controlled re-entry\*\* from published evidence by creating a new working revision rather than editing published artifacts in place



This repository is documentation-first by design. The docs are intended to prevent the project from repeating earlier failure modes where code, workflow, persistence, and architecture drifted apart.



\---



\## What problem this project is solving

The system is meant to replace fragile, hard-to-govern workflow behavior with a more defensible lifecycle for laboratory work.



At a high level, the system must support:



\- creating a new run from a planned sample set

\- editing and saving working truth

\- uploading and reconciling raw instrument data

\- auditing downstream matching and calculation behavior

\- handing work off for independent review

\- approving and publishing governed outputs

\- preserving immutable evidence after publish

\- allowing controlled operational re-entry through a new working revision when necessary



The project is not just building screens. It is building a durable workflow model.



\---



\## Core architectural stance

This project should be understood as:



\*\*workflow-governed Python core + thin UI\*\*



not:



\*\*UI app with some helper functions\*\*



That distinction drives the design:



\- workflow logic belongs in service/domain modules

\- persisted truth must remain authoritative

\- derived state must stay recomputable

\- evidence state must remain immutable after publish

\- routing must derive from persisted truth, not stale UI memory

\- the presentation layer should remain replaceable in the future



\---



\## Workflow summary

The current documented workflow is:



1\. Start a new dataset/run

2\. Complete the planned sample set in Step 1

3\. Save working truth

4\. Upload instrument/raw data

5\. Save governed exclusions or row-drop decisions

6\. Rebuild and audit downstream matches/calculations

7\. Continue draft work or submit for review

8\. Independent reviewer claims and reviews the run

9\. Approved runs are published into an immutable evidence package

10\. If post-publish correction is required, an authorized user creates a new working revision derived from the published evidence package



The detailed workflow contract lives in `WORKFLOW\_TIMELINE.md`.



\---



\## Documentation map

Start with:



1\. `INDEX.md`

2\. `PROJECT\_BRIEF.md`

3\. `BOOTSTRAP\_QUESTIONNAIRE.md`

4\. `WORKFLOW\_TIMELINE.md`

5\. `DATA\_MODEL.md`

6\. `STATE\_CLASSIFICATION.md`

7\. `ARCHITECTURE\_SELECTION.md`

8\. relevant ADRs

9\. `TEST\_STRATEGY.md`

10\. `QUALITY\_GATES.md`

11\. `FAILURE\_CATALOG.md`

12\. `RETROSPECTIVE.md`



Do not change critical workflow code without grounding in those docs.



\---



\## Key design principles

\- Planned sample set is first-class working truth.

\- `Run`, `Working Revision`, and `Published Evidence Package` are separate concepts and must remain separate.

\- Publish creates immutable evidence.

\- Reopen does not mutate published evidence; it creates a new working revision with lineage back to the published source.

\- Single-editor lock semantics are intentional for the current deployment model.

\- Review independence is mandatory.

\- Restricted-environment practicality matters; do not assume cloud-first architecture.



\---



\## Current deployment posture

The near-term deployment model assumes:

\- shared storage

\- launcher-based access

\- local/network-restricted operation

\- no dependency on public hosted infrastructure for core operation



This is a deliberate choice for the current phase, not a claim that the long-term deployment model is permanently fixed.



\---



\## What this repo is trying to prevent

This docs set exists in part because earlier work revealed recurring failure patterns such as:

\- UI state drifting away from authoritative working state

\- routing depending on remembered page state instead of persisted truth

\- save/reopen behavior losing or mutating governed inputs

\- patches fixing the visible symptom while leaving the deeper persistence or lifecycle defect intact

\- architecture lagging behind implementation

\- failure lessons living only in chat or memory instead of durable project docs



Those lessons are now meant to be encoded directly into the way the project is built.



\---



\## For contributors and coding agents

Before changing code, do not assume the current implementation is the contract.



The contract lives in the docs.



At minimum, ground yourself in:

\- workflow timeline

\- data model

\- state classification

\- architecture selection

\- relevant ADRs

\- test strategy

\- quality gates

\- failure catalog

\- retrospective



If a code path and the docs disagree, surface the conflict before implementing further changes.



\---



\## Repo intent

This repository is meant to function as:

\- project memory

\- implementation guardrail

\- onboarding surface

\- architecture anchor

\- anti-regression knowledge base



If used correctly, it should make the next implementation pass more deliberate, more stable, and less likely to repeat the kind of failure patterns that previously consumed time and trust.

