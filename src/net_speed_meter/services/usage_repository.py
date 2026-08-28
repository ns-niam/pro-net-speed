from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DailyUsage:
    """Represents network usage for a single day."""

    date: str
    download_bytes: int
    upload_bytes: int

    @property
    def total_bytes(self) -> int:
        """Return the total network usage."""

        return self.download_bytes + self.upload_bytes


class UsageRepository:
    """Store and retrieve daily network usage with SQLite."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        """Create a connection to the usage database."""

        return sqlite3.connect(self._database_path)

    def _initialize_database(self) -> None:
        """Create the required database tables."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_usage (
                    date TEXT PRIMARY KEY,
                    download_bytes INTEGER NOT NULL DEFAULT 0,
                    upload_bytes INTEGER NOT NULL DEFAULT 0
                )
                """
            )

    def add_usage(
        self,
        date: str,
        download_bytes: int,
        upload_bytes: int,
    ) -> None:
        """Add network usage to a specific day."""

        safe_download = max(0, download_bytes)
        safe_upload = max(0, upload_bytes)

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO daily_usage (
                    date,
                    download_bytes,
                    upload_bytes
                )
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    download_bytes =
                        download_bytes + excluded.download_bytes,
                    upload_bytes =
                        upload_bytes + excluded.upload_bytes
                """,
                (
                    date,
                    safe_download,
                    safe_upload,
                ),
            )

    def get_daily_usage(
        self,
        date: str,
    ) -> DailyUsage:
        """Return usage for a specific day."""

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    date,
                    download_bytes,
                    upload_bytes
                FROM daily_usage
                WHERE date = ?
                """,
                (date,),
            ).fetchone()

        if row is None:
            return DailyUsage(
                date=date,
                download_bytes=0,
                upload_bytes=0,
            )

        return DailyUsage(
            date=row[0],
            download_bytes=row[1],
            upload_bytes=row[2],
        )

    def get_monthly_usage(
        self,
        year: int,
        month: int,
    ) -> DailyUsage:
        """Return total network usage for a month."""

        prefix = f"{year:04d}-{month:02d}-%"

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    COALESCE(SUM(download_bytes), 0),
                    COALESCE(SUM(upload_bytes), 0)
                FROM daily_usage
                WHERE date LIKE ?
                """,
                (prefix,),
            ).fetchone()

        return DailyUsage(
            date=f"{year:04d}-{month:02d}",
            download_bytes=row[0],
            upload_bytes=row[1],
        )

    def get_monthly_history(
        self,
        year: int,
        month: int,
    ) -> list[DailyUsage]:
        """Return daily usage records for a month."""

        prefix = f"{year:04d}-{month:02d}-%"

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    date,
                    download_bytes,
                    upload_bytes
                FROM daily_usage
                WHERE date LIKE ?
                ORDER BY date DESC
                """,
                (prefix,),
            ).fetchall()

        return [
            DailyUsage(
                date=row[0],
                download_bytes=row[1],
                upload_bytes=row[2],
            )
            for row in rows
        ]