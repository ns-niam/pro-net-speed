from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
    QVBoxLayout,
    QWidget,
)

from net_speed_meter.core.network_monitor import NetworkMonitor
from net_speed_meter.services.peak_speed_tracker import PeakSpeedTracker
from net_speed_meter.services.settings import AppSettings, SettingsManager
from net_speed_meter.services.speed_formatter import format_speed
from net_speed_meter.services.usage_repository import UsageRepository
from net_speed_meter.services.usage_service import UsageService
from net_speed_meter.ui.settings_window import SettingsWindow
from net_speed_meter.ui.speed_statistics_window import SpeedStatisticsWindow
from net_speed_meter.ui.usage_window import UsageWindow


class SpeedWidget(QWidget):
    """Floating widget that displays real-time network speed."""

    def __init__(
        self,
        settings: AppSettings,
        settings_manager: SettingsManager,
        usage_service: UsageService,
        usage_repository: UsageRepository,
    ) -> None:
        super().__init__()

        self._settings = settings
        self._settings_manager = settings_manager
        self._usage_service = usage_service
        self._usage_repository = usage_repository
        self._usage_window: UsageWindow | None = None
        self._speed_statistics_window: SpeedStatisticsWindow | None = None
        self._peak_speed_tracker = PeakSpeedTracker()
        self._monitor = NetworkMonitor()
        self._drag_position: QPoint | None = None

        self.setWindowTitle("ProNet Speed")
        self.setWindowFlags(self._get_window_flags())
        self.setFixedSize(140, 52)

        self.setWindowOpacity(self._settings.opacity)
        self.move(self._settings.x, self._settings.y)

        self._setup_ui()
        self._setup_timer()

    def _get_window_flags(self) -> Qt.WindowType:
        """Return window flags based on application settings."""

        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool

        if self._settings.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint

        return flags

    def _setup_ui(self) -> None:
        """Create the widget interface."""

        self.setStyleSheet(
            """
            QWidget {
                background-color: #111111;
                border-radius: 12px;
            }

            QLabel {
                color: white;
                font-size: 13px;
                font-weight: 600;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(0)

        self.download_label = QLabel("↓ 0 B/s")
        self.upload_label = QLabel("↑ 0 B/s")

        self.download_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )
        self.upload_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )

        layout.addWidget(self.download_label)
        layout.addWidget(self.upload_label)

    def _setup_timer(self) -> None:
        """Start the non-blocking speed update timer."""

        self._timer = QTimer(self)
        self._timer.setInterval(
            self._settings.update_interval_ms,
        )
        self._timer.timeout.connect(self._update_speed)
        self._timer.start()

    def _update_speed(self) -> None:
        """Update the displayed network speed."""

        try:
            self._usage_service.update()

            speed = self._monitor.get_current_speed()
            self._peak_speed_tracker.update(speed)

            download = format_speed(
                  speed.download_bytes_per_second,
        )
            upload = format_speed(
                speed.upload_bytes_per_second,
        )

            self.download_label.setText(f"↓ {download}")
            self.upload_label.setText(f"↑ {upload}")

            if self._usage_window is not None:
               self._usage_window.refresh()

            if self._speed_statistics_window is not None:
               self._speed_statistics_window.update_speed(speed)

        except Exception:
           import logging

           logging.exception("Network speed update failed")
        self._peak_speed_tracker.update(speed)

        download = format_speed(
            speed.download_bytes_per_second,
        )
        upload = format_speed(
            speed.upload_bytes_per_second,
        )

        self.download_label.setText(f"↓ {download}")
        self.upload_label.setText(f"↑ {upload}")

        if self._usage_window is not None:
            self._usage_window.refresh()

        if self._speed_statistics_window is not None:
            self._speed_statistics_window.update_speed(speed)

    def _show_context_menu(
        self,
        global_position: QPoint,
    ) -> None:
        """Show the widget context menu."""

        menu = QMenu(self)

        menu.setStyleSheet(
            """
            QMenu {
                background-color: #1b1e23;
                color: #f4f4f5;
                border: 1px solid #3f444d;
                border-radius: 8px;
                padding: 6px;
            }

            QMenu::item {
                color: #f4f4f5;
                padding: 8px 28px 8px 12px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color: #2f3742;
                color: #ffffff;
            }

            QMenu::item:disabled {
                color: #7a808a;
            }

            QMenu::separator {
                height: 1px;
                background: #3f444d;
                margin: 5px 8px;
            }
            """
        )

        usage_action = QAction("Data Usage", self)
        usage_action.triggered.connect(
            self._open_usage_window,
        )
        menu.addAction(usage_action)

        speed_statistics_action = QAction(
            "Speed Statistics",
            self,
        )
        speed_statistics_action.triggered.connect(
            self._open_speed_statistics_window,
        )
        menu.addAction(speed_statistics_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(
            self._open_settings,
        )
        menu.addAction(settings_action)

        always_on_top_action = QAction(
            "Always on Top",
            self,
        )
        always_on_top_action.setCheckable(True)
        always_on_top_action.setChecked(
            self._settings.always_on_top,
        )
        always_on_top_action.triggered.connect(
            self._toggle_always_on_top,
        )
        menu.addAction(always_on_top_action)

        menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.quit)
        menu.addAction(exit_action)

        menu.exec(global_position)

    def _open_usage_window(self) -> None:
        """Open or focus the data usage window."""

        if self._usage_window is None:
            self._usage_window = UsageWindow(
                repository=self._usage_repository,
            )

        self._usage_window.refresh()
        self._usage_window.show()
        self._usage_window.raise_()
        self._usage_window.activateWindow()

    def _open_speed_statistics_window(self) -> None:
        """Open or focus the speed statistics window."""

        if self._speed_statistics_window is None:
            self._speed_statistics_window = SpeedStatisticsWindow(
                peak_tracker=self._peak_speed_tracker,
                parent=self,
            )

        self._speed_statistics_window.update_speed(
            self._monitor.get_current_speed(),
        )
        self._speed_statistics_window.show()
        self._speed_statistics_window.raise_()
        self._speed_statistics_window.activateWindow()

    def _open_settings(self) -> None:
        """Open the application settings."""

        settings_window = SettingsWindow(
            settings=self._settings,
            settings_manager=self._settings_manager,
            parent=self,
        )

        if settings_window.exec():
            self._apply_settings()

    def _apply_settings(self) -> None:
        """Apply the current settings to the widget."""

        self.setWindowOpacity(
            self._settings.opacity,
        )

        self._timer.setInterval(
            self._settings.update_interval_ms,
        )

        self.setWindowFlags(
            self._get_window_flags(),
        )

        self.show()

    def _toggle_always_on_top(
        self,
        enabled: bool,
    ) -> None:
        """Toggle the always-on-top window setting."""

        self._settings.always_on_top = enabled
        self._settings_manager.save(self._settings)

        self.setWindowFlags(
            self._get_window_flags(),
        )
        self.show()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events."""

        if event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(
                event.globalPosition().toPoint(),
            )
            event.accept()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """Move the widget while dragging."""

        if (
            event.buttons() & Qt.MouseButton.LeftButton
            and self._drag_position is not None
        ):
            self.move(
                event.globalPosition().toPoint() - self._drag_position,
            )

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Stop dragging the widget and save its position."""

        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = None

            self._settings.x = self.x()
            self._settings.y = self.y()

            self._settings_manager.save(self._settings)

            event.accept()
            return

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event) -> None:
        """Adjust widget opacity with the mouse wheel."""

        delta = event.angleDelta().y()

        if delta == 0:
            event.ignore()
            return

        step = 0.05 if delta > 0 else -0.05

        new_opacity = max(
            0.3,
            min(
                1.0,
                self._settings.opacity + step,
            ),
        )

        self._settings.opacity = round(
            new_opacity,
            2,
        )
        self.setWindowOpacity(
            self._settings.opacity,
        )

        self._settings_manager.save(
            self._settings,
        )

        event.accept()
