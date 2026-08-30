from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UsageSnapshot:
    """Represents total network usage counters."""

    bytes_received: int
    bytes_sent: int


@dataclass(frozen=True)
class UsageDelta:
    """Represents network usage since the previous snapshot."""

    bytes_received: int
    bytes_sent: int


class UsageTracker:
    """Calculate network usage between counter snapshots."""

    def __init__(self) -> None:
        self._previous: UsageSnapshot | None = None

    def update(self, snapshot: UsageSnapshot) -> UsageDelta:
        """Calculate usage since the previous network snapshot."""

        if self._previous is None:
            self._previous = snapshot
            return UsageDelta(
                bytes_received=0,
                bytes_sent=0,
            )

        received_delta = max(
            0,
            snapshot.bytes_received - self._previous.bytes_received,
        )
        sent_delta = max(
            0,
            snapshot.bytes_sent - self._previous.bytes_sent,
        )

        self._previous = snapshot

        return UsageDelta(
            bytes_received=received_delta,
            bytes_sent=sent_delta,
        )
