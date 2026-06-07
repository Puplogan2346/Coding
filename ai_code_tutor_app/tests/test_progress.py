import json

from progress import (
    app_today,
    add_parking_lot_item,
    close_parking_lot_item,
    completion_percent,
    default_progress,
    load_progress,
    mark_lesson_complete,
    profile_slug,
    progress_path_for_profile,
    record_focus_checkin,
    record_official_ai_resource,
    record_project_milestone,
    record_prompt_score,
    record_quiz_score,
    save_focus_preferences,
    save_note,
    save_progress,
)


def test_profile_slug_is_safe():
    assert profile_slug("Ava Learns Python!") == "ava-learns-python"
    assert profile_slug("   ") == "guest"
    assert profile_slug("x" * 100) == "x" * 48


def test_progress_path_uses_safe_slug():
    path = progress_path_for_profile("Ava Learns Python!")
    assert path.name == "progress_ava-learns-python.json"


def test_default_progress_includes_notes_for_lessons():
    data = default_progress(["one", "two"], profile_name="Ava")
    assert data["profile_name"] == "Ava"
    assert data["notes"] == {"one": "", "two": ""}
    assert data["official_ai_status"] == {}
    assert data["official_ai_notes"] == {}
    assert data["focus_preferences"]["default_minutes"] == 30
    assert data["focus_checkins"] == []
    assert data["parking_lot"] == []
    assert data["project_milestones"] == {}


def test_progress_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "progress.json"
    data = default_progress(["one", "two"], profile_name="Ava")
    mark_lesson_complete(data, "one")
    record_quiz_score(data, "one", score=2, total=3)
    save_note(data, "one", "Remember f-strings")
    record_prompt_score(data, 8, "Please explain Python lists with examples and tests.")
    record_official_ai_resource(data, "gumloop_university", "In progress", "Doing the agent course")
    save_progress(data, path)

    loaded = load_progress(["one", "two"], path, profile_name="Ava")
    assert loaded["completed_lessons"] == ["one"]
    assert loaded["quiz_scores"]["one"]["percent"] == 66.7
    assert loaded["notes"]["one"] == "Remember f-strings"
    assert loaded["prompt_scores"][0]["score"] == 8
    assert loaded["official_ai_status"]["gumloop_university"] == "In progress"
    assert loaded["official_ai_notes"]["gumloop_university"] == "Doing the agent course"
    assert completion_percent(loaded, 2) == 0.5


def test_load_progress_migrates_lesson_ids(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text(
        json.dumps(
            {
                "completed_lessons": ["old", "new"],
                "quiz_scores": {"old": {"percent": 100}, "new": {"percent": 90}},
                "notes": {"old": "remove"},
            }
        ),
        encoding="utf-8",
    )
    loaded = load_progress(["new"], path, profile_name="Ava")
    assert loaded["completed_lessons"] == ["new"]
    assert list(loaded["quiz_scores"].keys()) == ["new"]
    assert "new" in loaded["notes"]


def test_record_official_ai_resource_normalizes_bad_status():
    data = default_progress(["one"], profile_name="Ava")
    record_official_ai_resource(data, "anthropic_academy", "Done-ish", "bad status should normalize")
    assert data["official_ai_status"]["anthropic_academy"] == "Not started"
    assert data["official_ai_notes"]["anthropic_academy"] == "bad status should normalize"


def test_focus_preferences_checkins_and_parking_lot_roundtrip(tmp_path):
    path = tmp_path / "progress_focus.json"
    data = default_progress(["one"], profile_name="Ava")
    save_focus_preferences(data, {"default_minutes": 45, "low_stimulation_mode": True})
    record_focus_checkin(data, "Low", "Scattered", "phone", "opened the lesson")
    assert add_parking_lot_item(data, "Research keyboards later", lesson_id="one") is True
    assert add_parking_lot_item(data, "   ") is False
    assert close_parking_lot_item(data, 0) is True
    assert close_parking_lot_item(data, 99) is False
    save_progress(data, path)

    loaded = load_progress(["one"], path, profile_name="Ava")
    assert loaded["focus_preferences"]["default_minutes"] == 45
    assert loaded["focus_preferences"]["low_stimulation_mode"] is True
    assert loaded["focus_checkins"][0]["win"] == "opened the lesson"
    assert loaded["parking_lot"][0]["status"] == "Closed"


def test_record_project_milestone_normalizes_bad_status():
    data = default_progress(["one"], profile_name="Ava")
    record_project_milestone(data, "quiz_scorekeeper", "plan", "Done-ish", "messy note")
    saved = data["project_milestones"]["quiz_scorekeeper"]["plan"]
    assert saved["status"] == "In progress"
    assert saved["note"] == "messy note"


def test_app_today_uses_configurable_timezone_without_crashing(monkeypatch):
    monkeypatch.setenv("APP_TIMEZONE", "America/Los_Angeles")
    assert hasattr(app_today(), "isoformat")
    monkeypatch.setenv("APP_TIMEZONE", "Invalid/Timezone")
    assert hasattr(app_today(), "isoformat")
