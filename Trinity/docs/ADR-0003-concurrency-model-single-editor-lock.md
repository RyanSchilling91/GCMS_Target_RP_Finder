# ADR-0003 - Use Single-Editor Per Run Locking with Timeout and Controlled Override

## Status
- Accepted

## Decision
Adopt a single-editor lock model per run working revision, with heartbeat, timeout, explicit save/close semantics, and controlled admin-only force-unlock.

## Context
Workflow requires multiple users over time, but not safe simultaneous editing of the same run in current architecture. Shared-storage deployment is the approved model, which makes stale locks a real operational risk. The workflow also requires users to pause work, close runs, resume later, and hand runs off for independent review.

## Alternatives considered
- Optimistic multi-editor concurrency: not chosen for current phase due to conflict complexity.
- No locking: rejected due to corruption and handoff ambiguity risk.
- Manual social locking only: rejected as non-deterministic and unauditable.

## Why chosen
Matches current operational pattern and minimizes risk while enabling reliable handoff.

## Consequences
- Easier: deterministic ownership, pause/resume behavior, and review claim semantics.
- Harder: lock lifecycle edge cases must be engineered and tested.
- Requires: lock metadata schema, 60-second heartbeat, 20-minute stale timeout, admin override audit event, and explicit workflow actions (`Save Draft`, `Save & Close`, `Submit for Review`).
- Requires: review lock acquisition must reject `reviewer == primary_user` for the same run.

## Review trigger
Revisit if true simultaneous editing becomes mandatory.
