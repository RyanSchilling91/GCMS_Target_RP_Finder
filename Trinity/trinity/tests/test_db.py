from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from trinity.db import DBConfig, TrinityDB, _extract_sql_blocks


def test_db_contract_construction() -> None:
    config = DBConfig(db_path=Path('/tmp/trinity.db'), schema_version=1, app_version='0.0.0')
    db = TrinityDB(config)

    assert db.config == config


def test_initialize_creates_schema_and_version_marker(tmp_path: Path) -> None:
    db_path = tmp_path / 'working.db'
    db = TrinityDB(DBConfig(db_path=db_path, schema_version=1, app_version='0.1.0'))

    db.initialize()
    metadata = db.load_metadata()

    expected_tables = {'trinity_metadata', 'runs', 'revisions', 'locks', 'audit_events'}
    rows = db._connection().execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    existing = {row[0] for row in rows}

    assert expected_tables.issubset(existing)
    assert metadata['schema_version'] == '1'
    assert metadata['app_version'] == '0.1.0'
    assert metadata['schema_source'] == 'SCHEMA.md'


def test_initialize_rejects_schema_mismatch(tmp_path: Path) -> None:
    db_path = tmp_path / 'working.db'

    first = TrinityDB(DBConfig(db_path=db_path, schema_version=1, app_version='0.1.0'))
    first.initialize()
    first.close()

    mismatched = TrinityDB(DBConfig(db_path=db_path, schema_version=2, app_version='0.2.0'))
    with pytest.raises(RuntimeError, match='migration required'):
        mismatched.initialize()


def test_duplicate_lims_id_rejected_by_unique_display_id_constraint(tmp_path: Path) -> None:
    db_path = tmp_path / 'working.db'
    db = TrinityDB(DBConfig(db_path=db_path, schema_version=1, app_version='0.1.0'))
    db.initialize()

    db._connection().execute(
        '''
        INSERT INTO runs(
            run_id, display_id, created_at, created_by, current_revision_id, run_status, run_year, source_context
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        ('run-1', 'LIMS-123', '2026-03-26T00:00:00+00:00', 'analyst-1', None, 'Draft', 2026, None),
    )
    db._connection().commit()

    with pytest.raises(sqlite3.IntegrityError):
        db._connection().execute(
            '''
            INSERT INTO runs(
                run_id, display_id, created_at, created_by, current_revision_id, run_status, run_year, source_context
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            ('run-2', 'LIMS-123', '2026-03-26T00:00:01+00:00', 'analyst-2', None, 'Draft', 2026, None),
        )


def test_extract_sql_blocks_returns_only_sql_fences() -> None:
    markdown = """
# Example

```text
skip
```

```sql
CREATE TABLE demo (id INTEGER PRIMARY KEY);
```

```sql
CREATE INDEX demo_idx ON demo(id);
```
"""
    blocks = _extract_sql_blocks(markdown)

    assert blocks == [
        'CREATE TABLE demo (id INTEGER PRIMARY KEY);',
        'CREATE INDEX demo_idx ON demo(id);',
    ]
