from code_runner import run_python_with_tests
from curriculum import LESSONS, get_lesson_by_id
from prompt_lab import score_prompt


def test_curriculum_has_lessons():
    assert len(LESSONS) >= 10
    assert all(lesson.id for lesson in LESSONS)
    assert all(lesson.quiz for lesson in LESSONS)
    assert all(lesson.challenge.tests for lesson in LESSONS)


def test_lesson_ids_are_unique():
    ids = [lesson.id for lesson in LESSONS]
    assert len(ids) == len(set(ids))


def test_quiz_answers_are_valid_options():
    for lesson in LESSONS:
        for question in lesson.quiz:
            assert question.answer in question.options, lesson.id


def test_get_lesson_by_id():
    first = LESSONS[0]
    assert get_lesson_by_id(first.id).title == first.title


def test_prompt_score_stronger_prompt_scores_higher():
    weak = score_prompt("fix this")
    strong = score_prompt(
        "Role: Python tutor. Task: explain this loop error. Context: I am a beginner. "
        "Constraints: do not give the final answer. Output format: 3 bullet points and one test. "
        "Example code: for x in range(3): print(x). Verification: include an edge case."
    )
    assert strong.score > weak.score


def test_all_sample_solutions_pass_their_lesson_tests():
    for lesson in LESSONS:
        result = run_python_with_tests(lesson.challenge.sample_solution, lesson.challenge.tests)
        assert result.ok, f"{lesson.id} failed: {result.stderr}"
