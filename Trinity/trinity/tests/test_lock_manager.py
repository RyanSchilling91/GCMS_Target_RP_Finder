from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from trinity.db import DBConfig, TrinityDB


class LockHeldError(RuntimeError):
    """Raised when another actor still holds an active non-stale lock."""


@dataclass(frozen=True)
class LockRecord:
    run_id: str
    revision_id: str
    owner: str
    acquired_at: datetime
    heartbeat_at: datetime
    expires_at: datetime


def _seed_run_revision(db: TrinityDB, *, run_id: str, revision_id: str) -> None:
    conn = db._connection()
    conn.execute(
        '''
        INSERT INTO runs(
            run_id, display_id, created_at, created_by, current_revision_id, run_status, run_year, source_context
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (run_id, f'LIMS-{run_id}', '2026-03-26T00:00:00+00:00', 'analyst-1', None, 'Draft', 2026, None),
    )
    conn.execute(
        '''
        INSERT INTO revisions(
            revision_id, run_id, revision_number, revision_status, working_state_version,
            state_json, checksum, created_at, created_by, based_on_revision_id,
            is_current_revision, superseded_at, superseded_by_revision_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            revision_id,
            run_id,
            1,
            'Draft',
            1,
            '{}',
            None,
            '2026-03-26T00:00:00+00:00',
            'analyst-1',
            None,
            1,
            None,
            None,
        ),
    )
    conn.execute(
        'UPDATE runs SET current_revision_id = ? WHERE run_id = ?',
        (revision_id, run_id),
    )
    conn.commit()


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def acquire_lock(db: TrinityDB, *, run_id: str, revision_id: str, owner: str, now: datetime, ttl: timedelta) -> LockRecord:
    conn = db._connection()
    row = conn.execute(
        '''
        SELECT owner, acquired_at, heartbeat_at, expires_at
        FROM locks
        WHERE run_id = ? AND revision_id = ? AND is_active = 1
        ''',
        (run_id, revision_id),
    ).fetchone()

    if row is not None:
        expires_at = _parse_iso(row['expires_at'])
        if row['owner'] != owner and expires_at > now:
            raise LockHeldError(f'Lock is currently held by {row["owner"]}.')
        if expires_at <= now:
            conn.execute(
                '''
                UPDATE locks
                SET is_active = 0,
                    released_at = ?,
                    release_actor = ?,
                    release_reason = ?,
                    release_type = 'timeout'
                WHERE run_id = ? AND revision_id = ? AND is_active = 1
                ''',
                (now.isoformat(), owner, 'stale timeout takeover', run_id, revision_id),
            )

    acquired_at = now
    expires_at = now + ttl
    conn.execute(
        '''
        INSERT INTO locks(
            run_id, revision_id, owner, acquired_at, heartbeat_at, expires_at,
            released_at, release_actor, release_reason, release_type, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, 1)
        ''',
        (run_id, revision_id, owner, acquired_at.isoformat(), acquired_at.isoformat(), expires_at.isoformat()),
    )
    conn.commit()
    return LockRecord(run_id, revision_id, owner, acquired_at, acquired_at, expires_at)


def get_active_lock(db: TrinityDB, *, run_id: str, revision_id: str) -> LockRecord | None:
    row = db._connection().execute(
        '''
        SELECT run_id, revision_id, owner, acquired_at, heartbeat_at, expires_at
        FROM locks
        WHERE run_id = ? AND revision_id = ? AND is_active = 1
        ''',
        (run_id, revision_id),
    ).fetchone()
    if row is None:
        return None
    return LockRecord(
        run_id=row['run_id'],
        revision_id=row['revision_id'],
        owner=row['owner'],
        acquired_at=_parse_iso(row['acquired_at']),
        heartbeat_at=_parse_iso(row['heartbeat_at']),
        expires_at=_parse_iso(row['expires_at']),
    )


def release_lock(db: TrinityDB, *, run_id: str, revision_id: str, owner: str, now: datetime) -> None:
    db._connection().execute(
        '''
        UPDATE locks
        SET is_active = 0,
            released_at = ?,
            release_actor = ?,
            release_reason = ?,
            release_type = 'owner_release'
        WHERE run_id = ? AND revision_id = ? AND owner = ? AND is_active = 1
        ''',
        (now.isoformat(), owner, 'owner released lock', run_id, revision_id, owner),
    )
    db._connection().commit()


def test_acquire_verify_release_lock(tmp_path: Path) -> None:
    db = TrinityDB(DBConfig(db_path=tmp_path / 'working.db', schema_version=1, app_version='0.1.0'))
    db.initialize()
    _seed_run_revision(db, run_id='run-1', revision_id='rev-1')

    now = datetime(2026, 3, 26, 12, 0, tzinfo=timezone.utc)
    acquire_lock(db, run_id='run-1', revision_id='rev-1', owner='analyst-a', now=now, ttl=timedelta(minutes=20))

    active = get_active_lock(db, run_id='run-1', revision_id='rev-1')
    assert active is not None
    assert active.owner == 'analyst-a'

    release_lock(db, run_id='run-1', revision_id='rev-1', owner='analyst-a', now=now + timedelta(minutes=1))
    assert get_active_lock(db, run_id='run-1', revision_id='rev-1') is None


def test_acquire_raises_lock_held_error_for_fresh_competing_lock(tmp_path: Path) -> None:
    db = TrinityDB(DBConfig(db_path=tmp_path / 'working.db', schema_version=1, app_version='0.1.0'))
    db.initialize()
    _seed_run_revision(db, run_id='run-1', revision_id='rev-1')

    now = datetime(2026, 3, 26, 12, 0, tzinfo=timezone.utc)
    acquire_lock(db, run_id='run-1', revision_id='rev-1', owner='analyst-a', now=now, ttl=timedelta(minutes=20))

    with pytest.raises(LockHeldError, match='held by analyst-a'):
        acquire_lock(
            db,
            run_id='run-1',
            revision_id='rev-1',
            owner='analyst-b',
            now=now + timedelta(minutes=5),
            ttl=timedelta(minutes=20),
        )


def test_stale_lock_can_be_taken_over_after_expiry_threshold(tmp_path: Path) -> None:
    db = TrinityDB(DBConfig(db_path=tmp_path / 'working.db', schema_version=1, app_version='0.1.0'))
    db.initialize()
    _seed_run_revision(db, run_id='run-1', revision_id='rev-1')

    t0 = datetime(2026, 3, 26, 12, 0, tzinfo=timezone.utc)
    acquire_lock(db, run_id='run-1', revision_id='rev-1', owner='analyst-a', now=t0, ttl=timedelta(minutes=20))

    takeover_time = t0 + timedelta(minutes=21)
    takeover = acquire_lock(
        db,
        run_id='run-1',
        revision_id='rev-1',
        owner='analyst-b',
        now=takeover_time,
        ttl=timedelta(minutes=20),
    )

    assert takeover.owner == 'analyst-b'

    rows = db._connection().execute(
        '''
        SELECT owner, is_active, release_type
        FROM locks
        WHERE run_id = ? AND revision_id = ?
        ORDER BY lock_id ASC
        ''',
        ('run-1', 'rev-1'),
    ).fetchall()

    assert [(row['owner'], row['is_active'], row['release_type']) for row in rows] == [
        ('analyst-a', 0, 'timeout'),
        ('analyst-b', 1, None),
    ]
