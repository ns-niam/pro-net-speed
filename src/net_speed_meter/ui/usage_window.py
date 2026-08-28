from __future__ import annotations

from datetime import date

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from net_speed_meter.services.data_formatter import format_data
from net_speed_meter.services.usage_repository import (
    DailyUsage,
    UsageRepository,
)


class UsageWindow(QDialog):
    """Display monthly and daily network usage."""

    def __init__(
        self,
        repository: UsageRepository,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._repository = repository

        self.setWindowTitle("Data Usage")
        self.setMinimumSize(420, 360)

        self._setup_ui()
        self._load_usage()

    def _setup_ui(self) -> None:
        """Create the usage history interface."""

        layout = QVBoxLayout(self)

        self._month_label = QLabel()
        self._month_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: 600;
            """
        )

        self._total_label = QLabel()
        self._total_label.setStyleSheet(
            """
            font-size: 15px;
            font-weight: 600;
            """
        )

        summary_layout = QHBoxLayout()
        summary_layout.addWidget(self._month_label)
        summary_layout.addStretch()
        summary_layout.addWidget(self._total_label)

        layout.addLayout(summary_layout)

        self._download_label = QLabel()
        self._upload_label = QLabel()

        layout.addWidget(self._download_label)
        layout.addWidget(self._upload_label)

        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(
            [
                "Date",
                "Download",
                "Upload",
                "Total",
            ]
        )

        self._table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers,
        )
        self._table.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection,
        )

        self._table.horizontalHeader().setStretchLastSection(
            True,
        )

        layout.addWidget(self._table)

    def _load_usage(self) -> None:
        """Load current month's usage data."""

        today = date.today()

        monthly_usage = self._repository.get_monthly_usage(
            today.year,
            today.month,
        )

        history = self._repository.get_monthly_history(
            today.year,
            today.month,
        )

        self._month_label.setText(
            today.strftime("%B %Y"),
        )

        self._total_label.setText(
            f"Total: {format_data(monthly_usage.total_bytes)}",
        )

        self._download_label.setText(
            f"Download: "
            f"{format_data(monthly_usage.download_bytes)}",
        )

        self._upload_label.setText(
            f"Upload: "
            f"{format_data(monthly_usage.upload_bytes)}",
        )

        self._populate_table(history)

    def _populate_table(
        self,
        history: list[DailyUsage],
    ) -> None:
        """Populate the daily usage table."""

        self._table.setRowCount(len(history))

        for row_index, usage in enumerate(history):
            values = [
                usage.date,
                format_data(usage.download_bytes),
                format_data(usage.upload_bytes),
                format_data(usage.total_bytes),
            ]

            for column_index, value in enumerate(values):
                self._table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(value),
                )