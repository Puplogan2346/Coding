from daily_coach import daily_session_checklist
from experience import (
    SESSION_LABELS,
    daily_timeline,
    effective_energy_for_session,
    mission_is_complete,
    mission_stage_cards,
    next_action_card,
    percent_label,
    plan_progress_sentence,
    session_choice_by_label,
    session_index_for_minutes,
    session_label_for_minutes,
    session_minutes_total,
    streak_microcopy,
    today_progress_label,
)
from progress import default_progress, record_daily_checklist, record_daily_mission
from study_plan import mission_by_day


def test_session_choices_support_rescue_daily_and_deep_dive():
    assert SESSION_LABELS == ("10 min rescue", "30 min daily", "45 min deep dive")
    assert session_choice_by_label("10 min rescue").minutes == 10
    assert session_choice_by_label("missing").label == "30 min daily"
    assert effective_energy_for_session("10 min rescue", "High") == "Low"
    assert effective_energy_for_session("30 min daily", "high") == "High"


def test_next_action_card_moves_from_step_to_mission_to_done():
    mission = mission_by_day(1)
    steps = daily_session_checklist(mission, "Medium")
    action = next_action_card(mission.title, {}, steps)
    assert action.headline.startswith("Do this now")
    assert "one job" in action.proof.lower()

    saved = {step.id: True for step in steps}
    action = next_action_card(mission.title, saved, steps)
    assert "Save the mission" in action.headline

    action = next_action_card(mission.title, saved, steps, mission_is_complete=True)
    assert "done" in action.headline.lower()


def test_timeline_and_copy_are_new_user_friendly():
    progress = default_progress(["01-python-mindset"], profile_name="Ava")
    timeline = daily_timeline(progress, total_days=3)
    assert [day.status for day in timeline] == ["current", "upcoming", "upcoming"]
    assert plan_progress_sentence(progress) == "0 done, 30 left in the 30-day plan."
    assert "No streak" in streak_microcopy(0, 0)

    record_daily_mission(progress, 1, status="Completed")
    record_daily_mission(progress, 2, status="Skipped")
    timeline = daily_timeline(progress, total_days=3)
    assert [day.status for day in timeline] == ["complete", "skipped", "current"]
    assert mission_is_complete(progress, 1) is True


def test_progress_labels_and_stage_cards():
    mission = mission_by_day(1)
    steps = daily_session_checklist(mission, "Medium")
    progress = default_progress(["01-python-mindset"], profile_name="Ava")
    record_daily_checklist(progress, 1, {"open": True})
    saved = {"open": True}

    assert today_progress_label(saved, steps) == "1 of 6 steps"
    assert percent_label(0.334) == "33%"
    assert percent_label(9) == "100%"
    assert session_minutes_total(steps) == 30

    cards = mission_stage_cards(mission, saved, steps)
    assert [card[0] for card in cards] == ["Now", "Then", "Proof"]
    assert "Park" in cards[0][1] or "park" in cards[0][1]


def test_session_label_for_minutes_prefers_nearest_daily_pace():
    assert session_label_for_minutes(10) == "10 min rescue"
    assert session_label_for_minutes("30") == "30 min daily"
    assert session_label_for_minutes(44) == "45 min deep dive"
    assert session_label_for_minutes("not a number") == "30 min daily"
    assert session_index_for_minutes(45) == 2
