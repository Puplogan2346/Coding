"""Build Studio content and framework tests.

The content tests mirror the curriculum auto-grader constraint: every step's
cumulative sample solution must pass its own static checks and its (stdlib
only) tests, so the guide never teaches something the checker rejects.
"""
import ast

from build_checks import StepCheck, all_checks_pass, run_static_checks
from code_runner import run_python_with_tests
from curriculum import get_lesson_by_id
from progress import (
    default_progress,
    normalize_progress_data,
    record_build_step,
    save_build_code,
)
from project_builds import (
    PROJECT_BUILDS,
    build_completion_percent,
    build_for_project,
    editor_seed,
    guide_code_before_step,
    next_build_step_index,
    passed_build_steps,
)
from projects import project_by_id

EXPECTED_BUILD_IDS = {"quiz_scorekeeper", "habit_tracker_json", "prompt_coach", "text_analyzer"}


def test_every_build_maps_to_a_real_project_and_its_milestones():
    assert set(PROJECT_BUILDS) >= EXPECTED_BUILD_IDS
    for project_id, build in PROJECT_BUILDS.items():
        project = project_by_id(project_id)
        assert [step.id for step in build.steps] == [m.id for m in project.milestones]
        assert build.project_id == project_id
        assert build.filename.endswith(".py")
        assert build.intro.strip() and build.run_hint.strip()
        ast.parse(build.scaffold)


def test_every_build_step_is_complete_and_lessons_exist():
    for build in PROJECT_BUILDS.values():
        for step in build.steps:
            assert step.title and step.goal and step.hint
            assert step.instructions and step.checks
            assert "assert" in step.tests
            for lesson_id in step.lesson_ids:
                get_lesson_by_id(lesson_id)


def test_sample_solutions_pass_their_own_static_checks():
    for build in PROJECT_BUILDS.values():
        for step in build.steps:
            results = run_static_checks(step.sample_solution, step.checks)
            failed = [result.detail for result in results if not result.passed]
            assert all_checks_pass(results), (build.project_id, step.id, failed)


def test_sample_solutions_pass_cumulative_tests():
    for build in PROJECT_BUILDS.values():
        for index, step in enumerate(build.steps):
            for earlier in build.steps[: index + 1]:
                result = run_python_with_tests(step.sample_solution, earlier.tests, timeout_seconds=8)
                assert result.ok, (build.project_id, step.id, earlier.id, result.stderr)


def test_final_program_runs_standalone_without_input():
    for build in PROJECT_BUILDS.values():
        final = build.steps[-1].sample_solution
        assert "input(" not in final
        result = run_python_with_tests(final, "", timeout_seconds=8)
        assert result.ok, (build.project_id, result.stderr)


def test_static_checks_cover_kinds_and_syntax_errors():
    code = (
        "import json\n\n"
        "def save(data):\n"
        "    return json.dumps(data)\n\n"
        "if __name__ == '__main__':\n"
        "    print(save({'a': 1}))\n"
    )
    checks = (
        StepCheck("defines_function", "save", "Define save"),
        StepCheck("uses", "import", "Import something"),
        StepCheck("uses", "main-guard", "Add a main guard"),
        StepCheck("calls", "json.dumps", "Call json.dumps"),
        StepCheck("uses", "dict", "Use a dict"),
    )
    assert all_checks_pass(run_static_checks(code, checks))

    missing = run_static_checks("x = 1", checks)
    assert not any(result.passed for result in missing)

    broken = run_static_checks("def broken(:", checks)
    assert all(not result.passed for result in broken)
    assert "syntax" in broken[0].detail.lower()

    assert not all_checks_pass(())


def test_build_progress_roundtrip_and_helpers():
    build = build_for_project("quiz_scorekeeper")
    data = default_progress(["one"], profile_name="Ava")

    assert editor_seed(data, build) == build.scaffold
    assert next_build_step_index(data, build) == 0
    assert build_completion_percent(data, build) == 0.0

    save_build_code(data, "quiz_scorekeeper", "print('hi')")
    assert editor_seed(data, build) == "print('hi')"

    record_build_step(data, "quiz_scorekeeper", build.steps[0].id, code="print('step')")
    assert passed_build_steps(data, "quiz_scorekeeper") == {build.steps[0].id}
    assert next_build_step_index(data, build) == 1
    assert build_completion_percent(data, build) == 0.2

    normalized = normalize_progress_data(data, ["one"], profile_name="Ava")
    assert passed_build_steps(normalized, "quiz_scorekeeper") == {build.steps[0].id}

    assert guide_code_before_step(build, 0) == build.scaffold
    assert guide_code_before_step(build, 2) == build.steps[1].sample_solution
