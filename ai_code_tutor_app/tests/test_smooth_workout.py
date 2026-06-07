from coding_gym import DAILY_BLOCKS, RESCUE_BLOCKS
from smooth_workout import (
    clean_step_state,
    current_focus_card,
    daily_use_smoothness_checks,
    focus_completion_sentence,
    mark_focus_step_done,
    resume_safety_report,
)


def test_current_focus_card_starts_with_first_unchecked_block():
    card = current_focus_card({}, DAILY_BLOCKS)
    assert card.block_id == "warmup"
    assert card.step_number == 1
    assert card.total_steps == len(DAILY_BLOCKS)
    assert "Step 1" in card.headline
    assert "Do only this rep" in card.nudge


def test_focus_card_advances_after_marking_current_step_done():
    state = mark_focus_step_done({}, DAILY_BLOCKS)
    assert state["warmup"] is True
    next_card = current_focus_card(state, DAILY_BLOCKS)
    assert next_card.block_id == "lesson"
    assert next_card.step_number == 2
    assert focus_completion_sentence(next_card).startswith("1 of")


def test_focus_card_moves_to_proof_after_all_steps_checked():
    state = {block.id: True for block in RESCUE_BLOCKS}
    card = current_focus_card(state, RESCUE_BLOCKS)
    assert card.is_complete is True
    assert card.completion == 1.0
    assert "save proof" in card.headline.lower()


def test_clean_step_state_drops_steps_from_other_workout_lengths():
    state = {"warmup": True, "project_reps": True, "not_real": True}
    cleaned = clean_step_state(state, DAILY_BLOCKS)
    assert cleaned == {"warmup": True}


def test_resume_safety_report_confirms_saved_in_progress_state():
    session = {
        "status": "In workout",
        "pace": "30 min daily",
        "lesson_id": "01-python-mindset",
        "proof_note": "I learned print basics.",
        "step_state": {"warmup": True},
    }
    report = resume_safety_report(session, DAILY_BLOCKS)
    assert report.can_resume is True
    assert report.saved_pace == "30 min daily"
    assert report.saved_lesson_id == "01-python-mindset"
    assert report.saved_blocks == 1
    assert report.proof_saved is True


def test_daily_use_smoothness_checks_cover_default_resume_focus_and_proof():
    progress = {
        "focus_preferences": {"default_minutes": 10},
        "gym_sessions": {
            "1": {
                "status": "In workout",
                "pace": "10 min rescue",
                "lesson_id": "01-python-mindset",
                "step_state": {"open": True},
            }
        },
    }
    checks = daily_use_smoothness_checks(progress, 1, RESCUE_BLOCKS, preferred_minutes=30)
    assert [check.name for check in checks] == [
        "Default workout length",
        "Stop/resume state",
        "One-step focus mode",
        "Proof habit",
    ]
    assert all(check.status in {"Pass", "Warning"} for check in checks)
    assert checks[0].status == "Pass"
    assert checks[1].status == "Pass"
