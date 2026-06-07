from __future__ import annotations

from curriculum import LESSONS
from learning_path import (
    MILESTONES,
    completed_milestones_count,
    current_milestone_status,
    graduation_readiness,
    learning_outcomes,
    milestone_status,
    milestone_statuses,
    overall_learning_percent,
)
from progress import (
    add_mistake_card,
    default_progress,
    mark_lesson_complete,
    record_daily_mission,
    record_gym_session,
    record_project_milestone,
    record_prompt_score,
    record_quiz_score,
)


LESSON_IDS = [lesson.id for lesson in LESSONS]


def _complete_day(data, day: int, lesson_id: str = "01-python-mindset") -> None:
    record_daily_mission(data, day, status="Completed", mood="Good", reflection="proof")
    record_gym_session(
        data,
        day,
        pace="30 min daily",
        status="Saved",
        proof_note=f"Proof for day {day}",
        next_review="tiny review",
        minutes=30,
        lesson_id=lesson_id,
        step_state={"warmup": True, "lesson": True, "reps": True, "ai_prompt": True, "proof": True},
    )


def test_new_user_learning_path_has_clear_current_milestone():
    data = default_progress(LESSON_IDS, profile_name="New Learner")
    statuses = milestone_statuses(data)

    assert len(statuses) == 6
    assert completed_milestones_count(data) == 0
    assert overall_learning_percent(data) == 0.0
    assert current_milestone_status(data).milestone.id == "m1-python-start"
    assert current_milestone_status(data).next_action.startswith("Start Day 1")
    assert any("variables" in outcome.lower() for outcome in learning_outcomes())


def test_first_milestone_completes_with_lessons_days_quizzes_and_proofs():
    data = default_progress(LESSON_IDS, profile_name="Ava")
    first = MILESTONES[0]
    for lesson_id in first.lesson_ids:
        mark_lesson_complete(data, lesson_id)
        record_quiz_score(data, lesson_id, score=3, total=3)
    for day in range(first.day_range[0], first.day_range[1] + 1):
        _complete_day(data, day, lesson_id=first.lesson_ids[0])

    status = milestone_status(data, first)

    assert status.status == "Complete"
    assert status.percent == 1.0
    assert completed_milestones_count(data) == 1
    assert current_milestone_status(data).milestone.id == "m2-control-flow"


def test_milestone_progress_includes_project_checkpoints():
    data = default_progress(LESSON_IDS, profile_name="Ava")
    milestone = MILESTONES[1]
    for lesson_id in milestone.lesson_ids:
        mark_lesson_complete(data, lesson_id)
        record_quiz_score(data, lesson_id, score=2, total=3)
    for day in range(milestone.day_range[0], milestone.day_range[0] + 4):
        _complete_day(data, day, lesson_id=milestone.lesson_ids[0])

    before = milestone_status(data, milestone)
    assert before.status == "In progress"
    assert "Project checkpoints" in " ".join(before.evidence)

    record_project_milestone(data, "quiz_scorekeeper", "plan", status="Completed", note="planned")
    after = milestone_status(data, milestone)
    assert after.completed_requirements > before.completed_requirements


def test_graduation_readiness_moves_from_building_to_ready():
    data = default_progress(LESSON_IDS, profile_name="Ava")
    early = graduation_readiness(data, total_lessons=len(LESSONS))
    assert early.status == "Building"
    assert early.percent < 0.5

    for lesson_id in LESSON_IDS:
        mark_lesson_complete(data, lesson_id)
        record_quiz_score(data, lesson_id, score=3, total=3)
    for day in range(1, 31):
        _complete_day(data, day, lesson_id=LESSON_IDS[min(day - 1, len(LESSON_IDS) - 1)])
    for project_id, milestone_ids in {
        "quiz_scorekeeper": ("plan", "score", "feedback"),
        "habit_tracker_json": ("data", "add"),
        "prompt_coach": ("rubric", "detect"),
        "personal_ai_code_tutor": ("problem", "tiny_feature", "test"),
    }.items():
        for milestone_id in milestone_ids:
            record_project_milestone(data, project_id, milestone_id, status="Completed", note="done")
    for index in range(5):
        add_mistake_card(data, f"concept {index}", "mistake", "fix", lesson_id=LESSON_IDS[0])
    for _ in range(3):
        record_prompt_score(data, 8, "Help me debug this code with hints first.")

    ready = graduation_readiness(data, total_lessons=len(LESSONS))

    assert ready.status == "Ready to graduate"
    assert ready.percent == 1.0
    assert all(req.complete for req in ready.requirements)


def test_learning_path_exposes_graduation_promise_and_skill_map():
    from learning_path import GRADUATION_PROMISE, skill_statuses

    data = default_progress(LESSON_IDS, profile_name="Skill Map")
    statuses = skill_statuses(data)

    assert "variables" in GRADUATION_PROMISE
    assert "AI as a learning partner" in GRADUATION_PROMISE
    assert len(statuses) >= 10
    assert statuses[0].status == "Not started"
    assert statuses[0].next_lesson_id == "01-python-mindset"

    mark_lesson_complete(data, "01-python-mindset")
    updated = skill_statuses(data)
    assert updated[0].status == "Complete"
    assert updated[0].next_lesson_id is None
