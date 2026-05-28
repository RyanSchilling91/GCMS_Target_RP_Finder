from __future__ import annotations

import json
from pathlib import Path

from trinity.db import DBConfig, TrinityDB


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


def append_event(
    db: TrinityDB,
    *,
    event_id: str,
    run_id: str,
    revision_id: str,
    actor: str,
    event_type: str,
    occurred_at: str,
    details: dict,
) -> None:
    db._connection().execute(
        '''
        INSERT INTO audit_events(event_id, run_id, revision_id, actor, event_type, occurred_at, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (event_id, run_id, revision_id, actor, event_type, occurred_at, json.dumps(details, sort_keys=True)),
    )
    db._connection().commit()


def list_for_run(db: TrinityDB, *, run_id: str) -> list[dict]:
    rows = db._connection().execute(
        '''
        SELECT event_id, actor, event_type, occurred_at, details_json
        FROM audit_events
        WHERE run_id = ?
        ORDER BY occurred_at ASC, event_id ASC
        ''',
        (run_id,),
    ).fetchall()
    return [
        {
            'event_id': row['event_id'],
            'actor': row['actor'],
            'event_type': row['event_type'],
            'occurred_at': row['occurred_at'],
            'details': json.loads(row['details_json']),
        }
        for row in rows
    ]


def test_audit_append_and_ordered_retrieval(tmp_path: Path) -> None:
    db = TrinityDB(DBConfig(db_path=tmp_path / 'working.db', schema_version=1, app_version='0.1.0'))
    db.initialize()
    _seed_run_revision(db, run_id='run-1', revision_id='rev-1')

    append_event(
        db,
        event_id='event-2',
        run_id='run-1',
        revision_id='rev-1',
        actor='reviewer-1',
        event_type='review_claimed',
        occurred_at='2026-03-26T12:01:00+00:00',
        details={'note': 'claimed'},
    )
    append_event(
        db,
        event_id='event-1',
        run_id='run-1',
        revision_id='rev-1',
        actor='analyst-1',
        event_type='draft_saved',
        occurred_at='2026-03-26T12:00:00+00:00',
        details={'checkpoint': 'step_1'},
    )

    events = list_for_run(db, run_id='run-1')

    assert [e['event_id'] for e in events] == ['event-1', 'event-2']
    assert events[0]['details'] == {'checkpoint': 'step_1'}
    assert events[1]['details'] == {'note': 'claimed'}
