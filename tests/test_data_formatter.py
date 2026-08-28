from net_speed_meter.services.data_formatter import (
    format_data_size,
)


def test_formats_zero_bytes() -> None:
    assert format_data_size(0) == "0 B"


def test_formats_negative_bytes_as_zero() -> None:
    assert format_data_size(-100) == "0 B"


def test_formats_bytes() -> None:
    assert format_data_size(500) == "500 B"


def test_formats_kilobytes() -> None:
    assert format_data_size(1024) == "1.00 KB"


def test_formats_megabytes() -> None:
    assert format_data_size(1024 * 1024) == "1.00 MB"


def test_formats_gigabytes() -> None:
    assert format_data_size(
        1024 * 1024 * 1024
    ) == "1.00 GB"


def test_formats_fractional_megabytes() -> None:
    size = 5_074_942

    assert format_data_size(size) == "4.84 MB"