# ADR-0002 — State Classification Before Persistence

## Status
Template seed / Required unless explicitly deferred

## Decision
Working, derived, and evidence state must be classified before persistence design.

## Context
Past failures occurred when derived outputs were stored as source truth or when working state and published evidence were mixed.

## Alternatives considered
- Design storage first: faster but prone to stale truth and unsafe overwrites.
- Classify state first: slower but safer and easier to test.

## Why chosen
Persistence is only safe when the project knows which data is editable, recomputable, or immutable.

## Consequences
Prevents hidden source-of-truth conflicts. Forces early thinking before code.

## Review trigger
Revisit if project has no persistence or state surviving a single execution.
