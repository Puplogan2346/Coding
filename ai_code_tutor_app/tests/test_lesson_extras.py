from curriculum import LESSONS
from lesson_extras import common_mistake, worked_example


def test_every_lesson_has_a_worked_example():
    missing = [lesson.id for lesson in LESSONS if not worked_example(lesson.id).strip()]
    assert not missing, f"Lessons missing a worked example: {missing}"


def test_every_lesson_has_a_common_mistake():
    missing = [lesson.id for lesson in LESSONS if not common_mistake(lesson.id).strip()]
    assert not missing, f"Lessons missing a common-mistake note: {missing}"


def test_worked_examples_show_code():
    # Most worked examples teach with a code block; ensure they are substantive.
    for lesson in LESSONS:
        assert len(worked_example(lesson.id)) > 40, lesson.id
