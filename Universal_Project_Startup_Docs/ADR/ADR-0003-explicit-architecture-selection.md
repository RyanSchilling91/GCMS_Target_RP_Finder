# ADR-0003 — Explicit Architecture Selection

## Status
Template seed / Required for new projects

## Decision
UI, persistence, deployment, auth/session, and concurrency choices must be compared and documented before implementation.

## Context
Prior success patterns can become accidental defaults. A stack that fits one internal workflow tool may be wrong for another project.

## Alternatives considered
- Reuse last successful stack by default: fast, but biased.
- Compare options against current requirements: better fit and clearer tradeoffs.

## Why chosen
The architecture should follow project constraints, not habit.

## Consequences
Adds planning time but reduces retrofit risk.

## Review trigger
Revisit when project requirements change: multi-user needs, compliance needs, offline needs, hosting model, scale, or IT constraints.
