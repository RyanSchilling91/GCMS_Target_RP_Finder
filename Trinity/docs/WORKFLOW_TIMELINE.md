\# WORKFLOW\_TIMELINE



\## Purpose of this document

Describe the real workflow as a step-by-step operational timeline from run creation through governed completion, including human actions, system actions, review points, persistence points, decision gates, and freeze/archive points.



This document is written from the new bootstrap questionnaire and is intended to define the workflow from first principles, not merely describe the previous app screens.



\---



\## Guided fill status

\- Status: Complete

\- Last reviewed by: project owner + AI

\- Source of truth for this draft: latest `BOOTSTRAP\_QUESTIONNAIRE.md`



\---



\## Workflow summary

The workflow begins with the planned sample set, not the raw upload.



The prior system improved spreadsheet handling but still carried structural confusion because key planning truth was captured too late. The correct operational order begins with pre-run planning, then uses raw upload to satisfy or challenge that plan.



The workflow for version 1 is:



1\. Create or open a run.

2\. Create, import, or verify the planned sample set.

3\. Upload raw instrument rows.

4\. Exclude or document bad/missed injections when needed.

5\. Deterministically match uploaded rows to the pre-run plan.

6\. Review and resolve mismatches, exclusions, and metadata issues.

7\. Derive calculations and review-ready outputs from committed workflow state.

8\. Perform primary QA and either save draft progress or submit for review.

9\. Secondary reviewer claims eligible work and either returns it for rework or approves it.

10\. Publish the approved run into an immutable evidence package.

11\. If later correction is needed, reopen by creating a new working revision from published evidence; never edit the published artifact in place.



This is a governed lifecycle, not an “upload then export” tool.



\---



\## Lifecycle states

\- `Draft`

\- `Ready for Review`

\- `In Review`

\- `Needs Rework`

\- `Approved`

\- `Published`



Allowed transitions:

\- `Draft -> Ready for Review`

\- `Ready for Review -> In Review`

\- `In Review -> Needs Rework`

\- `Needs Rework -> Draft`

\- `In Review -> Approved`

\- `Approved -> Published`

\- `Published -> Draft` only through admin-controlled creation of a new working revision from the published evidence package; the original published revision remains immutable



Lifecycle meaning:

\- `Draft`: mutable working state under analyst control

\- `Ready for Review`: analyst has submitted a saved working revision for independent review

\- `In Review`: eligible reviewer has claimed the run

\- `Needs Rework`: reviewer rejected approval and returned the run for analyst correction

\- `Approved`: reviewer has approved the working revision for publication

\- `Published`: immutable evidence package exists for that revision



\---



\## Workflow timeline



\### Step 0 — Launch, identity capture, and run selection

\- Actor: User

\- Human action: Launch the application from the workstation/approved launcher and choose one of:

&#x20; - `Start New Dataset`

&#x20; - `Continue My Drafts`

&#x20; - `Runs Ready for Review`

&#x20; - `My Reviews In Progress`

&#x20; - `Published Runs`

\- System action:

&#x20; - capture workstation/user identity and launch context

&#x20; - load run listings from governed persistence

&#x20; - route based on selected action plus persisted lifecycle truth

&#x20; - if opening an existing mutable run, attempt to acquire the correct lock

\- Decision point:

&#x20; - create new run

&#x20; - resume draft

&#x20; - claim or resume review

&#x20; - open published evidence

\- Persistence impact:

&#x20; - append audit/open events

&#x20; - no scientific working data changed yet

\- Rule:

&#x20; - home/open behavior must route from persisted workflow truth, not stale UI memory or remembered tab state



\### Step 1 — Create or open the planned sample set

\- Actor: Primary analyst / operator

\- Human action:

&#x20; - create a new planned sample set

&#x20; - or import/restore an existing plan

&#x20; - or verify the current saved plan before continuing

\- What enters the system first:

&#x20; - the planned sample set

\- Planning content may include:

&#x20; - intended sample set

&#x20; - expected rows

&#x20; - pairing expectations

&#x20; - categories / labels

&#x20; - exclusions

&#x20; - metadata required before upload and matching

\- System action:

&#x20; - initialize or restore the working Sample Set Manager for the run

&#x20; - preserve stable row ordering and committed plan state

&#x20; - persist working-state edits at explicit save checkpoints

\- Decision point:

&#x20; - commit sample plan for downstream matching

\- Persistence impact:

&#x20; - editable working state is created or updated

\- Notes:

&#x20; - this step is the true workflow entry artifact

&#x20; - the workflow is wrong if raw upload is treated as the first truth source



\### Step 2 — Upload or import raw instrument rows

\- Actor: Primary analyst

\- Human action:

&#x20; - upload/import the raw instrument data file(s)

&#x20; - inspect preview

\- System action:

&#x20; - parse the raw upload

&#x20; - preserve raw row provenance

&#x20; - stage imported rows for matching without treating them as final truth by themselves

\- Persistence impact:

&#x20; - raw input enters mutable working state

\- Notes:

&#x20; - raw upload is an input to the governed workflow, not a replacement for pre-run planning



\### Step 3 — Exclude or document unusable raw rows

\- Actor: Primary analyst

\- Human action:

&#x20; - exclude rows for missed injection, bad injection, or documented instrument/human error

&#x20; - document reasons where required

\- System action:

&#x20; - preserve the original raw row payload

&#x20; - track which rows are excluded from matching/rebuild consumption

\- Decision point:

&#x20; - whether a row remains available for deterministic matching

\- Persistence impact:

&#x20; - working-state exclusion decisions are saved

\- Notes:

&#x20; - exclusion is a controlled workflow decision, not silent raw-data mutation



\### Step 4 — Deterministic match of raw rows to the pre-run plan

\- Actor: System, initiated by primary analyst

\- Human action:

&#x20; - trigger matching/rebuild from the current committed plan plus current saved raw-row state

\- System action:

&#x20; - perform deterministic matching between remaining raw rows and planned sample set lines

&#x20; - build resolved row mappings, pairing structures, mismatch flags, and warnings

&#x20; - produce matching preview and downstream review-ready structures

\- Automated work:

&#x20; - matching logic

&#x20; - pairing logic

&#x20; - warning generation

&#x20; - workflow-progress derivation

\- Decision point:

&#x20; - upload/match validation

\- Persistence impact:

&#x20; - derived-from-working-state structures may be refreshed

\- Notes:

&#x20; - matching rules must be documented and stable

&#x20; - rematch must consume committed upstream state, not unsaved UI drift



\### Step 5 — Matching preview and mismatch resolution

\- Actor: Primary analyst

\- Human action:

&#x20; - review the matching preview

&#x20; - resolve mismatches, exclusions, missing metadata, and planning issues

&#x20; - revise the plan or exclusions where needed

\- System action:

&#x20; - present resolved sample rows, warnings, and consistency checks

&#x20; - rebuild downstream structures after committed corrections

\- Manual work:

&#x20; - mismatch resolution

&#x20; - exclusions

&#x20; - metadata correction

\- Decision point:

&#x20; - whether matching state is acceptable to proceed

\- Persistence impact:

&#x20; - committed corrections update mutable working state

\- Notes:

&#x20; - this is the first major human validation point after automated matching



\### Step 6 — Derivation of calculations and review-ready outputs

\- Actor: System

\- Human action:

&#x20; - none required beyond using the committed workflow state as source

\- System action:

&#x20; - derive calculations

&#x20; - produce resolved tables

&#x20; - generate review-ready outputs from committed workflow state

\- Automated work:

&#x20; - derived calculations

&#x20; - resolved tables

&#x20; - route/resume logic

&#x20; - guarded state transitions

\- Persistence impact:

&#x20; - derived state may be cached for workflow use, but canonical truth remains committed working state plus governed config

\- Notes:

&#x20; - calculations are outputs of workflow truth, not editable source truth



\### Step 7 — Primary QA and draft handling

\- Actor: Primary analyst

\- Human action:

&#x20; - perform primary QA judgment

&#x20; - choose to continue editing, save draft, save and close, or submit for review

\- System action:

&#x20; - `Save Draft`: persist current working state and retain lock

&#x20; - `Save \& Close`: persist current working state and release lock

&#x20; - `Submit for Review`: persist current working state, move run to `Ready for Review`, release analyst lock, and make the run available for reviewer claim

\- Manual work:

&#x20; - QA judgment

\- Decision point:

&#x20; - analyst QA

&#x20; - submit-for-review decision

\- Persistence impact:

&#x20; - mutable working state and handoff metadata are saved

\- Notes:

&#x20; - explicit save/close/review actions are workflow controls, not mere UI conveniences



\### Step 8 — Review claim and independent secondary review

\- Actor: Secondary reviewer

\- Human action:

&#x20; - claim eligible review work

&#x20; - review committed workflow state, resolved sample rows, calculation outputs, metadata consistency, and required publish artifacts

&#x20; - either return for rework or approve

\- System action:

&#x20; - enforce reviewer independence

&#x20; - reject self-review

&#x20; - acquire review lock

&#x20; - record review claim, review outcome, actor, and timestamps

\- What gets reviewed:

&#x20; - committed workflow state

&#x20; - resolved sample rows

&#x20; - calculation outputs

&#x20; - metadata consistency

&#x20; - required publish artifacts/prerequisites

\- What determines approval:

&#x20; - reviewer independence

&#x20; - valid workflow state

&#x20; - complete required artifacts

&#x20; - no unresolved blocking issues

&#x20; - publish prerequisites satisfied

\- Persistence impact:

&#x20; - review/signoff/audit state appended

&#x20; - lifecycle state changes to `Needs Rework` or `Approved`

\- Notes:

&#x20; - review independence is a per-run rule and part of system correctness



\### Step 9 — Rework loop when review fails

\- Actor: Reviewer then primary analyst

\- Human action:

&#x20; - reviewer returns the run for rework with rationale

&#x20; - analyst reopens mutable work, corrects issues, and resubmits when ready

\- System action:

&#x20; - transition `In Review -> Needs Rework`

&#x20; - restore the run to editable draft workflow under proper lock/handoff rules

\- Persistence impact:

&#x20; - rework reason and lifecycle changes are recorded

\- Notes:

&#x20; - rework is a governed loop, not an ad hoc restart



\### Step 10 — Publish validation and evidence packaging

\- Actor: System, under approved user action

\- Human action:

&#x20; - initiate publish only after approval

\- System action:

&#x20; - validate publish prerequisites

&#x20; - recompute final outputs from approved working truth

&#x20; - build immutable published evidence package

&#x20; - record signoff/review data, manifest metadata, audit references, and criteria provenance

&#x20; - transition the revision to `Published`

\- Automated work:

&#x20; - artifact packaging

&#x20; - publish validation

&#x20; - evidence freezing

\- Final published package contains:

&#x20; - approved working snapshot

&#x20; - exported result files

&#x20; - summary report(s)

&#x20; - manifest metadata

&#x20; - signoff / review record

&#x20; - audit trail or audit references

&#x20; - criteria provenance used for the approved output

\- Freeze point:

&#x20; - publish is the freeze signal for that revision

\- Persistence impact:

&#x20; - evidence state is written and becomes immutable

\- Notes:

&#x20; - operator-facing exports may leave the system, but the published evidence package remains the governed archive



\### Step 11 — Published viewing and governed archive use

\- Actor: User, reviewer, admin, or support owner as appropriate

\- Human action:

&#x20; - open published runs in read-only mode

&#x20; - inspect evidence package and published lineage

\- System action:

&#x20; - route published runs to a read-only published evidence surface

&#x20; - never open published evidence as editable draft/review state

\- Persistence impact:

&#x20; - read-only access only, aside from audit/view events

\- Notes:

&#x20; - published evidence is a governed archive object, not a live editable workspace



\### Step 12 — Controlled reopen or reload from published evidence

\- Actor: Admin / project lead / recovery operator under governed authority

\- Human action:

&#x20; - authenticate protected action

&#x20; - record reason for reopen or controlled reload

\- System action:

&#x20; - validate the published artifact package

&#x20; - create a new working revision derived from published evidence

&#x20; - preserve lineage to the published source revision

&#x20; - return the new revision to the proper lower workflow stage without mutating the original evidence package

\- Manual work:

&#x20; - admin override / recovery actions

\- Decision point:

&#x20; - admin-controlled recovery / reopen

\- Persistence impact:

&#x20; - new mutable working revision created

&#x20; - original published evidence remains untouched

\- Notes:

&#x20; - published artifacts are never edited in place

&#x20; - controlled reload back into lower workflow stages is allowed only through this governed path



\---



\## Human vs system responsibilities



\### Human-driven actions

\- sample planning

\- mismatch resolution

\- exclusions

\- metadata correction

\- QA judgment

\- review judgment

\- admin override / recovery actions



\### System-driven actions

\- matching logic

\- derived calculations

\- workflow progress determination

\- route/resume logic

\- lock handling

\- artifact packaging

\- publish validation

\- guarded state transitions



\---



\## Review and approval points

Formal review points in this workflow are:



1\. Matching preview review by the analyst

2\. Primary QA before submission

3\. Secondary independent review before approval

4\. Publish validation before evidence freeze



Approval is not only “looks good.” Approval means:

\- independent reviewer

\- valid lifecycle state

\- no unresolved blocking issues

\- required publish prerequisites satisfied



\---



\## Handoff points

Formal handoff points are:



\- `Save \& Close` for paused unfinished work

\- `Submit for Review` for analyst-to-review transfer

\- `Needs Rework` for reviewer-to-analyst return

\- `Approved` as the state permitting publish

\- `Published` as the evidence freeze point



\---



\## Freeze and archive points

\- Working state remains mutable through draft and rework phases

\- Derived state is disposable/recomputable

\- `Published` freezes the revision as immutable evidence

\- Any later change must occur through a new working revision created from the published package



\---



\## Edge cases and alternate paths

This workflow must explicitly support or fail safely for:



\- parse failure on upload

\- damaged or incomplete working metadata

\- missing or stale saved state

\- mismatch between pre-run plan and uploaded raw rows

\- excluded or bad raw rows

\- incomplete metadata before review or publish

\- stale or orphaned locks

\- invalid admin override requests

\- self-review attempts

\- duplicate run-ID creation attempts

\- partial publish artifact creation failure

\- damaged published package on reopen

\- controlled deletion or disposal of drafts before publish

\- controlled reload from published evidence into lower workflow stages when authorized



\---



\## Notes for the agent

\- Do not collapse this workflow into “upload, review, export.”

\- The planned sample set is the real operational entry artifact.

\- Workflow truth must come from committed/persisted state, not inferred UI state.

\- Reviewer independence, immutable publish, and controlled reopen are not optional.

\- Keep this document aligned with `PROJECT\_BRIEF.md`, `DATA\_MODEL.md`, `STATE\_CLASSIFICATION.md`, ADRs, `TEST\_STRATEGY.md`, and `QUALITY\_GATES.md`.

