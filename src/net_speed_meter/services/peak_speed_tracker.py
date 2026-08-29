from __future__ import annotations

from dataclasses import dataclass

from net_speed_meter.core.network_monitor import NetworkSpeed


@dataclass(frozen=True, slots=True)
class PeakNetworkSpeed:
    """Represents the highest observed network speeds."""

    download_bytes_per_second: float
    upload_bytes_per_second: float


class PeakSpeedTracker:
    """Tracks the highest observed download and upload speeds."""

    def __init__(self) -> None:
        self._peak_download = 0.0
        self._peak_upload = 0.0

    def update(self, speed: NetworkSpeed) -> PeakNetworkSpeed:
        """Update and return the highest observed network speeds."""

        self._peak_download = max(
            self._peak_download,
            max(0.0, speed.download_bytes_per_second),
        )

        self._peak_upload = max(
            self._peak_upload,
            max(0.0, speed.upload_bytes_per_second),
        )

        return self.get_peak_speed()

    def get_peak_speed(self) -> PeakNetworkSpeed:
        """Return the current highest observed speeds."""

        return PeakNetworkSpeed(
            download_bytes_per_second=self._peak_download,
            upload_bytes_per_second=self._peak_upload,
        )

    def reset(self) -> None:
        """Reset all recorded peak speeds to zero."""

        self._peak_download = 0.0
        self._peak_upload = 0.0
