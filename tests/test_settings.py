from __future__ import annotations

import json

from net_speed_meter.services.settings import (
    AppSettings,
    SettingsManager,
)


def test_returns_default_settings_when_file_does_not_exist(
    tmp_path,
) -> None:
    settings_path = tmp_path / "settings.json"
    manager = SettingsManager(settings_path)

    settings = manager.load()

    assert settings == AppSettings()


def test_saves_and_loads_settings(tmp_path) -> None:
    settings_path = tmp_path / "settings.json"
    manager = SettingsManager(settings_path)

    original_settings = AppSettings(
        x=250,
        y=400,
        opacity=0.75,
        always_on_top=False,
        update_interval_ms=500,
    )

    manager.save(original_settings)
    loaded_settings = manager.load()

    assert loaded_settings == original_settings


def test_returns_defaults_for_invalid_json(tmp_path) -> None:
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    manager = SettingsManager(settings_path)

    assert manager.load() == AppSettings()


def test_loads_available_values_and_defaults_missing_values(
    tmp_path,
) -> None:
    settings_path = tmp_path / "settings.json"

    data = {
        "x": 500,
        "opacity": 0.8,
    }

    settings_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    manager = SettingsManager(settings_path)
    settings = manager.load()

    assert settings.x == 500
    assert settings.y == 100
    assert settings.opacity == 0.8
    assert settings.always_on_top is True
    assert settings.update_interval_ms == 1_000