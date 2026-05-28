\# DATA\_MODEL



\## Purpose of this document

Define the core entities, ownership boundaries, identifiers, required fields, allowed states, and relationships that make the workflow deterministic.



This document is written from the new bootstrap questionnaire and updated workflow. Its purpose is not to mirror the current code structure. Its purpose is to define the real data truth of the system so implementation can remain disciplined and prior lifecycle failures do not repeat.



\---



\## Guided fill status

\- Status: Complete

\- Last reviewed by: project owner + AI

\- Source of truth for this draft: latest `BOOTSTRAP\_QUESTIONNAIRE.md`



\---



\## Modeling principles



\### 1. Separate lifecycle identity from mutable working content

A `Run` is the durable identity and lineage anchor for a lab workflow instance.  

A `Working Revision` is the current mutable branch of that run.



They are related, but they are not the same object.



\### 2. The planned sample set is a first-class source object

The workflow begins with the planned sample set. It must be modeled as explicit working truth, not as a temporary editor surface or post-upload cleanup structure.



\### 3. Raw upload provenance matters, but raw upload is not the only truth

Raw instrument rows enter the workflow as governed source inputs. They must retain provenance and operator handling history, but they do not replace planned workflow truth.



\### 4. Derived data must not become silent source truth

Matching outputs, progress labels, queue eligibility, results tables, readiness checks, and route destinations are derived from committed state. They may be cached, but they must not become the canonical source of truth.



\### 5. Evidence must be immutable

Published artifacts, signoff history, criteria provenance, and approved frozen snapshots are evidence-state objects. They must never be silently overwritten.



\### 6. UI session memory is not the model

The data model assumes persisted workflow state is authoritative. UI/session state is temporary presentation memory only.



\### 7. Reopen means new revision, never in-place published edits

If a published run must re-enter workflow, the system creates a new working revision with explicit lineage to the published source revision.



\---



\## Core entities



\### 1. Run



\#### What it is

The durable identity anchor for a lab workflow instance.



A run groups all revisions, lifecycle history, publish packages, and audit lineage under one business identity.



\#### What identifies it

\- `run\_id`



\#### Required fields

\- `run\_id`

\- `display\_id` or lab-facing identifier if different from internal `run\_id`

\- `created\_at`

\- `created\_by`

\- `current\_revision\_id`

\- `run\_status`

\- `run\_year` or archival bucket if foldered by year

\- `source\_context` if required for intake lineage



\#### Optional fields

\- external/LIMS identifier

\- project or method label

\- notes / operator-facing description

\- archive / retirement flags



\#### Ownership

\- system-owned identity and control object

\- some metadata may be user-supplied at creation

\- status transitions only through governed workflow actions



\#### Allowed states

\- `Draft`

\- `Ready for Review`

\- `In Review`

\- `Needs Rework`

\- `Approved`

\- `Published`



\#### Must never happen

\- two unrelated runs sharing the same `run\_id`

\- lifecycle state stored only in UI memory

\- ambiguous “current run” that cannot be tied to a persisted `run\_id`



\#### Notes

`Run` is the container and lineage root. Mutable scientific/editor content belongs to the current working revision, not directly to the run.



\---



\### 2. Working Revision



\#### What it is

The mutable branch of work for a run.



This is the object analysts edit, reviewers act on, locks protect, and save/resume restores.



\#### What identifies it

\- `revision\_id`



\#### Required fields

\- `revision\_id`

\- `run\_id`

\- `revision\_number` or ordered lineage position

\- `revision\_status`

\- `created\_at`

\- `created\_by`

\- `based\_on\_revision\_id` if derived from a published source

\- `working\_state\_version`

\- `is\_current\_revision`



\#### Optional fields

\- reopen reason

\- recovery reason

\- revision label

\- superseded\_at

\- superseded\_by\_revision\_id



\#### Ownership

\- system creates and controls lineage

\- analyst edits the mutable content inside the revision

\- admin may create a new revision from published evidence via governed reopen



\#### Allowed states

\- `Draft`

\- `Ready for Review`

\- `In Review`

\- `Needs Rework`

\- `Approved`

\- `Published` as the state at which the revision’s evidence package is frozen



\#### Must never happen

\- more than one active mutable current revision for the same run without explicit versioning intent

\- reopening a published revision by mutating the original published one

\- review/publish actions referencing a revision that is not the persisted current target for the run



\#### Notes

This is the object most likely to be confused with the run itself. The model must keep them distinct.



\---



\### 3. Planned Sample Set Line



\#### What it is

One planned line in the pre-run sample set.



This is the first real workflow artifact and the anchor for later matching and review.



\#### What identifies it

\- `sample\_plan\_line\_id`



\#### Required fields

\- `sample\_plan\_line\_id`

\- `revision\_id`

\- `line\_order`

\- `sample\_type`

\- `sample\_identifier` or planned sample label

\- `exclude\_flag`

\- `created\_at`

\- `updated\_at`



\#### Common fields

\- category / label

\- pairing expectation

\- target or concentration expectation

\- dilution factor

\- filtered volume

\- extracted volume

\- total area

\- sub-volume

\- analyst notes

\- planning notes

\- required metadata flags



\#### Ownership

\- analyst-edited working state

\- system preserves line order and identity

\- reviewers inspect but do not silently mutate without governed workflow action



\#### Allowed states

\- active

\- excluded

\- superseded by later saved edit within same revision



\#### Must never happen

\- plan lines existing only as transient widget rows

\- matching depending on a plan that was never committed

\- silent row reorder that changes matching meaning without auditability



\#### Notes

One plan line is not the same thing as one raw row. The whole point of modeling this separately is to stop post-upload confusion from becoming structural again.



\---



\### 4. Raw Upload Batch



\#### What it is

A provenance object representing one imported raw source file or batch import event.



\#### What identifies it

\- `raw\_upload\_batch\_id`



\#### Required fields

\- `raw\_upload\_batch\_id`

\- `revision\_id`

\- `imported\_at`

\- `imported\_by`

\- `source\_filename`

\- `source\_file\_hash` if available

\- `parse\_status`



\#### Optional fields

\- instrument type

\- file size

\- parser version

\- import warnings

\- import notes



\#### Ownership

\- system-owned provenance record with analyst-triggered creation



\#### Allowed states

\- imported

\- parse warning

\- parse failed

\- superseded by later re-import if workflow allows



\#### Must never happen

\- raw uploads with no link to revision

\- later inability to tell which file produced which working data

\- parse failure silently producing partial truth without flagging



\---



\### 5. Raw Instrument Row



\#### What it is

One parsed raw input row belonging to an uploaded raw batch.



\#### What identifies it

\- `raw\_row\_id`



\#### Required fields

\- `raw\_row\_id`

\- `raw\_upload\_batch\_id`

\- `revision\_id`

\- `row\_order`

\- raw source payload or normalized parsed fields

\- `row\_status`



\#### Common fields

\- sample name / instrument label

\- acquisition order / timestamp if present

\- measured values from source

\- parse warnings

\- operator drop/exclude flags

\- drop/exclude reason if required



\#### Ownership

\- system preserves source payload/provenance

\- analyst may mark usability decisions such as drop/exclude

\- raw source values themselves should not be silently rewritten



\#### Allowed states

\- available

\- dropped

\- excluded from matching

\- parse warning

\- unmatched

\- matched



\#### Must never happen

\- operator usability decisions destroying the original raw provenance

\- raw rows detached from their upload batch

\- source payload rewritten without audit trace



\---



\### 6. Match Mapping



\#### What it is

The deterministic association between planned sample set lines and surviving raw instrument rows.



This is where the workflow bridges pre-run plan and uploaded reality.



\#### What identifies it

\- `match\_mapping\_id`



\#### Required fields

\- `match\_mapping\_id`

\- `revision\_id`

\- `sample\_plan\_line\_id`

\- mapping status

\- mapping algorithm/version

\- created\_at or recomputed\_at



\#### Common fields

\- one or more linked `raw\_row\_id` values

\- pair/group metadata

\- mismatch flags

\- warning codes

\- unresolved reason

\- operator-confirmed override or resolution note if needed



\#### Ownership

\- system-derived from committed working truth

\- analyst may resolve mismatch conditions through governed upstream edits or explicit resolution actions



\#### Allowed states

\- matched

\- partially matched

\- unmatched

\- mismatch warning

\- resolved after analyst intervention



\#### Must never happen

\- match outputs becoming independent source truth

\- two conflicting active mappings for the same plan line without explicit model support

\- rematch consuming unsaved UI edits instead of committed persisted upstream state



\#### Notes

This object exists specifically to stop “matching” from disappearing into ad hoc helper code.



\---



\### 7. Resolved Sample Row



\#### What it is

The workflow-ready row produced from a committed plan line plus its accepted raw mapping plus any governed metadata needed for downstream review/calculation.



\#### What identifies it

\- `resolved\_sample\_row\_id`



\#### Required fields

\- `resolved\_sample\_row\_id`

\- `revision\_id`

\- `sample\_plan\_line\_id`

\- resolved status



\#### Common fields

\- normalized sample identity

\- resolved pair/group references

\- labels/categories

\- calculation-ready metadata

\- warnings

\- human notes carried forward



\#### Ownership

\- system-derived from working truth

\- may be cached for review UX

\- not canonical source truth by itself



\#### Allowed states

\- ready

\- warning

\- blocked

\- excluded



\#### Must never happen

\- resolved rows being edited as if they are primary source truth without writing back to the governed upstream object



\---



\### 8. Derived Result Set



\#### What it is

Any recalculable calculation output built from the committed working revision and governed criteria/config.



Examples:

\- pairing audit

\- validation summaries

\- results table

\- readiness checks

\- progress summaries

\- queue eligibility

\- publish-readiness evaluation



\#### What identifies it

\- `derived\_result\_set\_id` or typed derived artifact key



\#### Required fields

\- `revision\_id`

\- `derived\_type`

\- `derived\_from\_version`

\- recompute timestamp if persisted/cache-backed



\#### Ownership

\- system-derived only



\#### Allowed states

\- current

\- stale

\- invalidated

\- recomputed



\#### Must never happen

\- derived results silently replacing source truth

\- old cached derived tables surviving after working state changed without invalidation

\- route/open logic using stale derived outputs when persisted workflow truth disagrees



\#### Notes

This is the zone where many previous failures hid. The model should treat derived data as disposable and recomputable unless explicitly frozen as evidence.



\---



\### 9. Review Assignment / Review Decision



\#### What it is

The record of review claim, active reviewer, review outcome, and rework/approval decisions for a revision.



\#### What identifies it

\- `review\_event\_id` or `review\_assignment\_id`



\#### Required fields

\- `revision\_id`

\- `reviewer\_user\_id`

\- `review\_state`

\- `claimed\_at`

\- outcome timestamp when finished

\- outcome type



\#### Common fields

\- return-for-rework reason

\- approval note

\- claim source

\- review lock metadata



\#### Ownership

\- system-created from eligible user actions

\- reviewer supplies review outcome and rationale

\- reviewer identity must be durable and auditable



\#### Allowed states

\- claimable

\- claimed

\- returned for rework

\- approved

\- released/abandoned only through governed recovery logic if needed



\#### Must never happen

\- reviewer approving a revision they authored as primary analyst

\- review state existing only as a queue label without durable identity

\- ambiguous “someone reviewed this” with no actor/timestamp trail



\---



\### 10. Published Evidence Package



\#### What it is

The immutable published artifact set for a specific approved revision.



This is the frozen evidence object, not merely a folder of exports.



\#### What identifies it

\- `published\_package\_id`



\#### Required fields

\- `published\_package\_id`

\- `run\_id`

\- `revision\_id`

\- `published\_at`

\- `published\_by`

\- package status / integrity status

\- manifest reference



\#### Required contents

\- approved frozen snapshot

\- exported result files

\- summary report(s)

\- signoff/review log

\- criteria provenance bundle

\- published manifest

\- audit references or embedded audit trail as designed



\#### Ownership

\- system-created under approved user action

\- immutable once published



\#### Allowed states

\- published

\- integrity-verified

\- damaged/invalid for reopen validation

\- superseded only by later separate published revisions, never overwritten in place



\#### Must never happen

\- published evidence being editable in place

\- package contents drifting from the approved revision they claim to represent

\- later revisions overwriting earlier evidence instead of existing alongside lineage



\---



\### 11. Lock Record



\#### What it is

The concurrency control object protecting a working revision from simultaneous active editing.



\#### What identifies it

\- `lock\_id`



\#### Required fields

\- `lock\_id`

\- `run\_id`

\- `revision\_id`

\- `lock\_owner`

\- `acquired\_at`

\- `lock\_status`



\#### Common fields

\- heartbeat timestamp

\- `released\_at`

\- `override\_by`

\- `override\_reason`

\- `override\_at`

\- workstation identity



\#### Ownership

\- system-managed

\- admin override is governed and audited



\#### Allowed states

\- Active

\- Released

\- Stale

\- Overridden



\#### Must never happen

\- multiple active edit locks on one working revision

\- stale lock with no governed recovery path

\- lock state inferred only from UI session rather than durable coordination state



\---



\### 12. Criteria Configuration



\#### What it is

The governed threshold/configuration object used by review, validation, and publish decisions.



\#### What identifies it

\- `criteria\_version\_id`



\#### Required fields

\- `criteria\_version\_id`

\- version label

\- effective date

\- threshold values / rule definitions

\- `created\_by`

\- `created\_at`



\#### Optional fields

\- approval metadata

\- retired flag

\- replacement version reference

\- config notes



\#### Ownership

\- admin/governed configuration only



\#### Allowed states

\- draft config if governance allows

\- active

\- retired

\- superseded



\#### Must never happen

\- analysts silently editing thresholds inside run data

\- published evidence lacking the criteria version that governed its outputs



\---



\### 13. User Identity



\#### What it is

The durable identity reference for analyst, reviewer, admin, and recovery actions.



\#### What identifies it

\- `user\_id`



\#### Required fields

\- `user\_id`

\- display name

\- active status



\#### Common fields

\- role

\- permission set

\- workstation identity linkage

\- admin eligibility

\- review eligibility



\#### Ownership

\- admin/system-managed depending on deployment posture



\#### Must never happen

\- protected actions with no recorded actor

\- review independence checks performed against display text only if a stronger identity is available



\---



\### 14. Audit Event



\#### What it is

The append-only record of meaningful workflow actions and protected events.



\#### What identifies it

\- `audit\_event\_id`



\#### Required fields

\- `audit\_event\_id`

\- `object\_type`

\- `object\_id`

\- `action`

\- `actor`

\- `timestamp`



\#### Common fields

\- before/after summary or structured delta

\- reason if required

\- source workstation/session

\- related revision/package/lock identifiers



\#### Ownership

\- append-only system evidence



\#### Must never happen

\- meaningful lifecycle transitions with no audit event

\- recovery/protected actions without reason capture where required

\- mutable audit history without explicit governance



\---



\## Relationships



\### Identity and lineage

\- One `Run` has one or more `Working Revision` records over time.

\- One `Working Revision` belongs to exactly one `Run`.

\- A later `Working Revision` may be based on one earlier published revision.



\### Planning and upload

\- One `Working Revision` has many `Planned Sample Set Line` records.

\- One `Working Revision` has zero or more `Raw Upload Batch` records.

\- One `Raw Upload Batch` has many `Raw Instrument Row` records.



\### Matching and resolution

\- One `Working Revision` has many `Match Mapping` records.

\- One `Match Mapping` links one planned line to one or more raw rows depending on workflow rules.

\- One `Working Revision` has many `Resolved Sample Row` records derived from plan + raw + mapping state.



\### Review and publish

\- One `Working Revision` may have many `Review Assignment / Review Decision` events over its lifecycle, but only one active review claim at a time.

\- One approved `Working Revision` may produce one `Published Evidence Package` per publish action for that revision model.

\- One `Published Evidence Package` belongs to exactly one `Run` and one `Revision`.



\### Concurrency and governance

\- One `Working Revision` may have at most one active `Lock Record`.

\- One `Published Evidence Package` captures exactly one `Criteria Configuration` version as provenance.

\- Many `Audit Event` records may reference the same run, revision, lock, or package.



\---



\## Source-of-truth boundaries



\### Canonical working truth

Canonical mutable workflow truth is:

\- `Run`

\- current `Working Revision`

\- `Planned Sample Set Line`

\- `Raw Upload Batch`

\- `Raw Instrument Row`

\- analyst-controlled inclusion/exclusion decisions

\- governed workflow metadata

\- durable review/lock/control metadata



\### Derived but not canonical

These may be recomputed and must not become independent truth:

\- route/open destination

\- current workflow step label

\- matching summaries

\- pairing audits

\- queue membership

\- publish readiness summaries

\- calculation tables

\- presentation summaries



\### Evidence truth

These must be frozen and immutable once published:

\- published package manifest

\- approved frozen snapshot

\- exported result files

\- signoff/review log

\- criteria provenance

\- published summary outputs

\- audit evidence relevant to the revision



\---



\## Failure-prevention rules baked into the model



\### Preventing workflow-truth drift

Do not store workflow truth in multiple competing places.  

The persisted run/revision state must be the authority used by summary, landing, open/resume, review eligibility, and publish gating.



\### Preventing stale session overwrite

Do not treat session widget values as authoritative after load/reopen.  

Committed persisted state wins.



\### Preventing matching ambiguity

Do not let matching depend on invisible editor state.  

Matching consumes committed plan lines plus committed raw-row usability state.



\### Preventing duplicate identity errors

Do not let display labels substitute for unique run/revision identifiers.



\### Preventing published mutation

Do not reopen by altering published package contents.  

Always create a new working revision with lineage.



\### Preventing derived-truth creep

Do not elevate cached results tables, progress summaries, or queue labels into source truth just because they are convenient to display.



\### Preventing audit gaps

Every protected transition should resolve to durable audit evidence with actor and timestamp.



\---



\## Persistence posture

The data model assumes:

\- active working truth persists in structured embedded persistence

\- run control metadata and event/audit metadata are durable

\- evidence artifacts are packaged separately as immutable published outputs

\- route/resume can be reconstructed from persisted truth without relying on remembered UI state



\---



\## Notes for the agent

\- Model the workflow the lab actually runs, not just the current screen layout.

\- Keep run identity, revision identity, and published evidence identity separate.

\- Be suspicious of any field that mixes working truth, derived truth, and evidence truth in one place.

\- If a future implementation wants to cache or denormalize data for UX speed, it must not blur these ownership lines.

