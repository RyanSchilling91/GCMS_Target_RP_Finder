# ADR-0004 — Published Evidence Is Immutable

## Status
Template seed / Required when publish, signoff, handoff, or audit matters

## Decision
Published or signed evidence must not be silently overwritten. Rework creates a new working revision or superseding evidence record.

## Context
Review workflows need defensible history. Mutating approved records destroys auditability and user trust.

## Alternatives considered
- Edit published records in place: simple but unsafe.
- Freeze evidence and supersede when needed: safer, traceable, more complex.

## Why chosen
Traceability and reconstruction are more important than storage simplicity in governed workflows.

## Consequences
Requires revision/supersession logic and tests. Prevents silent corruption of historical outputs.

## Review trigger
Revisit only if the project has no audit, handoff, signoff, archive, or evidence requirement.
