"""Audit logging contracts for governed workflow actions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class AuditEvent:
    """Append-only event record."""

    event_id: str
    run_id: str
    revision_id: str
    actor: str
    event_type: str
    occurred_at: datetime
    details: Mapping[str, Any]


class AuditLog:
    """Contract for writing and querying durable audit events."""

    def append(self, event: AuditEvent) -> None:
        """Append an immutable event."""
        raise NotImplementedError

    def list_for_run(self, *, run_id: str) -> Sequence[AuditEvent]:
        """List audit events for a run in chronological order."""
        raise NotImplementedError

    def list_for_revision(self, *, run_id: str, revision_id: str) -> Sequence[AuditEvent]:
        """List audit events for a specific revision in chronological order."""
        raise NotImplementedError
