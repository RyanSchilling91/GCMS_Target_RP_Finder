"""Database contracts and bootstrap utilities for Trinity working-state persistence."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class DBConfig:
    """Configuration for Trinity's file-backed working database."""

    db_path: Path
    schema_version: int
    app_version: str


class TrinityDB:
    """Persistence contract for mutable working state."""

    _SCHEMA_DOC = Path(__file__).with_name('SCHEMA.md')

    def __init__(self, config: DBConfig) -> None:
        self._config = config
        self._conn: sqlite3.Connection | None = None

    @property
    def config(self) -> DBConfig:
        """Return the active DB configuration."""
        return self._config

    def initialize(self) -> None:
        """Create required tables/metadata if not present."""
        conn = self._connection()
        conn.execute('PRAGMA foreign_keys = ON;')
        conn.execute('PRAGMA journal_mode = WAL;')
        conn.executescript(self._load_schema_sql())
        self._enforce_schema_marker(conn)
        conn.commit()

    def load_metadata(self) -> Mapping[str, Any]:
        """Load durable metadata (schema/app/storage versions, timestamps)."""
        conn = self._connection()
        rows = conn.execute('SELECT key, value FROM trinity_metadata').fetchall()
        return {key: value for key, value in rows}

    def save_metadata(self, metadata: Mapping[str, Any]) -> None:
        """Persist durable metadata."""
        conn = self._connection()
        now = _utc_now_iso()
        for key, value in metadata.items():
            conn.execute(
                '''
                INSERT INTO trinity_metadata(key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                ''',
                (key, str(value), now),
            )
        conn.commit()

    def close(self) -> None:
        """Release any active DB resources."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._config.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(self._config.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _enforce_schema_marker(self, conn: sqlite3.Connection) -> None:
        existing = conn.execute(
            "SELECT value FROM trinity_metadata WHERE key = 'schema_version'"
        ).fetchone()
        if existing is not None:
            existing_version = int(existing[0])
            if existing_version > self._config.schema_version:
                raise RuntimeError(
                    f'Unsupported schema version {existing_version}; '
                    f'runtime supports up to {self._config.schema_version}.'
                )
            if existing_version < self._config.schema_version:
                raise RuntimeError(
                    f'Database schema version {existing_version} is behind '
                    f'required version {self._config.schema_version}; migration required.'
                )

        marker_payload = {
            'schema_version': self._config.schema_version,
            'app_version': self._config.app_version,
            'storage_engine_version': sqlite3.sqlite_version,
            'schema_source': self._SCHEMA_DOC.name,
        }
        self.save_metadata(marker_payload)
        conn.execute(f'PRAGMA user_version = {self._config.schema_version}')

    def _load_schema_sql(self) -> str:
        raw = self._SCHEMA_DOC.read_text(encoding='utf-8')
        blocks = _extract_sql_blocks(raw)
        if not blocks:
            raise RuntimeError(f'No executable SQL schema blocks found in {self._SCHEMA_DOC}.')
        return '\n\n'.join(blocks)


def _extract_sql_blocks(markdown: str) -> list[str]:
    """Extract fenced ```sql blocks in declaration order."""
    blocks: list[str] = []
    active: list[str] | None = None

    for line in markdown.splitlines():
        stripped = line.strip().lower()
        if active is None:
            if stripped.startswith('```sql'):
                active = []
            continue
        if stripped == '```':
            blocks.append('\n'.join(active).strip())
            active = None
            continue
        active.append(line)

    return [block for block in blocks if block]


def _utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
