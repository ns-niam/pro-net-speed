from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

APP_NAME = "ProNet Speed"
LOGGER_NAME = "net_speed_meter"


def get_log_path() -> Path:
    """Return the application's writable log path."""

    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        base_directory = Path(local_app_data)
    else:
        base_directory = Path.home() / ".local" / "share"

    app_directory = base_directory / APP_NAME
    app_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return app_directory / "pronet_speed.log"


def configure_logging() -> Path:
    """Configure application logging before loading Qt."""

    log_path = get_log_path()

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        encoding="utf-8",
        force=True,
    )

    return log_path


def main() -> int:
    """Application entry point."""

    log_path = configure_logging()
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("=" * 60)
    logger.info("Starting %s", APP_NAME)
    logger.info("Executable: %s", sys.executable)
    logger.info("Python version: %s", sys.version)
    logger.info("Platform: %s", sys.platform)
    logger.info("Working directory: %s", Path.cwd())
    logger.info("Log file: %s", log_path)

    try:
        # Import Qt only after logging has been initialized.
        logger.info("Importing PySide6.")

        from PySide6.QtWidgets import QApplication

        logger.info("PySide6 imported successfully.")

        # Import application services.
        logger.info("Importing application modules.")

        from net_speed_meter.services.app_paths import (
            get_settings_path,
            get_usage_database_path,
        )
        from net_speed_meter.services.error_handler import ErrorHandler
        from net_speed_meter.services.settings import SettingsManager
        from net_speed_meter.services.usage_repository import UsageRepository
        from net_speed_meter.services.usage_service import UsageService
        from net_speed_meter.ui.widget import SpeedWidget

        logger.info("Application modules imported successfully.")

        # Install global error handling.
        error_handler = ErrorHandler(log_path)
        error_handler.install()

        logger.info("Creating QApplication.")

        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationDisplayName(APP_NAME)
        app.setOrganizationName("Niam Software")
        app.setOrganizationDomain("niam.software")

        logger.info("QApplication created successfully.")

        # Settings.
        logger.info("Initializing settings manager.")

        settings_manager = SettingsManager(
            get_settings_path(),
        )

        settings = settings_manager.load()

        logger.info(
            "Settings loaded successfully: %r",
            settings,
        )

        # Usage database.
        logger.info("Initializing usage repository.")

        usage_repository = UsageRepository(
            get_usage_database_path(),
        )

        logger.info("Usage repository initialized.")

        # Usage service.
        logger.info("Initializing usage service.")

        usage_service = UsageService(
            usage_repository,
        )

        logger.info("Usage service initialized.")

        # Main widget.
        logger.info("Creating main application widget.")

        widget = SpeedWidget(
            settings=settings,
            settings_manager=settings_manager,
            usage_service=usage_service,
            usage_repository=usage_repository,
        )

        logger.info("Main application widget created.")

        widget.show()

        logger.info("Main application widget displayed.")
        logger.info("Starting Qt event loop.")

        exit_code = app.exec()

        logger.info(
            "Qt event loop exited with code %s.",
            exit_code,
        )

        return exit_code

    except Exception as exc:
        logger = logging.getLogger(LOGGER_NAME)

        logger.critical(
            "Fatal application startup error: %s: %s",
            type(exc).__name__,
            exc,
            exc_info=True,
        )

        # If Qt is already available, try to show a useful message.
        try:
            from PySide6.QtWidgets import QApplication, QMessageBox

            application = QApplication.instance()

            if application is not None:
                QMessageBox.critical(
                    None,
                    APP_NAME,
                    (
                        "ProNet Speed could not start correctly.\n\n"
                        f"{type(exc).__name__}: {exc}\n\n"
                        f"Diagnostic log:\n{log_path}"
                    ),
                )
        except Exception:
            # Never allow error reporting itself to create another crash.
            logger.exception(
                "Failed to display startup error dialog."
            )

        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
    except BaseException:
        logging.getLogger(LOGGER_NAME).critical(
            "Fatal process-level error.",
            exc_info=True,
        )
        exit_code = 1

    raise SystemExit(exit_code)