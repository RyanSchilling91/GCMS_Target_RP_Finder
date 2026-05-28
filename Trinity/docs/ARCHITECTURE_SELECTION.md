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

The recommended architecture is a \*\*workflow-governed Python application core\*\* with a \*\*thin presentation layer\*\*, \*\*file-backed embedded persistence for working state\*\*, \*\*immutable published evidence packages\*\*, and \*\*single-editor concurrency controls\*\*.



The core design intent is not “keep the current app because it already exists.” The core design intent is:



1\. keep the workflow truth in governed persisted objects

2\. keep derived state disposable

3\. keep evidence immutable

4\. keep the UI replaceable

5\. keep restricted-environment deployment practical



\---



\## UI options considered



\### Option

\- Name: Thin Streamlit presentation layer over service/domain modules

\- Why it fits: supports guided workflow screens, rapid iteration, and current environment constraints while allowing the real application logic to live outside the UI.

\- Risks / drawbacks: rerun/session behavior can corrupt workflow semantics if UI state is treated as source truth.

\- When this option is a bad fit: strict enterprise auth, highly concurrent multi-editor workflows, or very complex orchestration that depends on richer client/server state control.

\- Architectural rule if chosen: the UI may render workflow state and invoke actions, but run lifecycle, matching, review, locking, persistence, publish validation, and authorization must all live in non-UI modules.



\### Option

\- Name: Desktop application shell over the same Python core

\- Why it fits: could provide tighter workstation packaging and more explicit local-state handling if IT or user experience later demands it.

\- Risks / drawbacks: increases packaging and maintenance burden without solving the main current problem, which is governed workflow correctness rather than desktop integration.

\- When this option is a bad fit: when the team needs the fastest path to stabilize workflow behavior in a constrained environment.

\- Notes: viable future renderer if UI portability is preserved from the start.



\### Option

\- Name: Full hosted web stack rewrite

\- Why it fits: strongest future path for enterprise auth, central APIs, and higher-scale collaboration.

\- Risks / drawbacks: major rewrite risk, delayed value, and misalignment with current deployment constraints. It also risks repeating the earlier failure mode of changing stack before workflow truth and state boundaries are fully stabilized.

\- When this option is a bad fit: current restricted/offline environment and current project phase.

\- Notes: deferred, not rejected forever.



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

