from net_speed_meter.services.speed_formatter import format_speed


def test_formats_zero_speed() -> None:
    assert format_speed(0) == "0 B/s"


def test_formats_negative_speed_as_zero() -> None:
    assert format_speed(-100) == "0 B/s"


def test_formats_bytes_per_second() -> None:
    assert format_speed(512) == "512.00 B/s"


def test_formats_kilobytes_per_second() -> None:
    assert format_speed(1_024) == "1.00 KB/s"


def test_formats_megabytes_per_second() -> None:
    assert format_speed(1_048_576) == "1.00 MB/s"


def test_formats_gigabytes_per_second() -> None:
    assert format_speed(1_073_741_824) == "1.00 GB/s"