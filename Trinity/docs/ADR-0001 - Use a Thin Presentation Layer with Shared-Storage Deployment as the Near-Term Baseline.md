\# ADR-0001 - Use a Thin Presentation Layer with Shared-Storage Deployment as the Near-Term Baseline



\## Status
- \*\*Archived — Not Applicable\*\*
- Original status: Accepted (superseded by ADR-0006 in host repo; not applicable
  to Trinity because Trinity has no presentation layer)

> \*\*Archive notice:\*\* Trinity is a pure Python backend package with no
> presentation layer. This ADR was written when Trinity was incorrectly conceived
> as a standalone application with a UI. It does not govern any aspect of
> Trinity's current design.
>
> The shared-storage deployment stance and thin-layer architectural principle
> remain valid — but they apply to the \*\*host application\*\*, not to Trinity
> itself. See the host repo's own ADR-0001 and ADR-0006 for current presentation
> and deployment decisions.
>
> Trinity's architectural boundaries are governed by ARCHITECTURE\_SELECTION.md
> and ADR-0002 through ADR-0005.

\## Decision

Use a thin presentation layer over a workflow-governed Python application core as the near-term baseline, with shared-storage deployment and launcher-based access for version 1.



For the current phase, Streamlit is the accepted presentation layer. It is a renderer and interaction surface, not the owner of workflow logic, persistence semantics, routing rules, review control, lock handling, or publish behavior.



Shared storage remains the accepted near-term operating model for working-state persistence, run discovery, handoff, and published artifact access in the current restricted environment.



\## Context

The project must operate in a constrained environment where public hosting, enterprise platform services, and more complex infrastructure are not yet assumed to exist. At the same time, the system must support a governed workflow that includes draft work, save/resume, review handoff, publish, and controlled post-publish re-entry.



Earlier project failures showed that the main architectural risk is not simply “which UI framework to pick.” The bigger risk is letting the UI own business logic, workflow truth, route decisions, or persistence semantics. That pattern creates state drift, fragile reopen behavior, difficult testing, and stack lock-in.



The architecture therefore needs to support two realities at once:



1\. A practical near-term implementation that can run in the current environment.

2\. A longer-term design that keeps the application core portable if the renderer or deployment model changes later.



\## Alternatives considered

\- Keep building as a UI-led app with helper modules:

&#x20; - Rejected because it increases the risk of repeating earlier failure modes where UI/session behavior quietly becomes the system of record.



\- Adopt a heavier hosted web stack now:

&#x20; - Rejected for the current phase because it adds infrastructure and rewrite overhead before the workflow model is fully stabilized and before the environment clearly supports it.



\- Build a desktop-native client now:

&#x20; - Deferred because it would increase packaging and maintenance complexity without solving the primary current problem, which is workflow governance and state integrity.



\## Why chosen

This decision preserves a practical path for the current project while protecting the more important long-term architectural boundary: the workflow-governed Python core must remain separable from the presentation layer.



Using Streamlit now is acceptable because it allows quick iteration in the current environment, but the decision is intentionally framed as a renderer choice, not as permission to let Streamlit become the architecture.



Using shared storage now is acceptable because it matches the deployment constraints and enables save/resume, handoff, review access, and published artifact access without requiring hosted infrastructure.



\## Consequences

\- Easier:

&#x20; - The project can move forward in the current environment without waiting on central hosting or enterprise platform decisions.

&#x20; - The team can stabilize workflow behavior quickly while preserving future renderer flexibility.



\- Harder:

&#x20; - The codebase must actively resist UI creep. Workflow logic cannot be allowed to drift into page code or reactive callbacks.

&#x20; - Shared-storage deployment requires explicit lock handling, path discipline, stale-lock recovery, and deterministic run discovery.



\- Requires:

&#x20; - Business logic must live in service/domain modules, not UI files.

&#x20; - Routing must derive from persisted workflow truth, not remembered page state.

&#x20; - Save/resume behavior must be tested independently of the UI framework.

&#x20; - The renderer must remain replaceable in principle, even if Streamlit remains the current choice in practice.



\## Review trigger

Revisit this ADR if any of the following become true:

\- enterprise hosting or a managed backend becomes available and approved

\- simultaneous multi-user collaboration becomes a real requirement

\- the presentation layer begins constraining workflow correctness or maintainability

\- the team decides to replace Streamlit with another renderer while preserving the same application core

