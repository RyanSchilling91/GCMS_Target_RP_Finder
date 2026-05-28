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

## UI options considered
Compare at least two when undecided.

| Option | Why it fits | Risks / drawbacks | Bad fit when | Decision |
|---|---|---|---|---|
|  |  |  |  |  |

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
