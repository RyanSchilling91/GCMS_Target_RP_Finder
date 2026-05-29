\# ARCHITECTURE\_SELECTION



\## Purpose of this document

Evaluate architecture options before locking the project into a stack.



This draft is based on the current bootstrap questionnaire, project brief, workflow timeline, data model, state classification, assumptions, and accepted ADRs. Its purpose is to describe the architecture that best fits the real workflow and operating constraints, while explicitly avoiding failure patterns already seen in the earlier project.



\---



\## Guided fill status

\- Status: Complete

\- Last reviewed by: project owner + AI

\- Source of truth for this draft: latest `BOOTSTRAP\_QUESTIONNAIRE.md`, `WORKFLOW\_TIMELINE.md`, `DATA\_MODEL.md`, `STATE\_CLASSIFICATION.md`, accepted ADRs, and failure-learning docs.



\---



\## Core requirements affecting architecture

\- Multi-user over time, but not simultaneous co-editing of the same working revision. The accepted operating rule is one active editor per working revision.

\- Restricted environment. The system must work offline or on a local network and cannot depend on public internet hosting.

\- Shared storage plus launcher-based access is the approved deployment posture for version 1.

\- The workflow begins with a planned sample set, not with raw upload. Architecture must therefore model planning as first-class working truth rather than as a temporary editor or post-upload cleanup layer.

\- Run identity and working-revision identity must remain distinct. Published evidence identity must also remain distinct from mutable working state.

\- Save/resume and backward-compatible rehydration are required. Routing and progress must derive from persisted truth rather than stale UI/session memory.

\- Review must be independent, sequential, and auditable. Self-review is forbidden.

\- Publication produces an immutable evidence package. Reopen/reload after publish must create a new working revision from published evidence rather than modifying the published revision in place.

\- The UI layer must stay replaceable. Business rules, validation, persistence, locking, and authorization cannot be owned by the UI layer.



\---



\## Architecture stance

Trinity is a \*\*workflow-governed Python backend package\*\* with a \*\*pure Python
service API\*\*, \*\*file-backed embedded persistence for working state\*\*, \*\*immutable
published evidence packages\*\*, and \*\*single-editor concurrency controls\*\*.

Trinity has no presentation layer. The architecture stance covers only what
Trinity itself owns: the service/domain API boundary, persistence strategy,
concurrency model, and evidence lifecycle.

The host application's architecture (FastAPI, HTML frontend, deployment model,
session handling) is governed by the host repo's own architecture docs and ADRs,
not by Trinity's docs.

The core design intent:
1. Keep the workflow truth in governed persisted objects
2. Keep derived state disposable and recomputable
3. Keep evidence immutable after publish
4. Keep the service API free of web framework concerns
5. Keep restricted-environment deployment practical through file-backed storage



\---



\## Service API boundary

All public Trinity service functions must:
- Accept actor identity, action context, and all governance inputs as explicit
  parameters — never infer them from environment, session, or framework state
- Return plain Python objects (dataclasses, typed dicts, domain model instances)
- Never import or reference FastAPI, Streamlit, or any HTTP/UI framework
- Be fully testable with plain \`pytest\` and no running server

This boundary is enforced by architecture rule, not by convention. Any Trinity
module that violates it has the wrong scope and must be corrected before merge.

\---

\## ADR applicability in Trinity

| ADR | Status | Notes |
|-----|--------|-------|
| ADR-0001 (Streamlit presentation layer) | Archived — not applicable | Trinity has no presentation layer |
| ADR-0002 (file-backed persistence, version-aware rehydration) | Accepted | Persistence is Trinity's concern |
| ADR-0003 (single-editor concurrency model) | Accepted | Locking is Trinity's concern |
| ADR-0004 (publish immutability / reopen policy) | Accepted | Evidence lifecycle is Trinity's concern |
| ADR-0005 (admin challenge bootstrap) | Accepted | Protected-action governance is Trinity's concern |
| ADR-0006 (FastAPI + HTML frontend) | Does not belong in Trinity | File in host repo ADR set |

\---

\## UI options considered

Not applicable. Trinity has no UI layer and owns no presentation concerns.

UI, routing, frontend framework, and deployment decisions belong in the host
repository's own ARCHITECTURE\_SELECTION and ADR set.

See the host repo's ADR-0006 (FastAPI + HTML browser frontend) for the
accepted application-layer presentation decision.



\---



\## Core application structure options considered



\### Option

\- Name: UI-led application with helper modules

\- Why it fits: easiest to grow from a working prototype.

\- Risks / drawbacks: this is also the pattern most likely to repeat prior failure modes, including UI/session state leaking into persistence truth, route logic duplicated across screens, and save behavior drifting from committed working state.

\- Notes: not recommended.



\### Option

\- Name: Service/domain core with thin UI adapters

\- Why it fits: matches the docs-kit rules, supports portability, keeps business rules testable, and makes persistence, routing, publish, review, and lock semantics explicit.

\- Risks / drawbacks: requires more discipline up front, especially around contracts between workflow services and presentation logic.

\- Notes: this is the architecture that best reflects the rewritten docs.



\---



\## Persistence options considered



\### Option

\- Name: File-backed embedded persistence per run/revision on shared storage, with structured working-state storage plus manifest, audit/event records, and lock metadata

\- Why it fits: works in restricted environments, supports save/resume, aligns with shared-storage deployment, and can preserve run identity, revision lineage, and working-state truth without requiring hosted infrastructure.

\- Risks / drawbacks: stale locks, schema/version drift, accidental duplication of truth, and path-based overwrite mistakes if identifiers and manifests are not treated as authoritative.

\- Architectural requirements if chosen:

&#x20; - persist explicit run identity and current revision identity

&#x20; - persist committed working truth, not transient widget state

&#x20; - keep derived state recomputable

&#x20; - validate schema/app compatibility on load

&#x20; - preserve immutable evidence separately from mutable working state



\### Option

\- Name: Central database service

\- Why it fits: stronger concurrency and centralized control.

\- Risks / drawbacks: likely incompatible with current IT/deployment constraints and introduces infrastructure dependence before the workflow model is mature.

\- When this option is a bad fit: current operating environment.

\- Notes: deferred until hosting approval exists.



\### Option

\- Name: Spreadsheet-based system of record

\- Why it fits: familiar operator mental model.

\- Risks / drawbacks: directly conflicts with auditability, concurrency control, lineage, and defensible publish requirements. It also recreates the fragility this project exists to escape.

\- Notes: not recommended.



\---



\## Evidence and publish architecture options considered



\### Option

\- Name: One mutable working package that also serves as archive

\- Why it fits: minimal implementation complexity.

\- Risks / drawbacks: destroys the separation between working truth and evidence truth and makes auditability weak. It also conflicts with the accepted reopen policy.

\- Notes: rejected.



\### Option

\- Name: Immutable published evidence package plus separate mutable working revision state

\- Why it fits: matches the workflow, data model, ADRs, and quality gates. It supports defensible archives, controlled reopen, lineage tracking, and safe recovery without mutating published artifacts.

\- Risks / drawbacks: requires stronger packaging, manifest integrity, artifact validation, and revision-lineage metadata.

\- Notes: this is a core architecture commitment, not an implementation detail.



\---



\## Deployment model options considered



\### Option

\- Name: Shared storage + local launcher + thin UI runtime

\- Why it fits: aligns with the approved operational pattern and preserves workstation identity capture while using governed shared persistence.

\- Risks / drawbacks: requires explicit lock ownership, stale-lock recovery, path conventions, and durable manifest-based run discovery.

\- When this option is a bad fit: high-write concurrent collaboration or enterprise hosting requirements.



\### Option

\- Name: Central hosted service

\- Why it fits: cleaner for centralized access and enterprise controls.

\- Risks / drawbacks: currently blocked by environment/approval constraints.

\- Notes: deferred.



\### Option

\- Name: Fully local isolated workstation installs only

\- Why it fits: reduces shared dependencies.

\- Risks / drawbacks: undermines review handoff, shared evidence access, and controlled collaboration.

\- Notes: not acceptable as the sole operating model.



\---



\## Auth / session options considered



\### Option

\- Name: Workstation identity for actor capture + governed in-app role/policy enforcement + admin challenge for protected actions

\- Why it fits: matches the restricted environment and accepted ADR direction. It supports review independence, audited protected actions, and recoverable admin controls without requiring enterprise identity now.

\- Risks / drawbacks: shared-secret admin hardening is still weaker than enterprise identity and must be tightly documented, audited, and kept out of source control except for the explicit bootstrap exception already recorded in the docs.

\- Notes: protected actions must always capture actor, reason, and governed path.



\### Option

\- Name: Enterprise identity / SSO

\- Why it fits: best long-term accountability and credential management.

\- Risks / drawbacks: not yet supported by current environment assumptions.

\- Notes: deferred, but architecture should avoid blocking this later.



\---



\## Concurrency / collaboration model options considered



\### Option

\- Name: Single-editor lock per working revision with heartbeat, timeout, and governed override

\- Why it fits: directly matches the resolved assumption and workflow. Review is sequential, handoff is explicit, and simultaneous co-editing is not required for version 1.

\- Risks / drawbacks: stale lock handling and lock lifecycle bugs can block work or damage confidence if not engineered and tested well.

\- Architectural rule if chosen: locks must be durable coordination objects, not inferred from session memory; override must require audit and reason; review claim rules must enforce reviewer independence.



\### Option

\- Name: Optimistic concurrent editing

\- Why it fits: broader collaboration flexibility.

\- Risks / drawbacks: high conflict complexity and poor fit for current workflow/governance needs.

\- Notes: not recommended.



\### Option

\- Name: Multi-branch merge workflow

\- Why it fits: preserves alternatives.

\- Risks / drawbacks: too operationally heavy for the intended user workflow.

\- Notes: only the publish-to-new-revision reopen pattern is accepted, and that is governed lineage, not collaborative branching.



\---



\## Canonical architectural boundaries



\### 1. Workflow truth boundary

Canonical mutable workflow truth lives in governed persisted objects such as `Run`, `Working Revision`, planned sample set lines, raw upload provenance/rows, analyst exclusion decisions, review state, lock state, and criteria references. It does not live in widget state, convenience caches, progress summaries, or route labels.



\### 2. Derived-state boundary

Matching outputs, routing decisions, workflow progress labels, queue eligibility, calculation tables, and publish-readiness summaries are derived. They may be cached for performance, but they must be invalidated and recomputed from committed working truth and may never become independent source truth.



\### 3. Evidence boundary

Published manifest, approved snapshot, exports, summary outputs, signoff logs, criteria provenance, and audit evidence are evidence state and must be immutable after publish.



\### 4. UI boundary

The UI renders and invokes; it does not own truth. Any architecture that lets UI memory silently outrank committed persisted state is considered invalid because it repeats known failure modes.



\---



\## Recommended run/revision artifact layout

The prior run-folder idea still works, but it should now be revision-aware rather than implying that one folder equals one mutable truth blob.



```text

runs/

&#x20; YYYY/

&#x20;   <run\_id>/

&#x20;     manifest.json

&#x20;     events.jsonl

&#x20;     revisions/

&#x20;       <revision\_id>/

&#x20;         working.duckdb

&#x20;         lock.json

&#x20;         imports/

&#x20;         derived\_cache/

&#x20;     published/

&#x20;       <published\_package\_id>/

&#x20;         manifest.json

&#x20;         approved\_snapshot.duckdb

&#x20;         exports/

&#x20;         summary/

&#x20;         signatures/

&#x20;         criteria/

