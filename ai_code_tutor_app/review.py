"""Progress-based review logic.

Pure functions (no Streamlit) that decide what a learner should study or review
next, and that assemble a mixed review quiz drawn from the lessons they have
already completed — weakest first. The Review section in the Practice tab renders
these.
"""
from __future__ import annotations

from typing import List, Optional, Tuple

from curriculum import LESSONS, Lesson, QuizQuestion
from learning_path import first_incomplete_lesson_id

# A lesson "passes" once its quiz is at or above this percent.
REVIEW_THRESHOLD = 70.0


def quiz_percent(progress_data: dict, lesson_id: str) -> Optional[float]:
    """The saved quiz percent for a lesson, or None if it was never quizzed."""
    score = (progress_data.get("quiz_scores", {}) or {}).get(lesson_id)
    if not isinstance(score, dict):
        return None
    try:
        return float(score.get("percent"))
    except (TypeError, ValueError):
        return None


def needs_review(progress_data: dict, lesson_id: str) -> bool:
    """True for a completed lesson whose quiz has not been passed (none or < 70%)."""
    completed = set(progress_data.get("completed_lessons", []) or [])
    if lesson_id not in completed:
        return False
    percent = quiz_percent(progress_data, lesson_id)
    return percent is None or percent < REVIEW_THRESHOLD


def _review_priority(progress_data: dict, lesson_id: str) -> float:
    """Lower = more urgent. Unquizzed completed lessons sort to the very front."""
    percent = quiz_percent(progress_data, lesson_id)
    return percent if percent is not None else -1.0


def lessons_to_review(progress_data: dict, lessons: List[Lesson] = LESSONS) -> List[Lesson]:
    """Completed lessons still needing a quiz pass, weakest (and unquizzed) first."""
    items = [lesson for lesson in lessons if needs_review(progress_data, lesson.id)]
    return sorted(items, key=lambda lesson: _review_priority(progress_data, lesson.id))


def next_lesson_to_study(progress_data: dict, lessons: List[Lesson] = LESSONS) -> Lesson:
    """The first lesson the learner has not completed (falls back to the last)."""
    target = first_incomplete_lesson_id(progress_data)
    return next((lesson for lesson in lessons if lesson.id == target), lessons[-1])


def review_pool(progress_data: dict, lessons: List[Lesson] = LESSONS) -> List[Lesson]:
    """Completed lessons to draw review questions from: weak/unquizzed first."""
    completed = set(progress_data.get("completed_lessons", []) or [])
    weak = lessons_to_review(progress_data, lessons)
    weak_ids = {lesson.id for lesson in weak}
    other_completed = [lesson for lesson in lessons if lesson.id in completed and lesson.id not in weak_ids]
    return weak + other_completed


def build_review_quiz(
    progress_data: dict,
    lessons: List[Lesson] = LESSONS,
    max_questions: int = 5,
) -> List[Tuple[Lesson, QuizQuestion]]:
    """One quiz question from each completed lesson (weakest first), up to a cap.

    Returns an empty list when nothing has been completed yet, so the UI can
    invite the learner to finish a lesson before reviewing.
    """
    quiz: List[Tuple[Lesson, QuizQuestion]] = []
    for lesson in review_pool(progress_data, lessons):
        if lesson.quiz:
            quiz.append((lesson, lesson.quiz[0]))
            if len(quiz) >= max_questions:
                break
    return quiz
