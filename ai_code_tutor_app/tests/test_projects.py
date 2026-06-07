from projects import (
    PROJECTS,
    completed_project_milestones_count,
    next_project_milestone,
    project_by_id,
    project_completion_percent,
    recommended_project_id,
)
from progress import default_progress, mark_lesson_complete, record_project_milestone


def test_project_catalog_has_capstone_and_tiny_milestones():
    assert len(PROJECTS) >= 5
    assert project_by_id("personal_ai_code_tutor").level == "Capstone"
    for project in PROJECTS:
        assert len(project.milestones) == 5
        assert project.minutes <= 180
        assert project.description
        assert all(milestone.proof for milestone in project.milestones)


def test_project_progress_and_next_milestone():
    data = default_progress(["one"], profile_name="Ava")
    project = project_by_id("quiz_scorekeeper")
    assert project_completion_percent(data, project.id) == 0.0
    assert next_project_milestone(data, project.id).id == "plan"

    record_project_milestone(data, project.id, "plan", "Completed", "I wrote inputs and outputs.")
    assert completed_project_milestones_count(data) == 1
    assert project_completion_percent(data, project.id) == 0.2
    assert next_project_milestone(data, project.id).id == "score"


def test_recommended_project_moves_with_lessons():
    lesson_ids = [f"lesson-{index}" for index in range(12)]
    data = default_progress(lesson_ids, profile_name="Ava")
    assert recommended_project_id(data) == "quiz_scorekeeper"

    for lesson_id in lesson_ids[:4]:
        mark_lesson_complete(data, lesson_id)
    assert recommended_project_id(data) == "habit_tracker_json"

    for lesson_id in lesson_ids[4:7]:
        mark_lesson_complete(data, lesson_id)
    assert recommended_project_id(data) == "prompt_coach"

    for lesson_id in lesson_ids[7:10]:
        mark_lesson_complete(data, lesson_id)
    assert recommended_project_id(data) == "personal_ai_code_tutor"
