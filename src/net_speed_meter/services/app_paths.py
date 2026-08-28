from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "Net Speed Meter"


def get_app_data_directory() -> Path:
    """Return the application's user-specific data directory."""

    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        return Path(local_app_data) / APP_NAME

    return Path.home() / ".net-speed-meter"


def get_settings_path() -> Path:
    """Return the path used to store application settings."""

    return get_app_data_directory() / "settings.json"