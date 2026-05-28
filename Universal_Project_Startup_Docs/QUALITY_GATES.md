# Quality Gates

## Purpose
Define the completion and release bar.

This prevents “done” from meaning “some code exists.”

## Guided fill status
- Status: [Complete / Present but weak / Missing]
- Last reviewed by:
- Last updated:

## Must pass before merge or release
| Gate | Required evidence | Status |
|---|---|---|
| Planning docs updated | Relevant docs reflect implementation |  |
| Required tests pass | Test command/output captured |  |
| Workflow matches docs | Manual or automated verification |  |
| State persistence behaves correctly | Refresh/restart/reload tested |  |
| Permissions/auth behave correctly | Role/session cases tested |  |
| Known blockers resolved/deferred | Deferrals logged with risk |  |
| Failure catalog updated for bugs | Entry added where applicable |  |

## Migration verification
Required when schema/storage changes.

- explicit schema/app version present:
- forward migration tested:
- partial/damaged state handling tested:
- unsupported newer schema behavior defined:
- rollback/restore tested:

## Rollback capability
Describe the recovery path if release or migration fails.

Fill in:

## Artifact validation
For published/evidence packages or exports.

| Artifact | Required contents | Validation method |
|---|---|---|
|  |  |  |

## Release hygiene
- dependencies pinned or documented
- run instructions current
- credentials/secrets excluded
- destructive operations controlled
- duplicate guards present where required
- logging/error messages operator-usable

## Bug fix / regression completion gate
Any bug fix is incomplete until:
1. root cause is identified
2. regression test added or reason documented
3. `FAILURE_CATALOG.md` updated
4. process/rule changes proposed in `RETROSPECTIVE.md` or `AGENTS.md` when needed

## Completion statement template
- Tests run:
- Results:
- Docs updated:
- Quality gates met:
- Known risks/deferrals:
