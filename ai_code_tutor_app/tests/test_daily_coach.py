from dataclasses import dataclass

from daily_coach import (
    daily_session_checklist,
    daily_session_nudge,
    next_unfinished_step,
    streak_repair_message,
    total_step_minutes,
)
from progress import (
    daily_checklist_completion,
    daily_checklist_steps,
    default_progress,
    load_progress,
    record_daily_checklist,
    save_focus_preferences,
)


@dataclass(frozen=True)
class FakeMission:
    day: int = 1
    title: str = "Start Python without fear"
    focus: str = "New lesson"
    proof: str = "Explain print."
    fun_challenge: str = "Change one print message."


def test_daily_coach_full_session_is_30_minutes_and_actionable():
    steps = daily_session_checklist(FakeMission(), "Medium")
    assert total_step_minutes(steps) == 30
    assert [step.id for step in steps] == ["open", "brain_dump", "learn", "practice", "check", "reflect"]
    assert all(step.action for step in steps)
    assert all(step.proof for step in steps)


def test_daily_coach_rescue_session_shrinks_low_energy_days():
    steps = daily_session_checklist(FakeMission(), "Low")
    assert total_step_minutes(steps) == 10
    assert steps[0].label == "Open the app"
    assert "tiny" in daily_session_nudge({}, steps).lower()


def test_daily_checklist_roundtrip_supports_mapping_and_old_iterable_format():
    progress = default_progress(["one"], profile_name="Ava")
    record_daily_checklist(progress, 1, {"open": True, "learn": False})
    assert daily_checklist_steps(progress, 1) == {"open": True, "learn": False}
    assert daily_checklist_completion(progress, 1, ["open", "learn"]) == 0.5

    record_daily_checklist(progress, 2, ["open", "practice"])
    assert daily_checklist_steps(progress, 2) == {"open": True, "practice": True}


def test_next_unfinished_step_and_finish_nudge():
    steps = daily_session_checklist(FakeMission(), "Medium")
    assert next_unfinished_step({"open": True}, steps).id == "brain_dump"
    assert "complete" in daily_session_nudge({step.id: True for step in steps}, steps).lower()


def test_focus_preferences_are_sanitized_from_bad_import(tmp_path):
    path = tmp_path / "progress_bad_focus.json"
    path.write_text(
        '{"focus_preferences": {"default_minutes": "forever", "reward_style": "pressure", "break_reminders": "no"}}',
        encoding="utf-8",
    )
    loaded = load_progress(["one"], path, profile_name="Ava")
    assert loaded["focus_preferences"]["default_minutes"] == 30
    assert loaded["focus_preferences"]["reward_style"] == "Tiny wins"
    assert loaded["focus_preferences"]["break_reminders"] is False

    save_focus_preferences(loaded, {"default_minutes": 999})
    assert loaded["focus_preferences"]["default_minutes"] == 45


def test_streak_repair_message_is_shame_free():
    assert "No streak pressure" in streak_repair_message(0, 0)
    assert "restarted" in streak_repair_message(1, 5).lower()
