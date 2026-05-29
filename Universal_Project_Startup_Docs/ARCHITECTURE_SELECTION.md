# Architecture Selection

## Purpose
Evaluate architecture options before locking the project into a stack.

Prior successful patterns may be strong candidates, but they are not defaults unless this project’s requirements justify them.

## Guided fill status
- Status: [Complete / Present but weak / Missing]
- Last reviewed by:
- Last updated:

## Core requirements affecting architecture
| Requirement | Answer | Architecture impact |
|---|---|---|
| Single-user or multi-user? |  |  |
| Simultaneous editing? |  |  |
| Local, on-prem, cloud, hybrid, offline? |  |  |
| Browser, desktop, API, mixed? |  |  |
| Restricted IT environment? |  |  |
| Auditability / traceability? |  |  |
| Expected data size/performance? |  |  |
| Recovery / retention expectations? |  |  |
| Replaceable UI needed? |  |  |

UI options considered
Option — ACCEPTED (current)

Name: FastAPI backend + plain HTML/CSS/JS frontend served to a local browser
Why it fits: provides a clean, explicit HTTP client/server boundary with no framework-managed session-state rerun model. FastAPI route handlers are thin presentation-layer callables; all workflow logic, persistence, locking, and review governance remain in domain/service modules. Runs locally, supports shared-storage deployment, is offline/local-network capable, and is launcher-compatible. Eliminates the structural source of the Streamlit-specific state-drift defects documented in the Failure Catalog and Retrospective.
Risks / drawbacks: existing Streamlit surfaces must be migrated. HTML/JS frontend development requires different skills than Streamlit widget composition. Route handler discipline is required to prevent business logic from drifting into the API layer (same rule as before, now applied to FastAPI handlers rather than Streamlit page files).
Architectural rule: FastAPI route handlers are presentation-layer thin. HTML frontend is a renderer only. Workflow truth, persistence, locking, review, publish validation, and authorization must live in domain/service modules, not in route handlers or frontend scripts.
ADR: ADR-0006

Option — SUPERSEDED

Name: Thin Streamlit presentation layer over service/domain modules
Why it was accepted: supported guided workflow screens, rapid iteration, and current environment constraints while keeping real application logic outside the UI.
Why superseded: Streamlit's rerun/session-state model is structurally misaligned with the explicit-commit, save-boundary, and route-from-persisted-truth requirements. Multiple Failure Catalog and Retrospective entries trace to Streamlit-specific state-drift defects (action-widget snapshot hardening, Step 1 navigation-persistence repair, snapshot key filtering). The review trigger in ADR-0001 — "if the presentation layer begins constraining workflow correctness or maintainability" — was met.
ADR: ADR-0001 (Superseded by ADR-0006)

Option — DEFERRED

Name: Desktop application shell over the same Python core
Why it fits: tighter workstation packaging and more explicit local-state handling.
Risks / drawbacks: increases packaging and maintenance burden without solving the main current problem.
Notes: viable future renderer if UI portability is preserved.

Option — DEFERRED

Name: Full hosted web stack rewrite
Why it fits: strongest future path for enterprise auth, central APIs, and higher-scale collaboration.
Risks / drawbacks: major rewrite risk, delayed value, and misalignment with current deployment constraints.
Notes: deferred, not rejected forever.

## Persistence options considered
Compare concurrency, operational burden, portability, analytical performance, migration complexity, and archive suitability.

| Option | Why it fits | Risks / drawbacks | Bad fit when | Decision |
|---|---|---|---|---|
|  |  |  |  |  |

## Deployment options considered
Examples: local workstation, central host with browser clients, desktop installs, server-hosted web app, hybrid.

| Option | Why it fits | Risks / drawbacks | Bad fit when | Decision |
|---|---|---|---|---|
|  |  |  |  |  |

## Auth / session options considered
Fill in:

## Concurrency / collaboration model considered
Options may include single writer, record lock, optimistic concurrency, branch/merge, immutable handoff package.

Fill in:

## Proven prior patterns worth considering, not assuming
| Pattern | Why it worked before | Conditions that made it fit | Conditions that make it a poor fit here |
|---|---|---|---|
| Thin UI + service/domain core | Preserved portability and testability | UI should be replaceable; business rules matter | Tiny throwaway script with no lifecycle |
| Local/embedded DB | Simple deployment and analytical workflows | Controlled writer model; modest concurrency | uncontrolled concurrent writers |
| Append-only audit log | Supported traceability and debugging | review/signoff/compliance matters | no audit or historical accountability needed |
| Publishable evidence package | Made handoff/archive defensible | outputs need review or later reconstruction | no handoff/archive requirement |

## Recommended direction
- Recommendation:
- Why chosen:
- Why alternatives were not chosen:
- What must be revisited if requirements change:

## ADR candidates
List decisions that must be recorded.

| Decision | Why irreversible/expensive | ADR file |
|---|---|---|
|  |  |  |

## Deferred decisions
| Decision | Risk if deferred | Who resolves | Trigger / deadline |
|---|---|---|---|
|  |  |  |  |

## Notes for the agent
- Do not frame a preferred stack as universal truth.
- If requirements materially shift the recommendation, surface it explicitly.
- After selection, record accepted choices in ADRs.
