from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from net_speed_meter.core.network_monitor import NetworkSpeed
from net_speed_meter.services.peak_speed_tracker import (
    PeakNetworkSpeed,
    PeakSpeedTracker,
)
from net_speed_meter.services.speed_formatter import format_speed


class SpeedStatisticsWindow(QDialog):
    """Display current and peak network speeds."""

    def __init__(
        self,
        peak_tracker: PeakSpeedTracker,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._peak_tracker = peak_tracker

        self.setWindowTitle("ProNet Speed Statistics")
        self.setMinimumSize(360, 280)

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Create the speed statistics interface."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        title = QLabel("Speed Statistics")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        self._download_current_label = QLabel()
        self._download_peak_label = QLabel()

        download_section = self._create_section(
            "↓ DOWNLOAD",
            self._download_current_label,
            self._download_peak_label,
        )

        self._upload_current_label = QLabel()
        self._upload_peak_label = QLabel()

        upload_section = self._create_section(
            "↑ UPLOAD",
            self._upload_current_label,
            self._upload_peak_label,
        )

        layout.addLayout(download_section)
        layout.addLayout(upload_section)

        layout.addStretch()

        self._reset_button = QPushButton("Reset Peak")
        self._reset_button.clicked.connect(
            self._reset_peak,
        )

        layout.addWidget(self._reset_button)

    def _create_section(
        self,
        heading: str,
        current_label: QLabel,
        peak_label: QLabel,
    ) -> QVBoxLayout:
        """Create a download or upload statistics section."""

        section = QVBoxLayout()
        section.setSpacing(6)

        heading_label = QLabel(heading)
        heading_label.setObjectName("sectionHeading")

        current_layout = QHBoxLayout()
        current_title = QLabel("Current:")
        current_label.setObjectName("speedValue")

        current_layout.addWidget(current_title)
        current_layout.addStretch()
        current_layout.addWidget(current_label)

        peak_layout = QHBoxLayout()
        peak_title = QLabel("Peak:")
        peak_label.setObjectName("peakValue")

        peak_layout.addWidget(peak_title)
        peak_layout.addStretch()
        peak_layout.addWidget(peak_label)

        section.addWidget(heading_label)
        section.addLayout(current_layout)
        section.addLayout(peak_layout)

        return section

    def update_speed(
        self,
        current_speed: NetworkSpeed,
    ) -> None:
        """Update current and peak speed values."""

        peak_speed = self._peak_tracker.get_peak_speed()

        self._update_labels(
            current_speed,
            peak_speed,
        )

    def _update_labels(
        self,
        current_speed: NetworkSpeed,
        peak_speed: PeakNetworkSpeed,
    ) -> None:
        """Update all speed labels."""

        self._download_current_label.setText(
            format_speed(
                current_speed.download_bytes_per_second,
            )
        )

        self._download_peak_label.setText(
            format_speed(
                peak_speed.download_bytes_per_second,
            )
        )

        self._upload_current_label.setText(
            format_speed(
                current_speed.upload_bytes_per_second,
            )
        )

        self._upload_peak_label.setText(
            format_speed(
                peak_speed.upload_bytes_per_second,
            )
        )

    def _reset_peak(self) -> None:
        """Reset recorded peak speeds."""

        self._peak_tracker.reset()

    def _apply_styles(self) -> None:
        """Apply the ProNet Speed dark theme."""

        self.setStyleSheet(
            """
            QDialog {
                background-color: #15171a;
                color: #f4f4f5;
            }

            QLabel {
                color: #d4d4d8;
                font-size: 14px;
            }

            QLabel#title {
                color: #ffffff;
                font-size: 20px;
                font-weight: 700;
                padding-bottom: 8px;
            }

            QLabel#sectionHeading {
                color: #7dd3fc;
                font-size: 15px;
                font-weight: 700;
                padding-top: 6px;
            }

            QLabel#speedValue {
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
            }

            QLabel#peakValue {
                color: #86efac;
                font-size: 15px;
                font-weight: 700;
            }

            QPushButton {
                background-color: #262b33;
                color: #ffffff;
                border: 1px solid #454c56;
                border-radius: 7px;
                padding: 9px 16px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #343b46;
                border-color: #38bdf8;
            }

            QPushButton:pressed {
                background-color: #1e88c8;
            }
            """
        )
