BOOTSTRAP QUESTIONNAIRE — AI-Guided Project Intake

Purpose



This document is the entry point for all new projects.



It is a guided conversation between the user and the AI that produces the foundational planning documents required for professional-grade development.



The goal is not speed.



The goal is:



clarity

structure

completeness

preventing architectural drift

preventing premature coding

AI INSTRUCTIONS (MANDATORY)



You must follow these rules:



DO NOT START CODING

No code, no file structures, no module design.

This phase is planning only.

WORK IN PHASES

Do not jump ahead.

Complete each phase before moving on.

EVALUATE ANSWERS

For each section, classify responses as:

COMPLETE

WEAK (needs refinement)

MISSING (blocking)

GUIDE, DO NOT INTERROGATE

Ask follow-up questions

Provide examples if needed

Help the user think, not just answer

DO NOT ASSUME

If something is unclear, ask

If something is missing, flag it

MAP OUTPUTS

Each phase feeds a specific document.

You should tell the user when enough information exists to draft it.

PHASE 1 — PROJECT PURPOSE



Target: PROJECT\_BRIEF.md



Core problem



What problem are you trying to solve?

Build a dependable lab workflow application that replaces brittle spreadsheet-driven run handling with a governed, resumable, reviewable system. The prior application proved there is real value in guided workflow, save/resume, role separation, and publish/reopen discipline, but it also exposed that workflow truth, routing, persistence semantics, and recovery behavior were not modeled tightly enough to remain stable under continued feature work. The new project must preserve the operational wins while rebuilding the system on clearer planning, stronger state boundaries, and safer lifecycle control.



Who are the primary users?



Primary analyst / operator

Secondary reviewer

Project lead / admin

Support owner / recovery operator



What do they currently do without this tool?

They rely on spreadsheets and ad hoc recovery behavior for run tracking, editing, QA/review handoff, and evidence generation. This creates brittleness around protected cells, inconsistent recovery behavior, weak traceability, and ambiguity around who changed what and when.



What is painful, slow, risky, or confusing today?

The pain is not just manual work. The true risk is lifecycle drift when workflow truth is inferred in multiple places. Prior failures included:



nondeterministic save/resume behavior

route/open drift

stale session state overriding persisted truth

duplicate run identity collisions

fragile publish/reopen behavior

inability to delete drafts before publish

inability to cleanly push published data back down into review or primary when controlled data reloads are required



These are not surface bugs. They threaten confidence in the run lifecycle itself.



What decision does this tool help make faster or safer?

It helps users decide whether a run is:



correctly planned

correctly matched

ready for review

approved

publishable

or in need of rework



It makes those decisions safer by enforcing workflow state, reviewer independence, auditability, and controlled recovery.



Scope control



What is OUT OF SCOPE for version 1?



simultaneous co-editing on the same run

internet-hosted SaaS deployment

enterprise SSO as a prerequisite

direct instrument integration

major scientific-method redesign

editing published evidence in place



What would be nice to have but not required?



future portability to a different UI layer

broader collaboration features

richer admin tooling

larger enterprise deployment patterns

more advanced workflow analytics

wider cross-project reuse beyond the first successful implementation

Success definition



How would you know this project is successful?

Success means the new build preserves the workflow value of the old application while removing the architectural ambiguity that made later changes unsafe. Specifically:



deterministic save/resume

one authoritative workflow-progress model

stable review handoff

immutable evidence packaging

safe reopen-by-new-revision only

auditable recovery paths

deletion or controlled disposal of drafts before publish

controlled reload flow from published evidence back into lower workflow stages when appropriate

release gates that catch workflow regressions before merge



What improves?



speed

accuracy

consistency

traceability

recoverability

confidence in lifecycle correctness

Classification

Problem clarity: COMPLETE

User clarity: COMPLETE

Scope boundaries: COMPLETE

Success definition: COMPLETE

PHASE 2 — WORKFLOW REALITY



Target: WORKFLOW\_TIMELINE.md



Entry point



What enters the system first?

The planned sample set enters the system first, not the raw upload. The workflow must begin from the pre-run planning artifact, because forcing planning after raw upload created structural confusion in the prior system.



Where does it come from?

From analyst-prepared run planning information:



intended sample set

expected rows

pairing expectations

categories / labels

exclusions

metadata required before upload and matching



Who interacts with it first?

Primary analyst / operator.



Step-by-step flow

Analyst creates or opens a run.

Analyst creates, imports, or verifies the planned sample set.

Raw instrument rows are uploaded or imported.

Raw rows may be excluded for miss injection, bad injection, or documented human/instrument error.

The system performs deterministic matching between uploaded rows and the pre-run plan.

The analyst reviews a matching preview and resolves mismatches, exclusions, or metadata issues.

The system derives calculations, resolved tables, and review-ready outputs from committed workflow state.

The analyst performs primary QA and either saves draft progress or submits the run for review.

The reviewer independently claims eligible work, reviews it, and either returns it for rework or approves it.

The approved run is published into an immutable evidence package.

If later correction is needed, reopen creates a new working revision from published evidence. The published artifact itself is never edited in place.

Human vs system work



What steps are manual?



sample planning

mismatch resolution

exclusions

metadata correction

QA judgment

review judgment

admin override / recovery actions



What steps are automated?



matching logic

derived calculations

workflow progress determination

route/resume logic

lock handling

artifact packaging

publish validation

guarded state transitions

Decision points



Where do decisions happen?



run creation / open

sample-plan commit

upload / match validation

analyst QA

submit-for-review

reviewer claim / approve / return-for-rework

publish validation

admin-controlled recovery / reopen



What gets reviewed?

The committed workflow state, resolved sample rows, calculation outputs, metadata consistency, and any required publish artifacts.



Who reviews it?

A secondary reviewer independent from the primary analyst.



What determines approval?



reviewer independence

valid workflow state

complete required artifacts

no unresolved blocking issues

publish prerequisites satisfied

End state



What is the final output?

A published, immutable run evidence package containing:



the approved working snapshot

exported result files

summary report(s)

manifest metadata

signoff / review record

audit trail or audit references

criteria provenance used for the approved output



What leaves the system?

Operator-facing outputs such as CSV, XLSX, PDF, reports, or approved downstream deliverables may leave the system, but the full published evidence package remains the governed archive and source for any future controlled revision or reload workflow.



Classification

Clear start: COMPLETE

Clear sequence: COMPLETE

Clear human vs system actions: COMPLETE

Clear end state: COMPLETE

PHASE 3 — DATA MODEL



Target: DATA\_MODEL.md



Main entities



The main entities in the system are:



Run

Working Revision

Planned Sample Set Line

Raw Instrument Row

Match Mapping

Resolved Sample Row

Derived Result Set

Review / Signoff Event

Published Evidence Package

Lock Record

Criteria Configuration

User Identity

Audit Event

Entity detail

1\. Run



What identifies it?



run\_id (primary business identifier)



Fields



run\_id

lims\_id or external identifier if applicable

created\_at

created\_by

current\_status

current\_revision\_id

primary\_analyst

current\_reviewer

publish\_count

last\_activity\_at



Required fields



run\_id

created\_at

created\_by

current\_status



Fields that change over time



current\_status

current\_revision\_id

current\_reviewer

publish\_count

last\_activity\_at



Ownership



system-generated: identifiers, timestamps, lifecycle pointers

user-assigned/admin-assigned: analyst/reviewer role assignment where applicable



Allowed states



Draft

Ready for Review

In Review

Needs Rework

Approved

Published

Archived (optional later-state if adopted)



Allowed transitions



Draft → Ready for Review

Ready for Review → In Review

In Review → Needs Rework

Needs Rework → Ready for Review

In Review → Approved

Approved → Published

Published → new Working Revision via controlled reopen



Must never happen



duplicate run\_id silently creating or overwriting a real run

Published → Draft by direct rollback

multiple active working revisions at the same time for one run

2\. Working Revision



What identifies it?



revision\_id



Fields



revision\_id

run\_id

revision\_number

parent\_published\_revision\_id

revision\_reason

status

created\_at

created\_by

approved\_at

approved\_by

published\_at

published\_by

snapshot\_reference



Required fields



revision\_id

run\_id

revision\_number

status

created\_at

created\_by



Fields that change over time



status

approved\_at

approved\_by

published\_at

published\_by

snapshot\_reference



Ownership



system-generated: revision numbering, timestamps, linkage

user/admin-entered: revision reason

system-controlled lifecycle fields



Allowed states



Draft

Submitted

In Review

Rework

Approved

Published

Superseded



Must never happen



editing a published revision in place

orphan revision with no parent run

two active Draft/Rework revisions for the same run at once

3\. Planned Sample Set Line



What identifies it?



planned\_line\_id



Fields



planned\_line\_id

run\_id

revision\_id

sequence\_number

sample\_id

sample\_type

pair\_group

category\_label

is\_excluded

exclusion\_reason

volume\_filtered

volume\_extracted

notes



Required fields



planned\_line\_id

run\_id

revision\_id

sequence\_number

sample\_id

sample\_type



Fields that change over time



exclusion fields

category/label fields

notes

planning metadata until committed



Ownership



primarily user-entered

some system-normalized fields allowed



Allowed states



Draft

Committed

Excluded



Must never happen



uncommitted editor state being treated as canonical truth

silent resequencing without audit or explicit intent

4\. Raw Instrument Row



What identifies it?



raw\_row\_id



Fields



raw\_row\_id

run\_id

revision\_id

source\_file\_name

source\_file\_hash

imported\_at

instrument\_sequence

instrument\_sample\_name

raw measured columns

is\_excluded

exclusion\_reason



Required fields



raw\_row\_id

run\_id

source\_file\_name

source\_file\_hash

imported\_at



Fields that change over time



exclusion flags only

raw measurement values themselves must not mutate after import capture



Ownership



system-generated provenance

user may set exclusion status with reason



Must never happen



silent mutation of imported raw evidence

loss of source provenance

5\. Match Mapping



What identifies it?



match\_id



Fields



match\_id

run\_id

revision\_id

planned\_line\_id

raw\_row\_id

match\_status

match\_reason

resolved\_by

resolved\_at



Required fields



match\_id

run\_id

revision\_id

match\_status



Fields that change over time



match\_status

match\_reason

resolution metadata



Ownership



system-suggested

user-confirmed or user-corrected

final committed state controlled by workflow rules



Allowed states



Unmatched

Matched

Excluded

Conflict

Needs Review



Must never happen



nondeterministic rematch without user action or explicit recompute rule

6\. Resolved Sample Row



What identifies it?



resolved\_row\_id



Fields



resolved\_row\_id

run\_id

revision\_id

planned\_line\_id

raw\_row\_id

final sample labels

resolved metadata

notes

workflow flags



Required fields



identifiers linking back to plan and/or raw rows

resolved label set needed for downstream results



Fields that change over time



user corrections

workflow annotations

notes

exclusions until locked by approval/publish



Ownership



mixed: user-entered and system-derived support fields

7\. Derived Result Set



What identifies it?



result\_set\_id



Fields



result\_set\_id

run\_id

revision\_id

derived calculation tables

result summaries

validation summaries

generation timestamp



Required fields



result\_set\_id

run\_id

revision\_id

generation metadata



Ownership



system-derived only



Must never happen



user-edited derived results becoming canonical truth

8\. Review / Signoff Event



What identifies it?



review\_event\_id



Fields



review\_event\_id

run\_id

revision\_id

event\_type

actor

timestamp

comment

decision\_reason



Required fields



review\_event\_id

run\_id

revision\_id

event\_type

actor

timestamp



Allowed event types



submitted\_for\_review

claimed\_for\_review

returned\_for\_rework

approved

published

reopened\_from\_published

admin\_override



Ownership



append-only system/event log with user-authored comments where applicable



Must never happen



review history overwrite

self-review accepted where reviewer independence is required

9\. Published Evidence Package



What identifies it?



published\_package\_id



Fields



published\_package\_id

run\_id

revision\_id

manifest

approved snapshot reference

export references

signoff record

criteria provenance

package timestamp

package hash if implemented



Required fields



published\_package\_id

run\_id

revision\_id

manifest

package timestamp



Ownership



system-generated and immutable after publish



Must never happen



in-place mutation after publish

publish with incomplete provenance

10\. Lock Record



What identifies it?



lock\_id



Fields



lock\_id

run\_id

revision\_id

lock\_owner

acquired\_at

released\_at

lock\_status

override\_by

override\_reason

override\_at



Required fields



lock\_id

run\_id

lock\_owner

acquired\_at

lock\_status



Allowed states



Active

Released

Stale

Overridden



Must never happen



stale lock with no governed recovery path

multiple active edit locks on one working revision

11\. Criteria Configuration



What identifies it?



criteria\_version\_id



Fields



criteria\_version\_id

version label

effective date

threshold values

created\_by

created\_at

approval metadata if governed



Ownership



admin/governed configuration only



Must never happen



analyst silently changing governed thresholds inside run data

12\. User Identity



What identifies it?



user\_id



Fields



user\_id

display name

role

permission set

active status



Ownership



admin/system-managed

13\. Audit Event



What identifies it?



audit\_event\_id



Fields



audit\_event\_id

object\_type

object\_id

action

actor

timestamp

before/after summary or structured delta

reason if required



Ownership



append-only system evidence

Classification

Entities are clearly defined: COMPLETE

Fields are not vague: COMPLETE

Ownership is assigned: COMPLETE

States are logical and complete: COMPLETE

PHASE 4 — STATE CLASSIFICATION



Target: STATE\_CLASSIFICATION.md



Working State



Editable, frequently changing, and tied to the current mutable revision:



planned sample set editor data

match-resolution choices

labels, exclusions, analyst notes

in-progress review-ready draft state

active lock ownership

current workflow interaction state

Derived State



Always recalculable from committed working inputs:



progress summaries

route destination

calculations/results

validation summaries

pairing audits

queue eligibility

publish-readiness checks



Derived state must not become independent truth.



Evidence State



Must be preserved and never silently overwritten:



imported raw source provenance

review/signoff events

admin override events

publish manifest

approved snapshot

immutable published package

audit history

criteria provenance

Persistence thinking



What must persist across sessions?



committed working revision state

run identity

revision lineage

review history

lock/recovery metadata

criteria version used

publish artifacts

audit trail



What can be recomputed safely?



progress labels

queue membership

derived calculation tables

presentation summaries

route/open recommendations

Classification

No duplication of truth: COMPLETE

Derived data is not incorrectly persisted: COMPLETE

Evidence data is protected: COMPLETE

PHASE 5 — ARCHITECTURE SELECTION



Target: ARCHITECTURE\_SELECTION.md + ADRs



Usage model



Single user or multi-user?

Multi-user over time.



Simultaneous users?

Yes, in the broad system, but not simultaneous co-editing of the same working revision.



Version 1 concurrency rule

Single active editor per working revision. Other users may view, queue, review eligible work, or perform governed admin actions depending on permissions.



Environment

must work in a restricted environment

must support offline or local-network operation

must not depend on public internet hosting

must tolerate institutional IT constraints

Deployment



Version 1 posture

Local launcher + thin UI + shared storage.



This means:



the application is launched locally by the user

the working experience is presented through a thin UI

durable state and governed artifacts live in shared storage

the business logic must remain separable from the UI layer so future UI replacement is possible

Requirements

auditability

deterministic lifecycle behavior

safe save/resume

stable route/open behavior

explicit concurrency control

controlled recovery and reopen behavior

modest-to-moderate data sizes

compatibility with restricted IT environments

strong separation between working state, derived state, and evidence state

Evaluate options

UI layer options



Option A — Browser-based thin UI launched locally

Pros:



easier stepwise workflow presentation

easier future portability if UI stays thin

familiar interaction model



Cons:



session behavior must be tightly controlled

can encourage accidental coupling between UI state and workflow truth if not disciplined



Option B — Desktop-native UI

Pros:



more traditional local-app deployment

potentially simpler user mental model



Cons:



usually heavier to build and harder to iterate

can raise cost of future UI replacement



Recommendation

Use a thin locally launched UI, but enforce a hard architectural boundary so workflow truth does not live in UI session state.



Persistence options



Option A — Shared file-based structured artifacts only

Pros:



simple to inspect

easy packaging of evidence



Cons:



can become brittle for live working-state coordination if not modeled carefully



Option B — Embedded relational persistence plus packaged evidence artifacts

Pros:



better lifecycle/state consistency

cleaner handling of current working truth

easier to enforce run/revision integrity



Cons:



more design discipline required

may feel heavier up front



Recommendation

Use embedded structured persistence for active working truth, with packaged evidence artifacts for publish/freeze outputs.



Concurrency options



Option A — Single active editor per run/revision

Pros:



easiest to reason about

strongest protection against silent overwrite

matches the workflow’s reviewed handoff model



Cons:



less collaborative in real time



Option B — Multi-editor conflict resolution

Pros:



more flexible collaboration



Cons:



dramatically higher complexity

much higher risk for version 1



Recommendation

Use single active editor per working revision for version 1.



Session handling options



Option A — UI session holds significant workflow truth

Pros:



quick to prototype



Cons:



directly linked to prior drift failures

resume/load behavior becomes fragile



Option B — Explicit persisted workflow state with minimal UI memory

Pros:



deterministic save/resume

safer route/open behavior

easier recovery and audit reasoning



Cons:



more discipline required up front



Recommendation

Use explicit persisted workflow state as the authority. UI session state should be treated as temporary presentation memory only.



ADR candidates

run identity and revision model

single-authority workflow-progress service

evidence package immutability

single-editor concurrency model

reopen and recovery model

criteria configuration governance model

UI portability boundary

persistence strategy for active truth vs published evidence

Classification

No default assumptions allowed: COMPLETE

Recommendation is justified: COMPLETE

ADR candidates identified: COMPLETE

PHASE 6 — ASSUMPTIONS \& OPEN QUESTIONS



Target: ASSUMPTIONS\_AND\_OPEN\_QUESTIONS.md



Assumptions

the real workflow begins with a planned sample set before upload

one active editor per working revision is acceptable for version 1

reviewer independence is mandatory

published evidence must be immutable

reopen must create a new working revision from published evidence

the environment will remain restricted enough that offline/local-network support is necessary

active workflow truth must not live primarily in UI session state

What could break if these are wrong?

if planning is not truly the first real-world artifact, workflow ordering will be wrong again

if users need real-time co-editing, single-editor locking may become a bottleneck

if deployment needs central hosting sooner than expected, early launch/session choices may need revision

if governed criteria are broader than currently modeled, admin/config design may be incomplete

if users actually require published data to be editable in place, the evidence model will conflict with operations

What needs validation?

whether the pre-run plan is always available before raw upload in real operations

whether single-editor locking is acceptable to actual users under workload pressure

whether the local launcher + thin UI + shared storage model is acceptable to IT

whether old historical data/packages need migration support or can be treated as legacy archive only

whether all required publish artifacts are fully known at project start

What is still unknown?

exact final UI technology

exact embedded persistence engine

exact package structure for published evidence

exact role/permission surface

exact stale-lock recovery policy details

exact artifact schema for draft deletion and controlled reload workflows

Classification

Assumptions explicit: COMPLETE

Risks real: COMPLETE

Unknowns tracked: COMPLETE

PHASE 7 — VERIFICATION \& COMPLETION



Target: TEST\_STRATEGY.md + QUALITY\_GATES.md



What absolutely must work?

deterministic save/resume

save-and-close lock release

correct open/run routing from persisted truth

duplicate run ID protection

reviewer independence and self-review rejection

publish validation and evidence freezing

reopen-from-published creating a new working revision only

stale lock recovery with audited admin override

workflow-progress summary aligned with actual allowed actions

explicit commit behavior on editor-style workflow pages

controlled deletion of drafts before publish

controlled reload from published evidence into lower workflow stages when authorized

What edge cases matter?

None, NaN, and missing-value drift across persistence

damaged or incomplete manifest/artifact packages

stale UI/session values after load

claim/open behavior for review runs

duplicate create attempts

invalid override requests

stale or orphaned locks

old snapshot or legacy state rehydration

widget/rerun overwrite behavior

partial publish artifact creation failure

draft deletion after partial work but before publish

What failure would be unacceptable?



Any failure that causes:



silent data loss

wrong run identity

wrong route/resume destination

mutable published evidence

broken reviewer independence

hidden mismatch between committed truth and displayed truth

unpublished draft state being mistaken for approved/published evidence

When can we say this is done?



This planning phase is done when:



the project brief is coherent

the workflow is complete end-to-end

the data model is specific enough to prevent vague implementation

working, derived, and evidence state are clearly separated

architecture recommendations are justified and ADR candidates are identified

assumptions and unknowns are explicit

verification scenarios are concrete

the resulting docs are strong enough to block premature coding and bad architecture shortcuts

Classification

Test scenarios concrete: COMPLETE

Completion criteria measurable: COMPLETE

FINAL READINESS SUMMARY



This bootstrap is complete enough to draft:



PROJECT\_BRIEF.md

WORKFLOW\_TIMELINE.md

DATA\_MODEL.md

STATE\_CLASSIFICATION.md

ARCHITECTURE\_SELECTION.md

ASSUMPTIONS\_AND\_OPEN\_QUESTIONS.md

TEST\_STRATEGY.md



This bootstrap is also complete enough to identify ADR candidates before implementation begins.

