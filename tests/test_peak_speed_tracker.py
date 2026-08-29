from net_speed_meter.core.network_monitor import NetworkSpeed
from net_speed_meter.services.peak_speed_tracker import PeakSpeedTracker


def test_initial_peak_speed_is_zero() -> None:
    tracker = PeakSpeedTracker()

    peak = tracker.get_peak_speed()

    assert peak.download_bytes_per_second == 0.0
    assert peak.upload_bytes_per_second == 0.0


def test_tracks_highest_download_and_upload_speeds() -> None:
    tracker = PeakSpeedTracker()

    tracker.update(
        NetworkSpeed(
            download_bytes_per_second=100.0,
            upload_bytes_per_second=50.0,
        )
    )

    peak = tracker.update(
        NetworkSpeed(
            download_bytes_per_second=80.0,
            upload_bytes_per_second=120.0,
        )
    )

    assert peak.download_bytes_per_second == 100.0
    assert peak.upload_bytes_per_second == 120.0


def test_peak_speed_does_not_decrease() -> None:
    tracker = PeakSpeedTracker()

    tracker.update(
        NetworkSpeed(
            download_bytes_per_second=500.0,
            upload_bytes_per_second=400.0,
        )
    )

    tracker.update(
        NetworkSpeed(
            download_bytes_per_second=100.0,
            upload_bytes_per_second=50.0,
        )
    )

    peak = tracker.get_peak_speed()

    assert peak.download_bytes_per_second == 500.0
    assert peak.upload_bytes_per_second == 400.0


def test_negative_speed_is_treated_as_zero() -> None:
    tracker = PeakSpeedTracker()

    tracker.update(
        NetworkSpeed(
            download_bytes_per_second=-100.0,
            upload_bytes_per_second=-50.0,
        )
    )

    peak = tracker.get_peak_speed()

    assert peak.download_bytes_per_second == 0.0
    assert peak.upload_bytes_per_second == 0.0


def test_reset_clears_peak_speed() -> None:
    tracker = PeakSpeedTracker()

    tracker.update(
        NetworkSpeed(
            download_bytes_per_second=1000.0,
            upload_bytes_per_second=500.0,
        )
    )

    tracker.reset()

    peak = tracker.get_peak_speed()

    assert peak.download_bytes_per_second == 0.0
    assert peak.upload_bytes_per_second == 0.0
