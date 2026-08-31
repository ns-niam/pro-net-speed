from __future__ import annotations

import logging
import os
import sys
import traceback
from pathlib import Path

from PySide6.QtWidgets import QApplication

from net_speed_meter.services.app_paths import (
    get_app_data_directory,
    get_settings_path,
    get_usage_database_path,
)
from net_speed_meter.services.settings import SettingsManager
from net_speed_meter.services.usage_repository import UsageRepository
from net_speed_meter.services.usage_service import UsageService
from net_speed_meter.ui.widget import SpeedWidget


def get_log_path() -> Path:
    """Return the application's crash log path."""

    log_directory = get_app_data_directory()
    log_directory.mkdir(parents=True, exist_ok=True)

    return log_directory / "pronet_speed.log"


def configure_logging() -> None:
    """Configure application logging."""

    logging.basicConfig(
        filename=get_log_path(),
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def install_exception_handler() -> None:
    """Write uncaught exceptions to the application log."""

    def handle_exception(
        exception_type,
        exception_value,
        exception_traceback,
    ) -> None:
        if issubclass(exception_type, KeyboardInterrupt):
            sys.__excepthook__(
                exception_type,
                exception_value,
                exception_traceback,
            )
            return

        logging.critical(
            "Unhandled exception",
            exc_info=(
                exception_type,
                exception_value,
                exception_traceback,
            ),
        )

    sys.excepthook = handle_exception


def main() -> None:
    """Start the ProNet Speed application."""

    configure_logging()
    install_exception_handler()

    logging.info("========================================")
    logging.info("Starting ProNet Speed")
    logging.info("Python: %s", sys.version)
    logging.info("Executable: %s", sys.executable)
    logging.info("Working directory: %s", os.getcwd())
    logging.info("App data directory: %s", get_app_data_directory())
    logging.info("========================================")

    try:
        logging.info("Creating QApplication...")
        app = QApplication(sys.argv)

        logging.info("Loading settings...")
        settings_manager = SettingsManager(
            get_settings_path(),
        )
        settings = settings_manager.load()

        logging.info("Opening usage repository...")
        usage_repository = UsageRepository(
            get_usage_database_path(),
        )

        logging.info("Creating usage service...")
        usage_service = UsageService(
            usage_repository,
        )

        logging.info("Creating SpeedWidget...")
        widget = SpeedWidget(
            settings=settings,
            settings_manager=settings_manager,
            usage_service=usage_service,
            usage_repository=usage_repository,
        )

        logging.info("Showing SpeedWidget...")
        widget.show()

        logging.info("Application event loop starting...")
        exit_code = app.exec()

        logging.info(
            "Application event loop exited with code %s",
            exit_code,
        )

        sys.exit(exit_code)

    except Exception:
        logging.critical(
            "Application startup failed:\n%s",
            traceback.format_exc(),
        )
        raise


if __name__ == "__main__":
    main()