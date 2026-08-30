from pathlib import Path

from net_speed_meter.services.usage_repository import (
    UsageRepository,
)


def test_returns_zero_for_missing_daily_usage(
    tmp_path: Path,
) -> None:
    repository = UsageRepository(tmp_path / "usage.db")

    usage = repository.get_daily_usage("2026-08-29")

    assert usage.download_bytes == 0
    assert usage.upload_bytes == 0
    assert usage.total_bytes == 0


def test_adds_and_retrieves_daily_usage(
    tmp_path: Path,
) -> None:
    repository = UsageRepository(tmp_path / "usage.db")

    repository.add_usage(
        date="2026-08-29",
        download_bytes=1_000,
        upload_bytes=500,
    )

    usage = repository.get_daily_usage("2026-08-29")

    assert usage.download_bytes == 1_000
    assert usage.upload_bytes == 500
    assert usage.total_bytes == 1_500


def test_accumulates_usage_for_same_day(
    tmp_path: Path,
) -> None:
    repository = UsageRepository(tmp_path / "usage.db")

    repository.add_usage(
        date="2026-08-29",
        download_bytes=1_000,
        upload_bytes=500,
    )

    repository.add_usage(
        date="2026-08-29",
        download_bytes=2_000,
        upload_bytes=300,
    )

    usage = repository.get_daily_usage("2026-08-29")

    assert usage.download_bytes == 3_000
    assert usage.upload_bytes == 800


def test_negative_usage_is_stored_as_zero(
    tmp_path: Path,
) -> None:
    repository = UsageRepository(tmp_path / "usage.db")

    repository.add_usage(
        date="2026-08-29",
        download_bytes=-100,
        upload_bytes=-200,
    )

    usage = repository.get_daily_usage("2026-08-29")

    assert usage.download_bytes == 0
    assert usage.upload_bytes == 0


def test_calculates_monthly_usage(
    tmp_path: Path,
) -> None:
    repository = UsageRepository(tmp_path / "usage.db")

    repository.add_usage(
        date="2026-08-28",
        download_bytes=1_000,
        upload_bytes=500,
    )

    repository.add_usage(
        date="2026-08-29",
        download_bytes=2_000,
        upload_bytes=300,
    )

    repository.add_usage(
        date="2026-09-01",
        download_bytes=9_000,
        upload_bytes=9_000,
    )

    usage = repository.get_monthly_usage(
        year=2026,
        month=8,
    )

    assert usage.download_bytes == 3_000
    assert usage.upload_bytes == 800
    assert usage.total_bytes == 3_800


def test_returns_monthly_history_in_descending_order(
    tmp_path: Path,
) -> None:
    repository = UsageRepository(tmp_path / "usage.db")

    repository.add_usage(
        date="2026-08-27",
        download_bytes=100,
        upload_bytes=10,
    )

    repository.add_usage(
        date="2026-08-29",
        download_bytes=200,
        upload_bytes=20,
    )

    repository.add_usage(
        date="2026-08-28",
        download_bytes=300,
        upload_bytes=30,
    )

    history = repository.get_monthly_history(
        year=2026,
        month=8,
    )

    assert [usage.date for usage in history] == [
        "2026-08-29",
        "2026-08-28",
        "2026-08-27",
    ]
