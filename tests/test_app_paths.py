from pathlib import Path

from net_speed_meter.services.app_paths import (
    APP_NAME,
    get_app_data_directory,
    get_settings_path,
)


def test_uses_local_app_data_when_available(monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", "/tmp/local-app-data")

    expected = Path("/tmp/local-app-data") / APP_NAME

    assert get_app_data_directory() == expected


def test_uses_home_directory_as_fallback(monkeypatch) -> None:
    monkeypatch.delenv("LOCALAPPDATA", raising=False)

    expected = Path.home() / ".net-speed-meter"

    assert get_app_data_directory() == expected


def test_settings_path_is_inside_app_data_directory(
    monkeypatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", "/tmp/local-app-data")

    expected = (
        Path("/tmp/local-app-data")
        / APP_NAME
        / "settings.json"
    )

    assert get_settings_path() == expected