\# ASSUMPTIONS\_AND\_OPEN\_QUESTIONS.md



\## Purpose of this document

Track what is being assumed, what has already been resolved, what remains open, and what risks exist if those assumptions turn out to be wrong.



This document is not a parking lot for vague ideas. It is meant to expose architecture, workflow, deployment, and governance assumptions early enough that the project does not silently hard-code them and rediscover them later as failures.



\---



\## Guided fill status

\- Status: Updated

\- Last reviewed by: project owner + AI

\- Last updated: 2026-03-24



\---



\## Assumptions



\### Assumption

\- Assumption: Shared-storage deployment with launcher shortcuts remains the approved near-term operating model.

\- Why it is currently being assumed: It matches the restricted environment, current workstation reality, and existing deployment posture.

\- Risk if wrong: The current persistence, locking, and pathing model would need substantial redesign.

\- Mitigation: Keep persistence rules, lock handling, and run discovery in service/domain modules rather than binding them to the UI.

\- Who resolves it: Project lead + IT.

\- Decision deadline or trigger: Revisit only if central hosting or a managed service becomes approved.



\### Assumption

\- Assumption: One active editor per working revision is operationally acceptable.

\- Why it is currently being assumed: The workflow is sequential and handoff-driven, not built around true simultaneous editing.

\- Risk if wrong: The current lock-first model will be insufficient and conflict-resolution logic will be required.

\- Mitigation: Treat lock ownership, heartbeat, timeout, and override as first-class architecture surfaces; defer collaborative merge logic unless it becomes mandatory.

\- Who resolves it: Project lead + lab operations.

\- Decision deadline or trigger: Revisit only if simultaneous co-editing becomes a real requirement.



\### Assumption

\- Assumption: The scientific calculation logic is substantially correct enough to preserve while workflow and governance are hardened.

\- Why it is currently being assumed: The project is focused first on workflow correctness, state integrity, auditability, and review/publish control.

\- Risk if wrong: The system could become operationally well-governed while still producing incorrect analytical outputs.

\- Mitigation: Expand regression datasets, equation audits, criteria validation, and publish-summary verification as part of test and release gates.

\- Who resolves it: Domain lead + reviewer.

\- Decision deadline or trigger: Before production hardening signoff.



\### Assumption

\- Assumption: Rehydration compatibility across application updates is required.

\- Why it is currently being assumed: Save/resume, handoff, reopen, and long-lived run storage are core workflow requirements.

\- Risk if wrong: Older runs or revisions may become unreadable or partially corrupted after updates.

\- Mitigation: Require schema/app version metadata, load-time validation, explicit migrations where needed, and compatibility tests.

\- Who resolves it: Engineering owner.

\- Decision deadline or trigger: Before any persistence format or schema change.



\### Assumption

\- Assumption: LIMS IDs are unique and stable enough to remain the canonical business identifier for a run.

\- Why it is currently being assumed: The project owner confirmed that this matches operational reality.

\- Risk if wrong: Duplicate creation, path collisions, or identity ambiguity may appear.

\- Mitigation: Preserve the canonical LIMS ID in metadata, while allowing a separate internal run identifier or path-safe normalization if future exceptions appear.

\- Who resolves it: Project lead + LIMS owner.

\- Decision deadline or trigger: On first observed invalid, reused, or path-unsafe identifier.



\### Assumption

\- Assumption: The planned sample set must be treated as first-class workflow truth before raw upload occurs.

\- Why it is currently being assumed: The workflow now begins with pre-run planning and the downstream matching logic depends on that data.

\- Risk if wrong: The app may regress toward a raw-upload-first design that recreates earlier state drift and routing problems.

\- Mitigation: Keep planned sample set rows in working state and ensure downstream steps derive from that persisted truth.

\- Who resolves it: Project lead + workflow owner.

\- Decision deadline or trigger: This should only be revisited if the workflow itself changes.



\### Assumption

\- Assumption: Published evidence must remain immutable, even when real-world workflow requires re-entry after publish.

\- Why it is currently being assumed: The project must support defensible archives while still allowing controlled corrections and revised working passes.

\- Risk if wrong: The system may blur the line between evidence and mutable work, damaging auditability.

\- Mitigation: Reopen by creating a new working revision from published evidence, never by editing the published revision in place.

\- Who resolves it: Project lead + reviewer stakeholders.

\- Decision deadline or trigger: This is considered foundational unless an external policy change overrides it.



\---



\## Resolved questions



\### Resolved

\- Question: What run status lifecycle should be enforced?

\- Decision: `Draft -> Ready for Review -> In Review -> Needs Rework -> Draft -> Approved -> Published`, with controlled post-publish re-entry handled through creation of a new working revision rather than mutation of the published revision.



\### Resolved

\- Question: What inactivity timeout and force-unlock policy is acceptable?

\- Decision: Heartbeat every 60 seconds; lock becomes stale after 20 minutes without heartbeat; admin/project lead may force unlock with required reason and audit logging.



\### Resolved

\- Question: What should publication produce?

\- Decision: An immutable published evidence package containing the approved snapshot, manifest, exports, summary/report artifacts, signature or signoff log, criteria provenance, and any other governed publish outputs required by the workflow.



\### Resolved

\- Question: How should save/quit behavior work?

\- Decision: Support `Save Draft`, `Save \& Close`, and `Submit for Review`. Save persists working truth; close/review actions then handle lock and status transitions in the proper sequence.



\### Resolved

\- Question: What should the home/router surface show?

\- Decision: `Start New Dataset`, `Continue My Drafts`, `Runs Ready for Review`, `My Reviews In Progress`, and `Published Runs`.



\### Resolved

\- Question: How should Sample Set Manager lines match to uploaded instrument rows in the first implementation?

\- Decision: Matching is deterministic and order-based. Non-excluded planned sample set lines are processed top-to-bottom; paired line types consume the next two raw rows, single-row types consume the next one, and missing/extra rows surface as warnings or audit output.



\### Resolved

\- Question: What auth/role model is acceptable in the near term?

\- Decision: Use lightweight `User` / `Admin` roles; enforce reviewer independence (`reviewer != primary\_user` on the same run); require admin challenge plus reason for protected actions; record actor from workstation identity.



\### Resolved

\- Question: What summary report format will the first implementation write?

\- Decision: The first implementation writes an HTML summary/report artifact alongside the immutable published evidence package.



\### Resolved

\- Question: How are near-term admin credential checks implemented?

\- Decision: Near-term protected admin actions use a password-only challenge with workstation identity recorded as actor. The bootstrap fallback password is currently accepted during the hardening phase.



\### Resolved

\- Question: What criteria and thresholds are user-editable vs admin-only?

\- Decision: Run-local scientific inputs remain editable during normal draft/rework workflow; global workflow criteria, tolerance settings, review thresholds, and governed options are admin-only and must be changed through authenticated, reason-logged criteria management.



\### Resolved

\- Question: What is the architectural separation between mutable work and immutable evidence?

\- Decision: `Run`, `Working Revision`, and `Published Evidence Package` are separate identities and must remain separate in documentation, persistence, and workflow logic.



\---



\## Open questions



\### Open question

\- Question: Should admin credential checks remain in-app only, or must they be backed by enterprise identity before production release?

\- Why it matters: This affects security posture, audit depth, and deployment complexity.

\- Risk of deferring: The workflow may stabilize before the long-term identity model is fully settled.

\- Who resolves it: Project lead + IT/security.

\- Decision deadline or trigger: Before production hardening signoff.



\### Open question

\- Question: Should the summary/report layer later add PDF output in addition to the initial HTML report?

\- Why it matters: It affects runtime dependencies, archive readability, and operator expectations.

\- Risk of deferring: Late implementation churn in report generation.

\- Who resolves it: Project lead + reviewer stakeholders.

\- Decision deadline or trigger: Before report-format expansion work begins.



\### Open question

\- Question: Should future deployments preserve file-backed working storage, or migrate to a central database once the workflow model is mature?

\- Why it matters: It affects lock strategy, storage layout, deployment overhead, and recoverability.

\- Risk of deferring: Documentation and interfaces may drift toward file-only assumptions.

\- Who resolves it: Project lead + engineering owner + IT.

\- Decision deadline or trigger: If central hosting becomes feasible.



\### Open question

\- Question: Does the long-term archive model need a distinct `Archived` lifecycle state beyond `Published`?

\- Why it matters: It affects lifecycle vocabulary and retention semantics.

\- Risk of deferring: Mild terminology churn later.

\- Who resolves it: Project lead + governance stakeholders.

\- Decision deadline or trigger: Before formal retention/archive policy is implemented.



\---



\## Deferred decisions summary

\- Central database migration path.

\- Enterprise identity / SSO integration.

\- Any multi-editor collaboration model beyond the accepted single-editor lock-first approach.

\- Whether HTML-only report output remains sufficient after the first publish-capable release.

\- Whether a formal `Archived` state is needed beyond `Published`.



\---



\## Notes for the agent

\- Do not treat open questions as permission to improvise architecture.

\- Resolved workflow, publish, lock, identity, and protected-action expectations should be treated as real constraints, not soft preferences.

\- If a proposed implementation conflicts with this document, the workflow timeline, the data model, or the state classification, stop and surface the conflict before writing code.

