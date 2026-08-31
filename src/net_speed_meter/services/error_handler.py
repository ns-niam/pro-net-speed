from __future__ import annotations

import logging
import sys
import traceback
from pathlib import Path
from types import TracebackType

LOGGER_NAME = "net_speed_meter"


class ErrorHandler:
    """Centralized application error and crash handling."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._logger = logging.getLogger(LOGGER_NAME)

    @property
    def log_path(self) -> Path:
        """Return the application log path."""

        return self._log_path

    def install(self) -> None:
        """Install the global uncaught exception handler."""

        sys.excepthook = self.handle_exception

        self._logger.info(
            "Global error handler installed."
        )

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        """Handle an uncaught exception."""

        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(
                exc_type,
                exc_value,
                exc_traceback,
            )
            return

        self._logger.critical(
            "Unhandled exception: %s: %s",
            exc_type.__name__,
            exc_value,
        )

        self._logger.critical(
            "Traceback:\n%s",
            "".join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    exc_traceback,
                )
            ),
        )

    def report(
        self,
        message: str,
        *,
        exception: BaseException | None = None,
        level: int = logging.ERROR,
    ) -> None:
        """Report a handled application error."""

        if exception is None:
            self._logger.log(
                level,
                "%s",
                message,
            )
            return

        self._logger.log(
            level,
            "%s: %s",
            message,
            exception,
            exc_info=True,
        )
