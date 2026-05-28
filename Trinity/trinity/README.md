# Trinity Scope

Trinity is a narrow infrastructure layer for workflow-governed applications.

## In-scope ownership

Trinity owns the following capabilities only:

- Database setup and storage initialization.
- Working-state persistence (save/load/delete) for mutable run/revision data.
- Lock management for single-editor coordination (acquire/heartbeat/release/override plumbing).
- Append-only audit logging.

## Boundary rules

- Trinity **must not** import UI frameworks.
- Trinity **must not** enforce business workflow policy (state transitions, review rules, publish/reopen policy, or domain validation logic).
- Callers (for example, EpicFlora) own workflow semantics and authorization checks.

## Non-goals (must never do)

To preserve portability and governance boundaries, Trinity must never:

- Become a UI-coupled module or depend on renderer/session widget behavior.
- Become the system of record for business workflow semantics.
- Encode review independence policy, publish/reopen policy, or authorization policy.
- Replace caller-owned domain validation or decision logic.
- Treat derived display/cache artifacts as authoritative working truth.
- Mutate caller-managed published evidence in place.

## Current implementation notes

- Current methods intentionally raise `NotImplementedError`.
- The module contracts are designed for a thin-caller integration model where policy stays outside Trinity.
