from __future__ import annotations


def format_data_size(size_in_bytes: int | float) -> str:
    """Format a byte value as a human-readable data size."""

    safe_size = max(0, float(size_in_bytes))

    units = ("B", "KB", "MB", "GB", "TB")
    value = safe_size

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{value:.0f} {unit}"

            return f"{value:.2f} {unit}"

        value /= 1024

    return "0 B"
