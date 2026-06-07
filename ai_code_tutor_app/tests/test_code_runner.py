from code_runner import run_python_with_tests


def test_code_runner_success():
    result = run_python_with_tests("def add(a, b):\n    return a + b", "assert add(2, 3) == 5")
    assert result.ok
    assert result.returncode == 0


def test_code_runner_failure():
    result = run_python_with_tests("def add(a, b):\n    return a - b", "assert add(2, 3) == 5")
    assert not result.ok
    assert result.returncode != 0
    assert "AssertionError" in result.stderr


def test_code_runner_timeout():
    result = run_python_with_tests("while True:\n    pass", "", timeout_seconds=1)
    assert not result.ok
    assert result.timed_out
