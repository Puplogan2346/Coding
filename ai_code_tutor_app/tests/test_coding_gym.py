from __future__ import annotations

from coding_gym import (
    build_review_items,
    gym_blocks_for_choice,
    gym_completion,
    gym_history_summary,
    gym_motivation_copy,
    gym_progress_label,
    gym_session_history,
    next_gym_action,
    proof_card_summary,
    total_gym_minutes,
    workout_finish_status,
    workout_lesson_options,
    workout_resume_setup,
    workout_resume_summary,
    workout_save_decision,
)
from curriculum import LESSONS
from progress import (
    add_mistake_card,
    default_progress,
    gym_session_for_day,
    gym_session_is_active,
    pause_gym_session,
    record_gym_session,
    record_quiz_score,
    load_progress,
    sanitize_focus_preferences,
    save_focus_preferences,
    save_progress,
    start_gym_session,
)
from study_plan import mission_by_day


def test_gym_blocks_match_session_lengths():
    rescue = gym_blocks_for_choice("10 min rescue")
    daily = gym_blocks_for_choice("30 min daily")
    deep = gym_blocks_for_choice("45 min deep dive")

    assert total_gym_minutes(rescue) == 10
    assert total_gym_minutes(daily) == 30
    assert total_gym_minutes(deep) == 45
    assert [block.id for block in daily] == ["warmup", "lesson", "reps", "ai_prompt", "proof"]


def test_gym_completion_and_next_action():
    blocks = gym_blocks_for_choice("30 min daily")
    state = {"warmup": True, "lesson": True}

    assert gym_completion(state, blocks) == 0.4
    assert gym_progress_label(state, blocks) == "2 of 5 blocks"
    action = next_gym_action("Loops", state, blocks)
    assert action.headline == "Next rep: Coding reps"
    assert action.stage == "workout"

    complete_state = {block.id: True for block in blocks}
    assert next_gym_action("Loops", complete_state, blocks).stage == "proof"
    assert next_gym_action("Loops", complete_state, blocks, session_saved=True).stage == "done"


def test_gym_motivation_and_finish_status():
    assert "Rescue mode counts" in gym_motivation_copy(0, "10 min rescue")
    assert workout_finish_status(0.5, "") == ("In workout", "Finish the next block or switch to rescue mode.")
    assert workout_finish_status(1.0, "") == ("Needs proof", "Write one sentence proof to close the session.")
    assert workout_finish_status(1.0, "I learned return") == ("Ready to save", "Save the proof card and stop.")
    assert workout_finish_status(1.0, "I learned return", session_saved=True)[0] == "Saved"


def test_build_review_items_from_quiz_and_mistake_cards():
    data = default_progress(["one", "two"], profile_name="Ava")
    record_quiz_score(data, "one", score=1, total=3)
    assert add_mistake_card(data, "colon syntax", "forgot colon", "if x:", lesson_id="two")

    items = build_review_items(data, ["one", "two"], max_items=5)
    assert items[0].lesson_id == "one"
    assert items[0].intensity == "shaky"
    assert any(item.reason.startswith("Mistake card") for item in items)


def test_proof_card_summary_and_progress_schema():
    card = proof_card_summary(1, "Start Python", "I learned print", "Review strings")
    assert card.title == "Day 1 proof: Start Python"
    assert card.summary == "I learned print"
    assert card.next_review == "Review strings"

    data = default_progress(["one"], profile_name="Ava")
    record_gym_session(
        data,
        1,
        pace="30 min daily",
        status="Saved",
        proof_note="I wrote a function",
        next_review="return values",
        minutes=30,
        lesson_id="one",
        step_state={"warmup": True},
    )
    assert data["gym_sessions"]["1"]["status"] == "Saved"
    assert data["gym_sessions"]["1"]["step_state"] == {"warmup": True}


def test_workout_save_decision_blocks_accidental_empty_completion():
    incomplete = workout_save_decision(0.4, "I learned print", "Completed")
    assert not incomplete.ok
    assert incomplete.gym_status == "In workout"
    assert "Finish each visible block" in incomplete.message

    empty_proof = workout_save_decision(1.0, "", "Completed")
    assert not empty_proof.ok
    assert empty_proof.gym_status == "Needs proof"

    parked = workout_save_decision(0.2, "", "In progress")
    assert parked.ok
    assert parked.gym_status == "In workout"
    assert parked.mission_status == "In progress"

    complete = workout_save_decision(1.0, "I learned return", "Completed")
    assert complete.ok
    assert complete.gym_status == "Saved"
    assert complete.mission_status == "Completed"


def test_started_gym_session_survives_refresh_and_preserves_created_at():
    data = default_progress(["one"], profile_name="Ava")
    start_gym_session(data, 1, pace="30 min daily", minutes=30, lesson_id="one", step_state={"warmup": False})
    first = gym_session_for_day(data, 1)
    assert gym_session_is_active(data, 1)
    assert first["status"] == "In workout"
    assert first["step_state"] == {"warmup": False}

    record_gym_session(data, 1, pace="30 min daily", status="Saved", proof_note="proof", minutes="bad", lesson_id="one", step_state={"warmup": True})
    saved = gym_session_for_day(data, 1)
    assert saved["created_at"] == first["created_at"]
    assert saved["minutes"] == 0
    assert saved["status"] == "Saved"


def test_gym_history_and_proof_review_items():
    data = default_progress(["one"], profile_name="Ava")
    record_gym_session(
        data,
        2,
        pace="10 min rescue",
        status="In workout",
        proof_note="Started loops",
        next_review="loop syntax",
        minutes=10,
        lesson_id="one",
        step_state={"open": True},
    )
    record_gym_session(
        data,
        1,
        pace="30 min daily",
        status="Saved",
        proof_note="I wrote print",
        next_review="print vs return",
        minutes=30,
        lesson_id="one",
        step_state={"warmup": True},
    )
    history = gym_session_history(data, limit=2)
    assert [item.day for item in history] == [2, 1]
    assert "1 saved" in gym_history_summary(data)
    assert "1 parked" in gym_history_summary(data)

    review_items = build_review_items(data, ["one"], max_items=5)
    assert any("Proof card review" in item.reason for item in review_items)


def test_workout_lesson_options_change_with_time_available():
    lesson_ids = [lesson.id for lesson in LESSONS]
    data = default_progress(lesson_ids, profile_name="Ava")
    data["completed_lessons"] = ["01-python-mindset", "02-variables-types"]
    mission = mission_by_day(5)

    rescue = workout_lesson_options(
        data,
        LESSONS,
        mission,
        10,
        review_lesson_ids=["02-variables-types"],
    )
    daily = workout_lesson_options(data, LESSONS, mission, 30, review_lesson_ids=["02-variables-types"])
    deep = workout_lesson_options(data, LESSONS, mission, 45, review_lesson_ids=["02-variables-types"])

    assert rescue[0].lesson_id == "02-variables-types"
    assert "10 min rescue" in rescue[0].reason
    assert daily[0].lesson_id == mission.lesson_id
    assert daily[0].reason == "today’s plan"
    assert deep[0].lesson_id == mission.lesson_id
    assert any(option.reason == "deep-dive stretch" for option in deep)


def test_workout_lesson_options_prioritize_saved_resume_lesson():
    lesson_ids = [lesson.id for lesson in LESSONS]
    data = default_progress(lesson_ids, profile_name="Ava")
    mission = mission_by_day(1)

    options = workout_lesson_options(
        data,
        LESSONS,
        mission,
        30,
        current_lesson_id="04-loops",
    )

    assert options[0].lesson_id == "04-loops"
    assert options[0].reason == "resume saved workout"


def test_preferred_workout_minutes_and_paused_session_resume_metadata():
    data = default_progress(["one", "two"], profile_name="Ava")
    save_focus_preferences(data, {"default_minutes": 10})
    assert data["focus_preferences"]["default_minutes"] == 10

    start_gym_session(data, 1, pace="10 min rescue", minutes=10, lesson_id="two", step_state={"open": True})
    pause_gym_session(
        data,
        1,
        pace="10 min rescue",
        proof_note="I started but need to pause",
        next_review="print syntax",
        minutes=10,
        lesson_id="two",
        step_state={"open": True, "tiny_rep": False},
    )

    saved = gym_session_for_day(data, 1)
    assert saved["status"] == "In workout"
    assert saved["pace"] == "10 min rescue"
    assert saved["minutes"] == 10
    assert saved["lesson_id"] == "two"
    assert saved["proof_note"] == "I started but need to pause"
    assert saved["step_state"] == {"open": True, "tiny_rep": False}
    assert gym_session_is_active(data, 1)
    assert data["daily_missions"]["1"]["status"] == "In progress"
    assert data["daily_checklists"]["1"]["steps"] == {"open": True, "tiny_rep": False}


def test_paused_session_roundtrip_after_reload_keeps_preference_and_lesson(tmp_path):
    lesson_ids = [lesson.id for lesson in LESSONS]
    path = tmp_path / "progress_resume.json"
    data = default_progress(lesson_ids, profile_name="Ava")
    save_focus_preferences(data, {"default_minutes": 45})
    mission = mission_by_day(8)

    pause_gym_session(
        data,
        mission.day,
        pace="45 min deep dive",
        proof_note="I paused after the warm-up",
        next_review="function parameters",
        minutes=45,
        lesson_id="05-functions",
        step_state={"warmup": True, "lesson": False},
    )
    save_progress(data, path)

    reloaded = load_progress(lesson_ids, path, profile_name="Ava")
    saved = gym_session_for_day(reloaded, mission.day)
    assert reloaded["focus_preferences"]["default_minutes"] == 45
    assert saved["status"] == "In workout"
    assert saved["pace"] == "45 min deep dive"
    assert saved["lesson_id"] == "05-functions"
    assert saved["step_state"] == {"warmup": True, "lesson": False}

    options = workout_lesson_options(
        reloaded,
        LESSONS,
        mission,
        45,
        review_lesson_ids=["03-conditionals"],
        current_lesson_id=saved["lesson_id"],
    )
    assert options[0].lesson_id == "05-functions"
    assert options[0].reason == "resume saved workout"


def test_resume_summary_makes_paused_workout_obvious():
    data = default_progress(["one", "two"], profile_name="Ava")
    pause_gym_session(
        data,
        3,
        pace="10 min rescue",
        minutes=10,
        lesson_id="two",
        step_state={"open": True, "tiny_rep": False, "proof": False},
        proof_note="I had to stop after reading variables.",
        next_review="string vs int",
    )

    summary = workout_resume_summary(data, 3)
    assert summary is not None
    assert summary.headline == "Resume where you stopped: 1/3 blocks done"
    assert summary.pace == "10 min rescue"
    assert summary.minutes == 10
    assert summary.lesson_id == "two"
    assert summary.checked_blocks == 1
    assert summary.total_blocks == 3
    assert summary.completion == 0.333
    assert "variables" in summary.proof_preview
    assert summary.next_review == "string vs int"


def test_resume_summary_only_shows_active_not_saved_sessions():
    data = default_progress(["one"], profile_name="Ava")
    record_gym_session(
        data,
        1,
        pace="30 min daily",
        status="Saved",
        proof_note="Done",
        minutes=30,
        lesson_id="one",
        step_state={"warmup": True, "lesson": True, "reps": True, "ai_prompt": True, "proof": True},
    )
    assert workout_resume_summary(data, 1) is None


def test_focus_preference_sanitizes_all_supported_lengths():
    clean = sanitize_focus_preferences({"default_minutes": 10})
    assert clean["default_minutes"] == 10
    clean = sanitize_focus_preferences({"default_minutes": 30})
    assert clean["default_minutes"] == 30
    clean = sanitize_focus_preferences({"default_minutes": 45})
    assert clean["default_minutes"] == 45
    assert sanitize_focus_preferences({"default_minutes": "bad"})["default_minutes"] == 30
    assert sanitize_focus_preferences({"default_minutes": 41})["default_minutes"] == 45


def test_time_choice_can_change_before_start_without_creating_session():
    lesson_ids = [lesson.id for lesson in LESSONS]
    data = default_progress(lesson_ids, profile_name="Ava")
    data["completed_lessons"] = ["01-python-mindset", "02-variables-types"]
    mission = mission_by_day(4)

    ten_min = workout_lesson_options(data, LESSONS, mission, 10, review_lesson_ids=["02-variables-types"])
    forty_five = workout_lesson_options(data, LESSONS, mission, 45, review_lesson_ids=["02-variables-types"])

    assert ten_min[0].lesson_id == "02-variables-types"
    assert ten_min[0].reason == "10 min rescue review"
    assert forty_five[0].lesson_id == mission.lesson_id
    assert forty_five[0].reason == "today’s full lesson"
    assert data["gym_sessions"] == {}


def test_resume_setup_uses_preferred_minutes_when_no_started_workout():
    data = default_progress([lesson.id for lesson in LESSONS], profile_name="Ava")
    save_focus_preferences(data, {"default_minutes": 45})

    setup = workout_resume_setup({}, data["focus_preferences"]["default_minutes"], [lesson.id for lesson in LESSONS])

    assert setup.locked is False
    assert setup.pace_label == "45 min deep dive"
    assert setup.minutes == 45
    assert setup.lesson_id is None
    assert setup.source == "preference"


def test_resume_setup_recovers_started_workout_from_saved_minutes_when_pace_is_old_or_bad():
    data = default_progress([lesson.id for lesson in LESSONS], profile_name="Ava")
    data["gym_sessions"]["4"] = {
        "status": "In workout",
        "pace": "old custom label",
        "minutes": 10,
        "lesson_id": "02-variables-types",
        "step_state": {"open": True},
    }

    setup = workout_resume_setup(data["gym_sessions"]["4"], 30, [lesson.id for lesson in LESSONS])

    assert setup.locked is True
    assert setup.pace_label == "10 min rescue"
    assert setup.minutes == 10
    assert setup.lesson_id == "02-variables-types"
    assert setup.source == "saved_minutes"


def test_stop_save_roundtrip_resumes_same_length_lesson_steps_and_drafts(tmp_path):
    lesson_ids = [lesson.id for lesson in LESSONS]
    path = tmp_path / "progress_stop_resume.json"
    data = default_progress(lesson_ids, profile_name="Ava")
    save_focus_preferences(data, {"default_minutes": 10})
    mission = mission_by_day(5)

    start_gym_session(
        data,
        mission.day,
        pace="10 min rescue",
        minutes=10,
        lesson_id="02-variables-types",
        step_state={"open": True, "tiny_rep": False, "proof": False},
    )
    pause_gym_session(
        data,
        mission.day,
        pace="10 min rescue",
        minutes=10,
        lesson_id="02-variables-types",
        step_state={"open": True, "tiny_rep": True, "proof": False},
        proof_note="I stopped after practicing variables.",
        next_review="string vs int",
    )
    save_progress(data, path)

    reloaded = load_progress(lesson_ids, path, profile_name="Ava")
    saved = gym_session_for_day(reloaded, mission.day)
    setup = workout_resume_setup(saved, reloaded["focus_preferences"]["default_minutes"], lesson_ids)
    summary = workout_resume_summary(reloaded, mission.day)

    assert setup.locked is True
    assert setup.pace_label == "10 min rescue"
    assert setup.lesson_id == "02-variables-types"
    assert saved["proof_note"] == "I stopped after practicing variables."
    assert saved["next_review"] == "string vs int"
    assert saved["step_state"] == {"open": True, "tiny_rep": True, "proof": False}
    assert reloaded["focus_preferences"]["default_minutes"] == 10
    assert summary is not None
    assert summary.checked_blocks == 2
    assert summary.total_blocks == 3
    assert "variables" in summary.proof_preview


def test_workout_resume_summary_recovers_bad_old_pace_from_minutes():
    data = default_progress(["one"], profile_name="Ava")
    data["gym_sessions"]["1"] = {
        "status": "In workout",
        "pace": "bad old label",
        "minutes": 10,
        "lesson_id": "one",
        "step_state": {"open": True},
        "proof_note": "I paused.",
    }

    summary = workout_resume_summary(data, 1)

    assert summary is not None
    assert summary.pace == "10 min rescue"
    assert summary.minutes == 10
    assert summary.checked_blocks == 1
    assert summary.total_blocks == 3


def test_v14_resume_setup_locks_saved_time_and_lesson_even_if_default_changes():
    lesson_ids = [lesson.id for lesson in LESSONS]
    data = default_progress(lesson_ids, profile_name="Ava")
    mission = mission_by_day(4)

    pause_gym_session(
        data,
        mission.day,
        pace="10 min rescue",
        minutes=10,
        lesson_id="02-variables-types",
        step_state={"open": True, "tiny_rep": False, "proof": False},
        proof_note="Paused after one variable review.",
        next_review="string vs int",
    )
    save_focus_preferences(data, {"default_minutes": 45})

    setup = workout_resume_setup(gym_session_for_day(data, mission.day), data["focus_preferences"]["default_minutes"], lesson_ids)

    assert setup.locked is True
    assert setup.pace_label == "10 min rescue"
    assert setup.minutes == 10
    assert setup.lesson_id == "02-variables-types"
    assert setup.source == "saved_pace"

    options = workout_lesson_options(
        data,
        LESSONS,
        mission,
        setup.minutes,
        current_lesson_id=setup.lesson_id,
    )
    assert options[0].lesson_id == "02-variables-types"
    assert options[0].reason == "resume saved workout"


def test_v14_resume_setup_uses_preferred_minutes_when_no_workout_started():
    lesson_ids = [lesson.id for lesson in LESSONS]
    data = default_progress(lesson_ids, profile_name="Ava")
    save_focus_preferences(data, {"default_minutes": 45})

    setup = workout_resume_setup({}, data["focus_preferences"]["default_minutes"], lesson_ids)

    assert setup.locked is False
    assert setup.pace_label == "45 min deep dive"
    assert setup.minutes == 45
    assert setup.lesson_id is None
    assert setup.source == "preference"


def test_v14_resume_setup_recovers_old_sessions_with_missing_pace_from_minutes():
    lesson_ids = [lesson.id for lesson in LESSONS]
    setup = workout_resume_setup(
        {"status": "In workout", "minutes": 30, "lesson_id": "03-conditionals"},
        preferred_minutes=10,
        valid_lesson_ids=lesson_ids,
    )

    assert setup.locked is True
    assert setup.pace_label == "30 min daily"
    assert setup.minutes == 30
    assert setup.lesson_id == "03-conditionals"
    assert setup.source == "saved_minutes"
