from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class AppSettings:
    """Application settings."""

    x: int = 100
    y: int = 100
    opacity: float = 0.9
    always_on_top: bool = True
    update_interval_ms: int = 1_000


class SettingsManager:
    """Loads and saves application settings."""

    def __init__(self, settings_path: Path) -> None:
        self._settings_path = settings_path

    def load(self) -> AppSettings:
        """Load settings, returning defaults if unavailable or invalid."""

        if not self._settings_path.exists():
            return AppSettings()

        try:
            with self._settings_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            return AppSettings(
                x=int(data.get("x", 100)),
                y=int(data.get("y", 100)),
                opacity=float(data.get("opacity", 0.9)),
                always_on_top=bool(data.get("always_on_top", True)),
                update_interval_ms=int(data.get("update_interval_ms", 1_000)),
            )
        except (
            OSError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ):
            return AppSettings()

    def save(self, settings: AppSettings) -> None:
        """Save settings to disk."""

        self._settings_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._settings_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                asdict(settings),
                file,
                indent=2,
            )
