from __future__ import annotations

import time
from dataclasses import dataclass

import psutil


@dataclass(frozen=True, slots=True)
class NetworkSpeed:
    """Represents current network upload and download speeds in bytes/second."""

    download_bytes_per_second: float
    upload_bytes_per_second: float


class NetworkMonitor:
    """Calculates real-time network speed without blocking the UI thread."""

    def __init__(self) -> None:
        counters = psutil.net_io_counters()

        self._previous_bytes_received = counters.bytes_recv
        self._previous_bytes_sent = counters.bytes_sent
        self._previous_timestamp = time.perf_counter()

    def get_current_speed(self) -> NetworkSpeed:
        """Return the current download and upload speed."""

        counters = psutil.net_io_counters()
        current_timestamp = time.perf_counter()

        elapsed_time = current_timestamp - self._previous_timestamp

        if elapsed_time <= 0:
            return NetworkSpeed(
                download_bytes_per_second=0.0,
                upload_bytes_per_second=0.0,
            )

        received_bytes = max(
            0,
            counters.bytes_recv - self._previous_bytes_received,
        )

        sent_bytes = max(
            0,
            counters.bytes_sent - self._previous_bytes_sent,
        )

        download_speed = received_bytes / elapsed_time
        upload_speed = sent_bytes / elapsed_time

        self._previous_bytes_received = counters.bytes_recv
        self._previous_bytes_sent = counters.bytes_sent
        self._previous_timestamp = current_timestamp

        return NetworkSpeed(
            download_bytes_per_second=download_speed,
            upload_bytes_per_second=upload_speed,
        )