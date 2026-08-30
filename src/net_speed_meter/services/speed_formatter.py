from __future__ import annotations


def format_speed(bytes_per_second: float) -> str:
    """Format a network speed into a human-readable string."""

    if bytes_per_second <= 0:
        return "0 B/s"

    units = ("B/s", "KB/s", "MB/s", "GB/s")
    speed = float(bytes_per_second)

    for unit in units:
        if speed < 1024 or unit == units[-1]:
            return f"{speed:.2f} {unit}"

        speed /= 1024

    return f"{speed:.2f} GB/s"
