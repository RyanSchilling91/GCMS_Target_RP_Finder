\# ADR-0002 - Persist Mutable Working State with Version-Aware Rehydration and Keep Published Evidence Separate



\## Status

\- Accepted



\## Decision

Persist mutable working state using file-backed, version-aware snapshots suitable for shared-storage deployment, and require deterministic rehydration of that working state across save/resume and application updates.



Published evidence is not part of this mutable working-state persistence model. Published artifacts remain separate, immutable evidence outputs and must not be treated as resumable working state.



The persistence model must preserve the distinction between:

\- `Run`

\- `Working Revision`

\- mutable working-state snapshot(s)

\- immutable published evidence package(s)



\## Context

The project requires reliable save/resume behavior in a constrained environment. Users must be able to stop work, reopen later, hand work off, and continue from governed persisted truth instead of reconstructing state from transient UI memory.



Earlier project failures showed that persistence bugs are not just storage bugs. They are workflow bugs. If the wrong truth is persisted, restored, or routed from, the system can:

\- reopen at the wrong step

\- restore stale or malformed state

\- silently treat derived or UI state as source truth

\- blur the line between editable work and frozen evidence

\- break handoff, review, or publish lineage



This ADR therefore exists to define the architectural persistence rule, not just an implementation detail.



\## Alternatives considered

\- Central database immediately:

&#x20; - Deferred because the current environment and deployment posture do not yet justify or support the added infrastructure.



\- Stateless sessions only:

&#x20; - Rejected because they would break save/resume, handoff, and governed continuity of workflow.



\- Spreadsheet or ad hoc export persistence:

&#x20; - Rejected because it is fragile, weak for auditability, and too easy to let drift into unmanaged truth.



\## Why chosen

File-backed working-state persistence fits the current environment and supports the project’s actual workflow needs without requiring hosted infrastructure.



Version-aware rehydration is required because save/resume is not enough on its own. If application updates can make old working states unreadable or semantically unstable, the persistence model fails its real purpose.



Separating mutable working-state persistence from immutable published evidence is also essential. The project must support both resumable workflow and defensible archives, and those are not the same thing.



\## Consequences

\- Easier:

&#x20; - The project can support draft save/resume, review handoff, reopen, and deterministic routing in the current deployment model.

&#x20; - Working truth can remain durable without introducing a central database prematurely.



\- Harder:

&#x20; - Persistence changes now require schema/version discipline, compatibility checks, and regression testing.

&#x20; - Rehydration semantics must stay stable enough that saved working truth does not silently drift after upgrades.



\- Requires:

&#x20; - Working-state snapshots must carry explicit schema or version metadata.

&#x20; - Rehydration must restore governed working truth in canonical form.

&#x20; - Unsupported or incompatible snapshots must fail clearly rather than partially loading corrupted or ambiguous state.

&#x20; - Persistence and rehydration tests must cover real workflow paths, not only helper functions.

&#x20; - Published evidence packages must remain separate from mutable working-state snapshots.



\- Out of scope for this ADR:

&#x20; - Field-by-field restoration details that belong in implementation tests, normalization helpers, or migration-specific documentation rather than in the architectural decision itself.



\## Review trigger

Revisit this ADR if any of the following become true:

\- central database deployment becomes practical and justified

\- incompatible snapshot incidents begin recurring

\- the working revision model expands beyond what the current file-backed snapshot pattern can support cleanly

\- the boundary between mutable working state and immutable evidence needs to be reworked for a new operational model

