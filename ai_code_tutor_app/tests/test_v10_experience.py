from daily_coach import daily_session_checklist
from experience import (
    checklist_completion_from_state,
    coach_header_summary,
    merge_step_state,
    pace_coach_copy,
    quick_win_message,
    timeline_legend_counts,
)
from progress import default_progress, record_daily_checklist, record_daily_mission
from study_plan import mission_by_day
from experience import daily_timeline


def test_merge_step_state_makes_unsaved_checkbox_changes_visible():
    mission = mission_by_day(1)
    steps = daily_session_checklist(mission, "Medium")
    saved = {"open": True}
    session_values = {f"coach_step_{mission.day}_brain_dump": True}

    merged = merge_step_state(saved, session_values, mission.day, steps)

    assert merged["open"] is True
    assert merged["brain_dump"] is True
    assert checklist_completion_from_state(merged, steps) == 0.333


def test_quick_win_message_guides_without_pressure():
    assert "first two-minute action" in quick_win_message(0)
    assert "Momentum" in quick_win_message(0.5)
    assert "Checklist done" in quick_win_message(1.0)
    assert "Win saved" in quick_win_message(1.0, mission_complete=True)


def test_coach_header_summary_and_pace_copy_are_adhd_friendly():
    headline, subline, support = coach_header_summary("Start Python", 0, "10 min rescue", streak=0)
    assert headline == "Today’s job: Start Python"
    assert "10 min rescue" in subline
    assert "Rescue mode counts" in subline
    assert "No streak" in support
    assert "Deep dive mode" in pace_coach_copy("45 min deep dive")


def test_timeline_legend_counts_support_accessible_legend():
    progress = default_progress(["01-python-mindset"], profile_name="Ava")
    record_daily_mission(progress, 1, status="Completed")
    record_daily_checklist(progress, 2, {"open": True})
    days = daily_timeline(progress, total_days=4)
    counts = timeline_legend_counts(days)

    assert counts["complete"] == 1
    assert counts["current"] == 1
    assert counts["upcoming"] == 2
