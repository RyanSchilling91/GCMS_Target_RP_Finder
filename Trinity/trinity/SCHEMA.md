# Trinity SQLite Schema Specification

- **Schema name:** `trinity`
- **Schema version:** `1`
- **Storage engine:** SQLite (with foreign keys enabled)

This file is the canonical schema contract for Trinity persistence.

## Governing principles

- Run identity (`runs`) is distinct from mutable revision content (`revisions.state_json`).
- Lock lifecycle is durable and auditable (`locks`).
- Workflow-critical events are append-only (`audit_events`).
- Runtime and migration compatibility metadata is durable (`trinity_metadata`).

## Tables and constraints

### 1) `trinity_metadata`
Stores durable metadata including schema/app/storage markers.

Columns:
- `key` (TEXT, PK)
- `value` (TEXT, NOT NULL)
- `updated_at` (TEXT, NOT NULL; ISO-8601 UTC timestamp)

### 2) `runs`
Lifecycle identity anchor for workflow runs.

Columns:
- `run_id` (TEXT, PK)
- `display_id` (TEXT, UNIQUE)
- `created_at` (TEXT, NOT NULL)
- `created_by` (TEXT, NOT NULL)
- `current_revision_id` (TEXT, nullable)
- `run_status` (TEXT, NOT NULL, constrained lifecycle state)
- `run_year` (INTEGER, NOT NULL)
- `source_context` (TEXT, nullable)

### 3) `revisions`
Mutable working revisions and revision lineage.

Columns:
- `revision_id` (TEXT, PK)
- `run_id` (TEXT, NOT NULL, FK -> `runs.run_id`)
- `revision_number` (INTEGER, NOT NULL, `> 0`)
- `revision_status` (TEXT, NOT NULL, constrained lifecycle state)
- `working_state_version` (INTEGER, NOT NULL, `> 0`)
- `state_json` (TEXT, NOT NULL)
- `checksum` (TEXT, nullable)
- `created_at` (TEXT, NOT NULL)
- `created_by` (TEXT, NOT NULL)
- `based_on_revision_id` (TEXT, nullable, FK -> `revisions.revision_id`)
- `is_current_revision` (INTEGER, NOT NULL, `IN (0,1)`)
- `superseded_at` (TEXT, nullable)
- `superseded_by_revision_id` (TEXT, nullable, FK -> `revisions.revision_id`)

Constraints:
- `UNIQUE(run_id, revision_number)`

### 4) `locks`
Durable lock ownership and lifecycle transitions.

Columns:
- `lock_id` (INTEGER, PK autoincrement)
- `run_id` (TEXT, NOT NULL, FK -> `runs.run_id`)
- `revision_id` (TEXT, NOT NULL, FK -> `revisions.revision_id`)
- `owner` (TEXT, NOT NULL)
- `acquired_at` (TEXT, NOT NULL)
- `heartbeat_at` (TEXT, NOT NULL)
- `expires_at` (TEXT, NOT NULL)
- `released_at` (TEXT, nullable)
- `release_actor` (TEXT, nullable)
- `release_reason` (TEXT, nullable)
- `release_type` (TEXT, nullable, `IN ('owner_release','force_release','timeout')`)
- `is_active` (INTEGER, NOT NULL, `IN (0,1)`)

Behavioral constraint:
- At most one active lock row for a run/revision pair.

### 5) `audit_events`
Append-only audit events for workflow governance.

Columns:
- `event_id` (TEXT, PK)
- `run_id` (TEXT, NOT NULL, FK -> `runs.run_id`)
- `revision_id` (TEXT, nullable, FK -> `revisions.revision_id`)
- `actor` (TEXT, NOT NULL)
- `event_type` (TEXT, NOT NULL)
- `occurred_at` (TEXT, NOT NULL)
- `details_json` (TEXT, NOT NULL)

## Indexes

- `idx_revisions_run_current` on `revisions(run_id, is_current_revision)`
- `idx_revisions_status` on `revisions(revision_status)`
- `idx_locks_active_lookup` on `locks(run_id, revision_id, is_active)`
- `uniq_locks_active_per_revision` partial unique index for active locks
- `idx_audit_events_run_time` on `audit_events(run_id, occurred_at)`
- `idx_audit_events_revision_time` on `audit_events(run_id, revision_id, occurred_at)`

## Executable schema SQL

```sql
CREATE TABLE IF NOT EXISTS trinity_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    display_id TEXT UNIQUE,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    current_revision_id TEXT,
    run_status TEXT NOT NULL CHECK (run_status IN ('Draft', 'Ready for Review', 'In Review', 'Needs Rework', 'Approved', 'Published')),
    run_year INTEGER NOT NULL,
    source_context TEXT,
    FOREIGN KEY (current_revision_id) REFERENCES revisions(revision_id)
);

CREATE TABLE IF NOT EXISTS revisions (
    revision_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    revision_number INTEGER NOT NULL CHECK (revision_number > 0),
    revision_status TEXT NOT NULL CHECK (revision_status IN ('Draft', 'Ready for Review', 'In Review', 'Needs Rework', 'Approved', 'Published')),
    working_state_version INTEGER NOT NULL CHECK (working_state_version > 0),
    state_json TEXT NOT NULL,
    checksum TEXT,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    based_on_revision_id TEXT,
    is_current_revision INTEGER NOT NULL DEFAULT 1 CHECK (is_current_revision IN (0, 1)),
    superseded_at TEXT,
    superseded_by_revision_id TEXT,
    UNIQUE (run_id, revision_number),
    FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE,
    FOREIGN KEY (based_on_revision_id) REFERENCES revisions(revision_id),
    FOREIGN KEY (superseded_by_revision_id) REFERENCES revisions(revision_id)
);

CREATE TABLE IF NOT EXISTS locks (
    lock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    revision_id TEXT NOT NULL,
    owner TEXT NOT NULL,
    acquired_at TEXT NOT NULL,
    heartbeat_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    released_at TEXT,
    release_actor TEXT,
    release_reason TEXT,
    release_type TEXT CHECK (release_type IN ('owner_release', 'force_release', 'timeout')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE,
    FOREIGN KEY (revision_id) REFERENCES revisions(revision_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    revision_id TEXT,
    actor TEXT NOT NULL,
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    details_json TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE,
    FOREIGN KEY (revision_id) REFERENCES revisions(revision_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_revisions_run_current ON revisions(run_id, is_current_revision);
CREATE INDEX IF NOT EXISTS idx_revisions_status ON revisions(revision_status);
CREATE INDEX IF NOT EXISTS idx_locks_active_lookup ON locks(run_id, revision_id, is_active);
CREATE UNIQUE INDEX IF NOT EXISTS uniq_locks_active_per_revision
    ON locks(run_id, revision_id)
    WHERE is_active = 1;
CREATE INDEX IF NOT EXISTS idx_audit_events_run_time ON audit_events(run_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_audit_events_revision_time ON audit_events(run_id, revision_id, occurred_at);
```
