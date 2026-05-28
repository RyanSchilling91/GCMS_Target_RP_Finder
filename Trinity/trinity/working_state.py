"""Working-state contracts for Trinity run revisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class WorkingStateRef:
    """Identity for mutable workflow truth."""

    run_id: str
    revision_id: str
    working_state_version: int


@dataclass(frozen=True)
class SaveResult:
    """Result metadata for an explicit save boundary."""

    saved_at: datetime
    checksum: str


class WorkingStateStore:
    """Contract for loading/saving canonical mutable working state."""

    def load(self, ref: WorkingStateRef) -> Mapping[str, Any]:
        """Return canonical working-state payload for a run revision."""
        raise NotImplementedError

    def save(self, ref: WorkingStateRef, payload: Mapping[str, Any]) -> SaveResult:
        """Persist canonical working-state payload for a run revision."""
        raise NotImplementedError

    def delete(self, ref: WorkingStateRef) -> None:
        """Delete mutable working-state payload for a run revision."""
        raise NotImplementedError
