from pathlib import Path

from code_runner import run_python_with_tests
from curriculum import LESSONS
from focus_coach import focus_blocks, total_focus_minutes
from official_ai_resources import official_resource_stats
from projects import completed_project_milestones_count, recommended_project_id
from progress import (
    completion_percent,
    lessons_remaining,
    load_progress,
    record_focus_checkin,
    mark_lesson_complete,
    record_official_ai_resource,
    record_project_milestone,
    record_prompt_score,
    record_quiz_score,
    save_note,
    save_progress,
)
from prompt_lab import improved_prompt_template, score_prompt


def test_new_user_can_complete_first_learning_loop(tmp_path: Path):
    """Smoke-test the path a brand-new learner should experience first."""
    lesson_ids = [lesson.id for lesson in LESSONS]
    first_lesson = LESSONS[0]
    progress_path = tmp_path / "progress_new_user.json"

    progress = load_progress(lesson_ids, progress_path, profile_name="New User")

    assert progress["profile_name"] == "New User"
    assert progress["completed_lessons"] == []
    assert len(progress["notes"]) == len(LESSONS)
    assert completion_percent(progress, len(LESSONS)) == 0.0
    assert lessons_remaining(progress, len(LESSONS)) == len(LESSONS)
    assert official_resource_stats(progress)["started"] == 0
    assert total_focus_minutes(focus_blocks(30, "Medium")) == 30
    assert recommended_project_id(progress) == "quiz_scorekeeper"

    mark_lesson_complete(progress, first_lesson.id)
    record_quiz_score(progress, first_lesson.id, len(first_lesson.quiz), len(first_lesson.quiz))
    save_note(progress, first_lesson.id, "Errors are feedback. Read the line number first.")

    code_result = run_python_with_tests(first_lesson.challenge.sample_solution, first_lesson.challenge.tests)
    assert code_result.ok, code_result.stderr

    prompt = improved_prompt_template(first_lesson.title)
    prompt_score = score_prompt(prompt)
    record_prompt_score(progress, prompt_score.score, prompt)
    record_official_ai_resource(progress, "gumloop_university", "Queued", "Try after lesson 3")
    record_focus_checkin(progress, "Medium", "Warming up", "new app", "finished first loop")
    record_project_milestone(progress, "quiz_scorekeeper", "plan", "Completed", "planned inputs and outputs")
    save_progress(progress, progress_path)

    reloaded = load_progress(lesson_ids, progress_path, profile_name="New User")
    assert reloaded["completed_lessons"] == [first_lesson.id]
    assert reloaded["quiz_scores"][first_lesson.id]["percent"] == 100.0
    assert reloaded["notes"][first_lesson.id].startswith("Errors are feedback")
    assert reloaded["prompt_scores"][0]["score"] >= 8
    assert reloaded["official_ai_status"]["gumloop_university"] == "Queued"
    assert official_resource_stats(reloaded)["started"] == 1
    assert reloaded["focus_checkins"][0]["win"] == "finished first loop"
    assert completed_project_milestones_count(reloaded) == 1
    assert completion_percent(reloaded, len(LESSONS)) == 0.083
    assert lessons_remaining(reloaded, len(LESSONS)) == len(LESSONS) - 1
