"""Session contracts for user/workstation context and guarded transitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class SessionContext:
    """Identity and launch context for a client session."""

    session_id: str
    user_id: str
    workstation_id: str
    started_at: datetime


class SessionStore:
    """Contract for creating and resolving active user sessions."""

    def start(self, *, user_id: str, workstation_id: str) -> SessionContext:
        """Create a new session context."""
        raise NotImplementedError

    def get(self, session_id: str) -> Optional[SessionContext]:
        """Look up a session context by ID."""
        raise NotImplementedError

    def end(self, session_id: str) -> None:
        """Terminate an active session context."""
        raise NotImplementedError
