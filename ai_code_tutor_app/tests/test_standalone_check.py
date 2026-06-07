from __future__ import annotations

from pathlib import Path

from standalone_check import REQUIRED_FILES, standalone_checks, standalone_summary


def test_standalone_checks_pass_for_project_skeleton(tmp_path: Path, monkeypatch):
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    for relative in REQUIRED_FILES:
        target = app_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("ok", encoding="utf-8")
    monkeypatch.delenv("ALLOW_CODE_RUNNER", raising=False)
    monkeypatch.setenv("APP_PRIVATE_PASSCODE", "local-test-passcode")

    checks = standalone_checks(app_dir=app_dir, data_dir=tmp_path / "data")

    required = [check for check in checks if check.required]
    assert all(check.status == "Pass" for check in required)
    assert "Standalone basics look ready" in standalone_summary(checks)


def test_standalone_check_warns_when_code_runner_is_on(tmp_path: Path, monkeypatch):
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    for relative in REQUIRED_FILES:
        target = app_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("ok", encoding="utf-8")
    monkeypatch.setenv("ALLOW_CODE_RUNNER", "true")

    checks = standalone_checks(app_dir=app_dir, data_dir=tmp_path / "data")
    code_runner = next(check for check in checks if check.id == "code-runner-public-safe")

    assert code_runner.status == "Warning"
    assert "sandbox" in code_runner.detail
    assert "warning" in standalone_summary(checks).lower()


def test_standalone_checks_report_missing_required_files(tmp_path: Path):
    checks = standalone_checks(app_dir=tmp_path, data_dir=tmp_path / "data")
    missing = [check for check in checks if check.required and check.status == "Fix needed"]

    assert missing
    assert "required standalone check" in standalone_summary(checks)
