# Recovery and Retention

## Purpose
Define recovery, backup, archive, and retention expectations before production reliance.

This document is generic. Each project must fill in concrete paths, tools, commands, owners, and retention windows.

## Recovery triggers
Recovery may be needed when:
- app startup fails due to storage corruption
- required tables/files are missing
- persisted state was accidentally deleted or overwritten
- migration partially completed
- published/evidence artifacts cannot be validated
- operator sees unexplained data loss or rollback

## First response rules
1. Stop the app or writer process if corruption is suspected.
2. Do not repeatedly restart into a failing store.
3. Capture exact error text and timestamp.
4. Preserve suspect files before replacement.
5. Validate candidate backup/archive before restore.
6. Log restore action with actor, source file, timestamp, and result.

## Backup layers
Define at least two layers when operationally important.

| Layer | Purpose | Example naming | Retention | Auto-prune? |
|---|---|---|---|---|
| Daily / short-gap backup | Crash recovery | `state_backup_YYYY-MM-DD.ext` | project-defined | yes/no |
| Monthly / compliance archive | Long-term reconstruction | `state_archive_YYYY-MM.ext` | project-defined | usually no |

## Separation rule
Operational backups and compliance archives should be stored separately and managed by separate logic paths when the project requires defensible recovery.

## Candidate validation before restore
Each project must define how to validate a recovery file before replacing live state.

Minimum checks:
- file exists and is readable
- schema/app version supported
- required tables/objects exist
- key row counts look plausible
- newest/oldest event timestamps make sense
- integrity check passes if storage engine supports it

## Restore procedure placeholder
Fill this per project:

1. Stop app/writer process:
2. Identify live state path:
3. Identify candidate backup/archive:
4. Validate candidate:
5. Quarantine existing live state:
6. Restore candidate:
7. Restart app:
8. Run smoke tests:
9. Confirm event/audit log recorded restore:
10. Record incident note:

## Post-restore verification
Minimum checks:
- app starts cleanly
- schema/migration state matches target
- core records load
- active users/roles/permissions work
- one save/load smoke test passes
- published/evidence artifacts remain valid
- restore event exists in audit/event log where applicable

## Retention policy placeholder
| Artifact | Purpose | Retention | Pruning | Owner |
|---|---|---|---|---|
|  |  |  |  |  |

## Notes for the agent
- Recovery design is not optional for production tools.
- A single database/file is not a complete evidence strategy unless the project explicitly accepts that risk.
- Restore actions should be auditable when traceability matters.
