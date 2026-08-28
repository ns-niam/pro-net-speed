from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from net_speed_meter.services.app_paths import get_settings_path
from net_speed_meter.services.settings import SettingsManager
from net_speed_meter.ui.widget import SpeedWidget


def main() -> None:
    """Start the Net Speed Meter application."""

    app = QApplication(sys.argv)

    settings_manager = SettingsManager(get_settings_path())
    settings = settings_manager.load()

    widget = SpeedWidget(
        settings,
        settings_manager,
    )
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()