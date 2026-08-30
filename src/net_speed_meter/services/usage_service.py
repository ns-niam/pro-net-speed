from __future__ import annotations

from datetime import date

import psutil

from net_speed_meter.core.usage_tracker import (
    UsageSnapshot,
    UsageTracker,
)
from net_speed_meter.services.usage_repository import UsageRepository


class UsageService:
    """Track and persist network usage."""

    def __init__(
        self,
        repository: UsageRepository,
    ) -> None:
        self._repository = repository
        self._tracker = UsageTracker()

    def update(self) -> None:
        """Read current network counters and store new usage."""

        counters = psutil.net_io_counters()

        snapshot = UsageSnapshot(
            bytes_received=counters.bytes_recv,
            bytes_sent=counters.bytes_sent,
        )

        usage = self._tracker.update(snapshot)

        today = date.today().isoformat()

        self._repository.add_usage(
            date=today,
            download_bytes=usage.bytes_received,
            upload_bytes=usage.bytes_sent,
        )
