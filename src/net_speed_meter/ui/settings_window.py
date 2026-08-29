from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)

from net_speed_meter.services.settings import (
    AppSettings,
    SettingsManager,
)


class SettingsWindow(QDialog):
    """Application settings dialog."""

    def __init__(
        self,
        settings: AppSettings,
        settings_manager: SettingsManager,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._settings = settings
        self._settings_manager = settings_manager

        self.setWindowTitle("ProNet Speed Settings")
        self.setMinimumWidth(360)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create the settings interface."""

        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setSpacing(14)

        self._opacity_slider = QSlider(
            Qt.Orientation.Horizontal,
        )
        self._opacity_slider.setRange(30, 100)
        self._opacity_slider.setValue(
            round(self._settings.opacity * 100),
        )

        self._opacity_label = QLabel()
        self._update_opacity_label(
            self._opacity_slider.value(),
        )

        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(
            self._opacity_slider,
        )
        opacity_layout.addWidget(
            self._opacity_label,
        )

        self._opacity_slider.valueChanged.connect(
            self._update_opacity_label,
        )

        form_layout.addRow(
            "Opacity:",
            opacity_layout,
        )

        self._update_interval_input = QSpinBox()
        self._update_interval_input.setRange(
            250,
            10000,
        )
        self._update_interval_input.setSingleStep(250)
        self._update_interval_input.setSuffix(" ms")
        self._update_interval_input.setValue(
            self._settings.update_interval_ms,
        )

        form_layout.addRow(
            "Update interval:",
            self._update_interval_input,
        )

        self._always_on_top_checkbox = QCheckBox(
            "Keep widget above other windows",
        )
        self._always_on_top_checkbox.setChecked(
            self._settings.always_on_top,
        )

        form_layout.addRow(
            "Always on top:",
            self._always_on_top_checkbox,
        )

        main_layout.addLayout(form_layout)

        main_layout.addStretch()

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel,
        )

        button_box.accepted.connect(
            self._save_settings,
        )
        button_box.rejected.connect(
            self.reject,
        )

        main_layout.addWidget(button_box)

    def _update_opacity_label(
        self,
        value: int,
    ) -> None:
        """Update the opacity percentage label."""

        self._opacity_label.setText(f"{value}%")

    def _save_settings(self) -> None:
        """Save settings and close the dialog."""

        self._settings.opacity = (
            self._opacity_slider.value() / 100
        )
        self._settings.update_interval_ms = (
            self._update_interval_input.value()
        )
        self._settings.always_on_top = (
            self._always_on_top_checkbox.isChecked()
        )

        self._settings_manager.save(
            self._settings,
        )

        self.accept()