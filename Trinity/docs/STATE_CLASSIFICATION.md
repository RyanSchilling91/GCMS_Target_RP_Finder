\# STATE\_CLASSIFICATION



\## Purpose of this document

Define which data belongs to mutable working state, recalculable derived state, immutable evidence state, and temporary UI/session state.



This document exists to prevent truth drift.  

Its purpose is to make it unambiguous which state the system may edit, which state it may recompute, which state it must preserve, and which state must never be treated as authoritative.



This is a governance document, not a caching document.



\---



\## Guided fill status

\- Status: Complete

\- Last reviewed by: project owner + AI

\- Source of truth for this draft: latest `BOOTSTRAP\_QUESTIONNAIRE.md`



\---



\## Why this document matters

Many of the prior failures were not “bugs” in isolation. They were classification failures.



Examples of what went wrong in the earlier build pattern:

\- route/open behavior depended too much on helper summaries or session memory

\- progress labels risked behaving like source truth

\- matching and workflow continuation could drift from committed persisted state

\- stale UI/session values could survive load/reopen and overwrite correct saved truth

\- published outputs and mutable working state were not always guarded by a hard enough conceptual boundary



This document is meant to stop that from happening again.



\---



\## State classes used by the system

The system recognizes four distinct state classes:



1\. \*\*Working State\*\*

2\. \*\*Derived State\*\*

3\. \*\*Evidence State\*\*

4\. \*\*UI / Session State\*\*



These classes are not interchangeable.



\---



\## 1. Working State



\### Definition

Working state is the editable, frequently changing, persisted state tied to the \*\*current mutable working revision\*\*.



This is the canonical source of mutable workflow truth.



If a user is actively performing work that may later be saved, resumed, reviewed, or published, that work should resolve to working state.



\### Key characteristics

\- editable

\- persists across sessions when committed

\- tied to one current mutable revision

\- used as input for matching, review, routing, and publish preparation

\- protected by lock and lifecycle rules

\- authoritative over derived displays and UI memory



\### Examples of working state

\- run identity and current revision linkage

\- committed planned sample set lines

\- analyst-edited labels and exclusions

\- match-resolution choices

\- raw upload batch records

\- raw instrument rows plus analyst usability/exclusion decisions

\- committed revision status

\- mutable notes and workflow annotations

\- current active lock ownership and release state

\- current review handoff state when still part of mutable workflow

\- governed metadata required before review/publish

\- explicit save/submit/rework state transitions on the mutable revision



\### What working state is not

Working state is \*\*not\*\*:

\- a convenience summary

\- a dashboard metric

\- a widget-only value

\- a route recommendation

\- a frozen evidence package

\- a recalculation cache that can be safely discarded without consequence



\### Ownership rule

Working state belongs to the persisted workflow model, not to the UI.



\### Persistence rule

Committed working state \*\*must\*\* persist across sessions.



\### Must never happen

\- mutable workflow truth living only in UI/session variables

\- analyst edits existing only in widgets with no committed persisted representation

\- matching or publish logic depending on uncommitted display state

\- two conflicting working-state authorities for the same revision



\---



\## 2. Derived State



\### Definition

Derived state is system-generated state that can always be recalculated from committed working inputs plus governed configuration.



Derived state may be cached for performance or UX clarity, but it is not the canonical source of truth.



\### Key characteristics

\- recalculable

\- may be cached or materialized temporarily

\- must be invalidated/recomputed when upstream working truth changes

\- should not be user-edited as source truth

\- can support routing, display, queueing, summaries, and validation

\- must yield to persisted working truth when conflicts appear



\### Examples of derived state

\- progress summaries

\- route/open destination recommendations

\- workflow step labels

\- matching summaries

\- resolved sample rows

\- validation summaries

\- pairing audits

\- queue eligibility

\- publish-readiness checks

\- calculation tables and result summaries

\- reviewer work queues

\- presentation summaries for dashboards or list pages



\### What derived state is not

Derived state is \*\*not\*\*:

\- a substitute for stored workflow truth

\- an excuse to bypass source objects

\- evidence that must be preserved permanently

\- safe to trust if upstream committed state has changed and invalidation has not occurred



\### Ownership rule

Derived state is system-owned only.



\### Persistence rule

Derived state may be persisted or cached only as a convenience.  

If persisted, it must still be treated as disposable and recomputable.



\### Invalidation rule

When working state changes, dependent derived state must either:

\- be recomputed immediately, or

\- be marked stale and prevented from acting as truth until recomputed



\### Must never happen

\- derived progress labels overriding the actual persisted lifecycle state

\- queue membership treated as canonical truth instead of being recalculated

\- stale calculation summaries surviving after edits to plan, exclusions, or raw-row handling

\- route/open behavior trusting cached derived state when persisted workflow truth disagrees

\- user-edited derived results becoming canonical source truth



\---



\## 3. Evidence State



\### Definition

Evidence state is preserved, durable, audit-relevant state that must never be silently overwritten and, in many cases, must be immutable.



Evidence state exists to prove what happened, who did it, what governed it, and what was published.



\### Key characteristics

\- durable

\- append-only or immutable depending on object type

\- audit-relevant

\- lineage-preserving

\- used for traceability, compliance, recovery reasoning, and historical inspection

\- may outlive mutable working state



\### Examples of evidence state

\- imported raw source provenance

\- raw upload batch provenance

\- review/signoff events

\- submitted/claimed/approved/rework/published event history

\- admin override events

\- stale-lock recovery events

\- publish manifest

\- approved frozen snapshot

\- immutable published package

\- criteria provenance

\- audit history

\- lineage records linking reopened revisions to published source revisions

\- package integrity metadata / hash if implemented



\### Subclasses inside evidence state



\#### A. Append-only evidence

These may grow by additional entries but prior entries should not be rewritten:

\- audit events

\- review/signoff events

\- admin override events

\- recovery records



\#### B. Frozen evidence

These are created at a publish/freeze point and then treated as immutable:

\- published manifest

\- approved snapshot

\- immutable published package

\- exported result artifacts tied to the published revision

\- criteria provenance bundle for the published revision



\### What evidence state is not

Evidence state is \*\*not\*\*:

\- the active editable workspace

\- a dashboard-only summary

\- temporary UI memory

\- something that can be regenerated with no governance once frozen and published



\### Ownership rule

Evidence state is system-governed.

Users may initiate actions that create evidence, but they do not casually edit evidence objects afterward.



\### Persistence rule

Evidence state must persist across sessions and across revisions where lineage matters.



\### Must never happen

\- silent overwrite of audit history

\- review history overwrite

\- published evidence edited in place

\- criteria provenance missing from a published package

\- mutable draft state being mistaken for frozen evidence

\- reopen implemented by mutating the original published package instead of creating a new working revision



\---



\## 4. UI / Session State



\### Definition

UI/session state is temporary presentation memory used to support interaction flow inside the running UI.



It is useful, but it is not authoritative workflow truth.



\### Key characteristics

\- ephemeral

\- interaction-oriented

\- may be reset by rerun, navigation, refresh, crash, or reopen

\- may hold unsaved edits before explicit commit

\- must never outrank persisted working truth



\### Examples of UI/session state

\- current tab/page selection

\- unsaved widget inputs

\- expanded/collapsed sections

\- selected table row in the UI

\- local filters/sorts/search terms

\- temporary preview data before explicit save

\- transient edit buffers

\- non-committed form state

\- presentation-only toggles



\### What UI/session state is not

UI/session state is \*\*not\*\*:

\- the persisted workflow lifecycle

\- the source of current run identity

\- the authority on lock ownership

\- the source of review eligibility

\- the source of published status

\- safe to trust after reload unless reconciled to persisted truth



\### Ownership rule

UI/session state belongs to the presentation layer only.



\### Persistence rule

UI/session state does not need to persist unless explicitly promoted into committed working state through a governed save/commit action.



\### Must never happen

\- session variables treated as the source of lifecycle truth

\- stale widget values overwriting reloaded persisted data

\- route/open behavior trusting last-screen memory instead of persisted run/revision state

\- UI-only selection state being mistaken for committed analyst decisions



\---



\## Classification of core model objects



\### Canonical working-state objects

These are primary mutable truth objects:

\- `Run`

\- current `Working Revision`

\- `Planned Sample Set Line`

\- mutable portions of `Raw Upload Batch` usage state

\- `Raw Instrument Row` plus analyst usability decisions

\- mutable match-resolution decisions

\- mutable labels, exclusions, notes, and workflow annotations

\- active `Lock Record`

\- current mutable review handoff state while the revision is still in workflow



\### Derived-state objects

These are recalculable support objects:

\- `Match Mapping`

\- `Resolved Sample Row`

\- `Derived Result Set`

\- progress summaries

\- route/open recommendations

\- queue membership

\- validation summaries

\- publish-readiness evaluations

\- reviewer queue views

\- list-page/status summaries



\### Evidence-state objects

These are durable traceability/freeze objects:

\- `Audit Event`

\- `Review / Signoff Event`

\- admin override records

\- lock recovery history

\- raw source provenance

\- criteria provenance

\- `Published Evidence Package`

\- publish manifest

\- approved frozen snapshot

\- lineage references between revisions and published packages



\### UI/session-state objects

These should remain presentation memory only:

\- local page state

\- widget buffers

\- unsaved editor rows prior to commit

\- temporary filters/sorts

\- display preferences

\- temporary selection/highlight state

\- pre-commit preview calculations not yet accepted into committed workflow state



\---



\## A subtle but important rule about mixed objects

Some objects contain both working and evidence aspects.  

Do not classify the whole object carelessly.



\### Example: Lock Record

\- active current lock status functions as working/control state

\- released/override/stale history becomes evidence once recorded



\### Example: Review workflow

\- “ready for review” or “in review” status is working/lifecycle truth

\- the claimed/reviewed/returned/approved events themselves are evidence



\### Example: Raw upload

\- current imported rows available for workflow are part of working truth

\- the fact that a specific file was imported by a specific user at a specific time is provenance evidence



\### Example: Published snapshot

\- once approved/published, the frozen snapshot is evidence

\- if a run must re-enter workflow, the system creates a new working revision derived from that evidence rather than converting the evidence back into mutable state in place



This means the system must be able to classify at the \*\*field and event level\*\*, not only the table/object level, when necessary.



\---



\## Truth hierarchy when states conflict

When there is disagreement, the system should trust state in this order:



1\. \*\*Evidence state\*\* for historical proof of what was approved, published, or done

2\. \*\*Committed working state\*\* for the current mutable workflow truth

3\. \*\*Freshly recomputed derived state\*\* built from current working truth

4\. \*\*UI/session state\*\* only for unsaved interaction memory



Important nuance:

\- evidence state does not replace current working truth for editable operations

\- working state does not override published evidence about what happened historically

\- derived state never outranks either

\- UI/session state outranks nothing



\---



\## What must persist across sessions

The bootstrap is clear that the following must persist across sessions:



\- committed working revision state

\- run identity

\- revision lineage

\- review history

\- lock/recovery metadata

\- criteria version used

\- publish artifacts

\- audit trail



These persistence requirements come from the workflow, not from implementation convenience. :contentReference\[oaicite:3]{index=3}



\---



\## What may be safely recomputed

The bootstrap also clearly identifies state that can be safely recomputed:



\- progress labels

\- queue membership

\- derived calculation tables

\- presentation summaries

\- route/open recommendations



These are useful, but they must not become independent truth. :contentReference\[oaicite:4]{index=4}



\---



\## Save / commit / freeze rules



\### Save / Commit

A save or commit action promotes valid UI/session edits into committed working state.



\### Recompute

A recompute action refreshes derived state from committed working inputs plus governed configuration.



\### Freeze

A publish/freeze action converts approved working truth plus required provenance into immutable evidence state.



\### Reopen

A reopen action does not “unfreeze” evidence.  

It creates a new working revision with lineage back to the frozen evidence state.



\---



\## Failure-prevention rules



\### Rule 1 — No duplication of authority

Do not store the same workflow truth in multiple competing places.



\### Rule 2 — Derived state must stay subordinate

If derived state disagrees with committed working truth, derived state is wrong or stale.



\### Rule 3 — UI memory is never authoritative

Unsaved UI state may be useful, but it must lose to committed persisted state after reload/open/recovery.



\### Rule 4 — Evidence must survive intact

Audit, review, publish, override, and criteria provenance records must not be silently overwritten.



\### Rule 5 — Published is a one-way freeze for that revision

After publish, the revision’s evidence is historical truth. Any later work occurs on a new revision.



\### Rule 6 — Mixed objects require discipline

If one object contains both workflow-control fields and historical evidence, the system must treat those parts according to their correct class.



\---



\## Practical classification tests



\### Test for Working State

Ask:

\- can a user still intentionally edit this as part of the current revision?

\- does losing it change the current workflow truth?

\- is it needed for save/resume and current routing?



If yes, it is probably working state.



\### Test for Derived State

Ask:

\- can this be recreated from committed inputs?

\- would recomputing it be acceptable and expected?

\- is it mainly a summary, recommendation, result, or queue view?



If yes, it is probably derived state.



\### Test for Evidence State

Ask:

\- does this prove something historical, approved, published, or governed?

\- would overwriting it damage auditability or lineage?

\- must it remain stable even after new revisions exist?



If yes, it is probably evidence state.



\### Test for UI / Session State

Ask:

\- is this mainly here to help the current screen behave?

\- would a refresh/rerun normally wipe it out unless explicitly saved?

\- is it not yet committed to the workflow model?



If yes, it is probably UI/session state.



\---



\## Notes for the agent

\- Be suspicious any time a status summary, queue label, or route decision starts behaving like source truth.

\- Be suspicious any time a widget value survives longer than the persisted truth it came from.

\- Be suspicious any time a published object is treated as editable rather than lineage-bearing evidence.

\- Keep this document aligned with `DATA\_MODEL.md`, `WORKFLOW\_TIMELINE.md`, ADRs on persistence/locking/reopen, and the release tests that verify save/resume, routing, publish freeze, and reopen behavior.

