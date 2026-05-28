# Data Model

## Purpose
Define the system truth model: entities, fields, ownership, lifecycle states, relationships, invariants, and forbidden states.

This is the main defense against building UI and persistence around a fuzzy mental model.

## Guided fill status
- Status: [Complete / Present but weak / Missing]
- Last reviewed by:
- Last updated:

## Entity list
| Entity | Purpose | Why it exists | Source of truth |
|---|---|---|---|
|  |  |  |  |

## Entity definitions
Repeat this section for every major entity.

### Entity: [name]

#### Purpose

#### Identity rules
- Business identifier:
- Technical identifier:
- Mutable or immutable:
- Duplicate handling:

#### Fields
| Field | Type | Required? | Owner | Editable? | Persistence category | Notes |
|---|---|---|---|---|---|---|
|  |  |  | user / system / reviewer / external | yes / no / conditional | working / derived / evidence |  |

#### Lifecycle states
| State | Entry path | Exit path | Allowed actor | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

#### Invariants
Things that must always be true.

- 

#### Forbidden states
States/combinations that must never occur.

- 

#### Relationships
Parent/child, dependency, reference, or historical-link rules.

- 

## Cross-entity rules
Examples: uniqueness, required parent/child relationships, dependency order, ownership constraints, authorization dependencies.

Fill in:

## Notes for the agent
- If a field owner is unclear, ask.
- If a state has no valid entry path, flag it.
- If the same fact appears to have multiple sources of truth, stop and resolve the conflict.
- Validate business identity separately from technical ID uniqueness.
