from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from net_speed_meter.services.app_paths import (
    get_settings_path,
    get_usage_database_path,
)
from net_speed_meter.services.settings import SettingsManager
from net_speed_meter.services.usage_repository import UsageRepository
from net_speed_meter.services.usage_service import UsageService
from net_speed_meter.ui.widget import SpeedWidget


def main() -> None:
    """Start the ProNet Speed application."""

    app = QApplication(sys.argv)

    settings_manager = SettingsManager(
        get_settings_path(),
    )
    settings = settings_manager.load()

    usage_repository = UsageRepository(
        get_usage_database_path(),
    )
    usage_service = UsageService(
        usage_repository,
    )

    widget = SpeedWidget(
        settings=settings,
        settings_manager=settings_manager,
        usage_service=usage_service,
        usage_repository=usage_repository,
    )
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
