from net_speed_meter.core.usage_tracker import (
    UsageSnapshot,
    UsageTracker,
)


def test_first_update_returns_zero_usage() -> None:
    tracker = UsageTracker()

    delta = tracker.update(
        UsageSnapshot(
            bytes_received=1_000,
            bytes_sent=500,
        )
    )

    assert delta.bytes_received == 0
    assert delta.bytes_sent == 0


def test_calculates_usage_between_snapshots() -> None:
    tracker = UsageTracker()

    tracker.update(
        UsageSnapshot(
            bytes_received=1_000,
            bytes_sent=500,
        )
    )

    delta = tracker.update(
        UsageSnapshot(
            bytes_received=1_500,
            bytes_sent=800,
        )
    )

    assert delta.bytes_received == 500
    assert delta.bytes_sent == 300


def test_negative_counter_difference_returns_zero() -> None:
    tracker = UsageTracker()

    tracker.update(
        UsageSnapshot(
            bytes_received=2_000,
            bytes_sent=1_000,
        )
    )

    delta = tracker.update(
        UsageSnapshot(
            bytes_received=1_000,
            bytes_sent=500,
        )
    )

    assert delta.bytes_received == 0
    assert delta.bytes_sent == 0


def test_updates_previous_snapshot_after_each_update() -> None:
    tracker = UsageTracker()

    tracker.update(
        UsageSnapshot(
            bytes_received=1_000,
            bytes_sent=1_000,
        )
    )

    tracker.update(
        UsageSnapshot(
            bytes_received=1_500,
            bytes_sent=1_200,
        )
    )

    delta = tracker.update(
        UsageSnapshot(
            bytes_received=2_000,
            bytes_sent=1_500,
        )
    )

    assert delta.bytes_received == 500
    assert delta.bytes_sent == 300