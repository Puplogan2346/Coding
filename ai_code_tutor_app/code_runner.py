from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunResult:
    ok: bool
    stdout: str
    stderr: str
    returncode: int | None
    timed_out: bool = False


def code_runner_enabled() -> bool:
    return os.getenv("ALLOW_CODE_RUNNER", "").lower() in {"1", "true", "yes", "on"}


def run_python_with_tests(user_code: str, tests: str, timeout_seconds: int = 4) -> RunResult:
    """
    Runs learner code plus lesson tests in a local subprocess.

    This is useful for local self-study. It is not a secure sandbox for public deployment.
    Do not enable it for untrusted users without a real sandbox/container boundary.
    """
    program = user_code.rstrip() + "\n\n# Lesson tests\n" + tests.strip() + "\n"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        script_path = tmp_path / "submission.py"
        script_path.write_text(program, encoding="utf-8")

        env = {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PATH": os.getenv("PATH", ""),
        }

        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-S", str(script_path)],
                cwd=str(tmp_path),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=env,
            )
        except subprocess.TimeoutExpired as exc:
            return RunResult(
                ok=False,
                stdout=exc.stdout or "",
                stderr=(exc.stderr or "") + f"\nTimed out after {timeout_seconds} seconds.",
                returncode=None,
                timed_out=True,
            )

    return RunResult(
        ok=completed.returncode == 0,
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )
