from curriculum import LESSONS
from progress import (
    default_progress,
    mark_lesson_complete,
    normalize_progress_data,
    record_quiz_score,
    record_review_result,
)
from review import (
    build_review_quiz,
    lessons_to_review,
    needs_review,
    next_lesson_to_study,
    quiz_percent,
)

LESSON_IDS = [lesson.id for lesson in LESSONS]


def _fresh():
    return default_progress(LESSON_IDS, profile_name="Reviewer")


def test_new_user_has_no_review_quiz():
    data = _fresh()
    assert build_review_quiz(data) == []
    assert lessons_to_review(data) == []


def test_review_result_persists_through_normalize():
    data = _fresh()
    record_review_result(data, 4, 5)
    restored = normalize_progress_data(data, LESSON_IDS)
    assert restored["review_history"][-1]["score"] == 4
    assert restored["review_history"][-1]["percent"] == 80.0


def test_next_lesson_to_study_is_first_incomplete():
    data = _fresh()
    assert next_lesson_to_study(data).id == LESSONS[0].id
    mark_lesson_complete(data, LESSONS[0].id)
    assert next_lesson_to_study(data).id == LESSONS[1].id


def test_completed_without_passing_quiz_needs_review():
    data = _fresh()
    mark_lesson_complete(data, "01-python-mindset")
    assert needs_review(data, "01-python-mindset") is True  # completed, no quiz
    record_quiz_score(data, "01-python-mindset", 3, 3)  # 100%
    assert needs_review(data, "01-python-mindset") is False
    assert quiz_percent(data, "01-python-mindset") == 100.0


def test_incomplete_lesson_never_needs_review():
    data = _fresh()
    assert needs_review(data, "02-variables-types") is False


def test_review_quiz_prioritizes_weak_lessons_and_caps_length():
    data = _fresh()
    # Complete three lessons; lesson 2 weak, lesson 1 strong, lesson 3 unquizzed.
    for lesson_id in ("01-python-mindset", "02-variables-types", "03-conditionals"):
        mark_lesson_complete(data, lesson_id)
    record_quiz_score(data, "01-python-mindset", 3, 3)   # 100%
    record_quiz_score(data, "02-variables-types", 1, 3)  # 33%

    review = lessons_to_review(data)
    review_ids = [lesson.id for lesson in review]
    # Weak (33%) and unquizzed lessons need review; the strong 100% one does not.
    assert "02-variables-types" in review_ids
    assert "03-conditionals" in review_ids
    assert "01-python-mindset" not in review_ids

    quiz = build_review_quiz(data, max_questions=2)
    assert len(quiz) == 2
    # No lesson appears twice.
    assert len({lesson.id for lesson, _ in quiz}) == 2
