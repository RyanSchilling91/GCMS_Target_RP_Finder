from __future__ import annotations

import json
from pathlib import Path

from trinity.db import DBConfig, TrinityDB


def _seed_run_revision(db: TrinityDB, *, run_id: str, revision_id: str, state_json: str = '{}') -> None:
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
            state_json,
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


def test_working_state_dict_json_round_trip(tmp_path: Path) -> None:
    db = TrinityDB(DBConfig(db_path=tmp_path / 'working.db', schema_version=1, app_version='0.1.0'))
    db.initialize()
    _seed_run_revision(db, run_id='run-1', revision_id='rev-1')

    payload = {
        'step': 1,
        'sample_set': [
            {'sample_id': 'S1', 'excluded': False},
            {'sample_id': 'S2', 'excluded': True},
        ],
        'metadata': {'operator': 'analyst-1', 'notes': 'ready'},
    }

    conn = db._connection()
    conn.execute(
        'UPDATE revisions SET state_json = ?, checksum = ? WHERE run_id = ? AND revision_id = ?',
        (json.dumps(payload, sort_keys=True), 'abc123', 'run-1', 'rev-1'),
    )
    conn.commit()

    raw = conn.execute(
        'SELECT state_json FROM revisions WHERE run_id = ? AND revision_id = ?',
        ('run-1', 'rev-1'),
    ).fetchone()[0]

    assert json.loads(raw) == payload
