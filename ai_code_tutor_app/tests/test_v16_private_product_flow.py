from __future__ import annotations

import json

import progress as progress_module
from coding_gym import gym_blocks_for_choice, gym_completion, workout_lesson_options, workout_resume_summary, workout_save_decision
from curriculum import LESSONS
from progress import (
    add_mistake_card,
    default_progress,
    load_progress,
    pause_gym_session,
    progress_path_for_profile,
    record_daily_mission,
    record_gym_session,
    save_focus_preferences,
    save_progress,
    start_gym_session,
)
from product_export import backup_zip_bytes, learning_transcript_markdown
from study_plan import DAILY_PLAN, next_mission


def test_private_learning_product_daily_loop_resume_and_export(tmp_path, monkeypatch):
    monkeypatch.setattr(progress_module, "DATA_DIR", tmp_path)
    lesson_ids = [lesson.id for lesson in LESSONS]
    data = default_progress(lesson_ids, profile_name="Daily Learner")
    save_focus_preferences(data, {"default_minutes": 10})

    mission = next_mission(data)
    options = workout_lesson_options(data, LESSONS, mission, 10, review_lesson_ids=[])
    selected_lesson_id = options[0].lesson_id
    blocks = gym_blocks_for_choice("10 min rescue")
    start_gym_session(data, mission.day, "10 min rescue", minutes=10, lesson_id=selected_lesson_id)
    pause_gym_session(
        data,
        mission.day,
        "10 min rescue",
        minutes=10,
        lesson_id=selected_lesson_id,
        step_state={blocks[0].id: True},
        proof_note="I started and will finish later.",
        next_review="variables vs strings",
    )
    path = tmp_path / "progress_daily-learner.json"
    save_progress(data, path)

    loaded = load_progress(lesson_ids, path, profile_name="Daily Learner")
    summary = workout_resume_summary(loaded, mission.day)
    assert summary is not None
    assert summary.pace == "10 min rescue"
    assert summary.lesson_id == selected_lesson_id
    assert "I started" in summary.proof_preview
    assert summary.checked_blocks == 1

    current_state = {block.id: True for block in blocks}
    decision = workout_save_decision(gym_completion(current_state, blocks), "I finished one rescue rep.", "Completed")
    assert decision.ok is True
    record_gym_session(
        loaded,
        mission.day,
        pace="10 min rescue",
        status=decision.gym_status,
        proof_note="I finished one rescue rep.",
        next_review="variables vs strings",
        minutes=10,
        lesson_id=selected_lesson_id,
        step_state=current_state,
    )
    record_daily_mission(loaded, mission.day, status=decision.mission_status, mood="Good", reflection="I finished one rescue rep.")
    add_mistake_card(loaded, "variables", "I mixed up strings and numbers", "Use quotes for strings", lesson_id=selected_lesson_id)
    save_progress(loaded, path)

    reloaded = load_progress(lesson_ids, path, profile_name="Daily Learner")
    assert reloaded["gym_sessions"][str(mission.day)]["status"] == "Saved"
    assert reloaded["daily_missions"][str(mission.day)]["status"] == "Completed"
    assert reloaded["focus_preferences"]["default_minutes"] == 10
    assert reloaded["mistake_cards"][0]["concept"] == "variables"

    transcript = learning_transcript_markdown("Daily Learner", reloaded, LESSONS, DAILY_PLAN)
    assert "I finished one rescue rep" in transcript
    assert backup_zip_bytes("Daily Learner", "daily-learner", reloaded, LESSONS, DAILY_PLAN)
