from __future__ import annotations

from unittest.mock import Mock, patch

from net_speed_meter.core.network_monitor import NetworkMonitor


def test_initializes_with_current_network_counters() -> None:
    """The monitor should store the initial network counters."""

    counters = Mock(bytes_recv=1_000, bytes_sent=500)

    with patch(
        "net_speed_meter.core.network_monitor.psutil.net_io_counters",
        return_value=counters,
    ):
        with patch(
            "net_speed_meter.core.network_monitor.time.perf_counter",
            return_value=10.0,
        ):
            monitor = NetworkMonitor()

    assert monitor is not None


def test_calculates_download_and_upload_speed() -> None:
    """The monitor should calculate network speed from counter changes."""

    initial_counters = Mock(bytes_recv=1_000, bytes_sent=500)
    current_counters = Mock(bytes_recv=3_000, bytes_sent=1_500)

    with patch(
        "net_speed_meter.core.network_monitor.psutil.net_io_counters",
        side_effect=[initial_counters, current_counters],
    ):
        with patch(
            "net_speed_meter.core.network_monitor.time.perf_counter",
            side_effect=[10.0, 12.0],
        ):
            monitor = NetworkMonitor()
            speed = monitor.get_current_speed()

    assert speed.download_bytes_per_second == 1_000.0
    assert speed.upload_bytes_per_second == 500.0


def test_negative_counter_difference_returns_zero_speed() -> None:
    """The monitor should never return negative network speeds."""

    initial_counters = Mock(bytes_recv=3_000, bytes_sent=2_000)
    current_counters = Mock(bytes_recv=1_000, bytes_sent=500)

    with patch(
        "net_speed_meter.core.network_monitor.psutil.net_io_counters",
        side_effect=[initial_counters, current_counters],
    ):
        with patch(
            "net_speed_meter.core.network_monitor.time.perf_counter",
            side_effect=[10.0, 11.0],
        ):
            monitor = NetworkMonitor()
            speed = monitor.get_current_speed()

    assert speed.download_bytes_per_second == 0.0
    assert speed.upload_bytes_per_second == 0.0


def test_zero_elapsed_time_returns_zero_speed() -> None:
    """The monitor should safely handle zero elapsed time."""

    counters = Mock(bytes_recv=1_000, bytes_sent=500)

    with patch(
        "net_speed_meter.core.network_monitor.psutil.net_io_counters",
        return_value=counters,
    ):
        with patch(
            "net_speed_meter.core.network_monitor.time.perf_counter",
            side_effect=[10.0, 10.0],
        ):
            monitor = NetworkMonitor()
            speed = monitor.get_current_speed()

    assert speed.download_bytes_per_second == 0.0
    assert speed.upload_bytes_per_second == 0.0
