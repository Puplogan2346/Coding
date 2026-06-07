from __future__ import annotations

from progress_store import init_db, list_profile_slugs, load_progress_snapshot, save_progress_snapshot, storage_health


def test_sqlite_progress_snapshot_round_trip(tmp_path):
    db_path = tmp_path / "progress.sqlite3"
    init_db(db_path)
    data = {"profile_name": "Ava", "completed_lessons": ["01-python-mindset"], "updated_at": "2026-01-01T00:00:00Z"}
    save_progress_snapshot(db_path, "ava", "Ava", data)

    loaded = load_progress_snapshot(db_path, "ava")
    assert loaded is not None
    assert loaded["completed_lessons"] == ["01-python-mindset"]
    assert list_profile_slugs(db_path) == ["ava"]
    assert storage_health(db_path)["ok"] is True
