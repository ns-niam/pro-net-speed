from unittest.mock import ANY, Mock, patch

from net_speed_meter.services.usage_service import UsageService


def test_first_update_stores_zero_usage() -> None:
    repository = Mock()

    service = UsageService(repository)

    counters = Mock(
        bytes_recv=1_000,
        bytes_sent=500,
    )

    with patch(
        "net_speed_meter.services.usage_service.psutil.net_io_counters",
        return_value=counters,
    ):
        service.update()

    repository.add_usage.assert_called_once_with(
        date=ANY,
        download_bytes=0,
        upload_bytes=0,
    )


def test_second_update_stores_network_usage() -> None:
    repository = Mock()

    service = UsageService(repository)

    first_counters = Mock(
        bytes_recv=1_000,
        bytes_sent=500,
    )

    second_counters = Mock(
        bytes_recv=1_500,
        bytes_sent=800,
    )

    with patch(
        "net_speed_meter.services.usage_service.psutil.net_io_counters",
        side_effect=[
            first_counters,
            second_counters,
        ],
    ):
        service.update()
        service.update()

    assert repository.add_usage.call_count == 2

    repository.add_usage.assert_called_with(
        date=ANY,
        download_bytes=500,
        upload_bytes=300,
    )