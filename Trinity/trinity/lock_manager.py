"""Single-editor locking contracts for Trinity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class LockToken:
    """Represents an acquired lock for a run revision."""

    run_id: str
    revision_id: str
    owner: str
    acquired_at: datetime
    expires_at: datetime


class LockManager:
    """Contract for lock acquisition, heartbeat, release, and override."""

    def acquire(
        self,
        *,
        run_id: str,
        revision_id: str,
        owner: str,
        ttl: timedelta,
    ) -> LockToken:
        """Acquire single-editor lock or fail if unavailable."""
        raise NotImplementedError

    def heartbeat(self, token: LockToken, ttl: timedelta) -> LockToken:
        """Renew lock lifetime for the token owner."""
        raise NotImplementedError

    def get_active(self, *, run_id: str, revision_id: str) -> Optional[LockToken]:
        """Return currently active lock, if any."""
        raise NotImplementedError

    def release(self, token: LockToken) -> None:
        """Release an active lock owned by token owner."""
        raise NotImplementedError

    def force_release(self, *, run_id: str, revision_id: str, actor: str, reason: str) -> None:
        """Admin/protected override lock release with required reason."""
        raise NotImplementedError
