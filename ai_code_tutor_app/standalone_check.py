from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from private_access import private_access_status
from progress_store import default_db_path, storage_health


@dataclass(frozen=True)
class StandaloneCheck:
    id: str
    title: str
    status: str
    detail: str
    required: bool = True


REQUIRED_FILES: tuple[str, ...] = (
    "app.py",
    "streamlit_app.py",
    "requirements.txt",
    "README.md",
    "README_DEPLOY.md",
    ".streamlit/config.toml",
    "Dockerfile",
    ".github/workflows/tests.yml",
    "private_access.py",
    "progress_store.py",
    "product_export.py",
)


def _exists_check(app_dir: Path, relative_path: str) -> StandaloneCheck:
    exists = (app_dir / relative_path).exists()
    return StandaloneCheck(
        id=f"file:{relative_path}",
        title=f"Required file: {relative_path}",
        status="Pass" if exists else "Fix needed",
        detail="Present." if exists else "Missing. Add this file before deploying outside ChatGPT.",
    )


def _data_dir_check(data_dir: Path) -> StandaloneCheck:
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        probe = data_dir / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        ok = True
    except OSError as exc:
        ok = False
        detail = f"Could not write progress data: {exc}"
    else:
        detail = f"Progress directory is writable: {data_dir}"
    return StandaloneCheck("data-writable", "Progress storage writable", "Pass" if ok else "Fix needed", detail)


def _sqlite_storage_check(data_dir: Path) -> StandaloneCheck:
    health = storage_health(default_db_path(data_dir))
    return StandaloneCheck(
        "sqlite-progress-store",
        "SQLite progress backup store",
        "Pass" if health.get("ok") else "Fix needed",
        str(health.get("message", "")) + f" Path: {health.get('path', default_db_path(data_dir))}",
    )


def _code_runner_check() -> StandaloneCheck:
    enabled = os.getenv("ALLOW_CODE_RUNNER", "false").strip().lower() in {"1", "true", "yes", "on"}
    return StandaloneCheck(
        "code-runner-public-safe",
        "Public code runner disabled",
        "Pass" if not enabled else "Warning",
        "ALLOW_CODE_RUNNER is off. Good for sharing." if not enabled else "ALLOW_CODE_RUNNER is on. Only use this locally or with a real sandbox.",
        required=False,
    )


def _secret_file_check(app_dir: Path) -> StandaloneCheck:
    real_secret = app_dir / ".streamlit" / "secrets.toml"
    if real_secret.exists():
        return StandaloneCheck(
            "secrets-not-committed",
            "No real secrets file in package",
            "Warning",
            "A local .streamlit/secrets.toml file exists. Keep it out of git; use platform secrets when deploying.",
            required=False,
        )
    return StandaloneCheck("secrets-not-committed", "No real secrets file in package", "Pass", "Only the secrets example file is expected.")


def _private_access_check() -> StandaloneCheck:
    status = private_access_status()
    if status.required and status.configured:
        return StandaloneCheck(
            "private-access",
            "Private access gate configured",
            "Pass",
            f"Private gate will require a passcode from {status.passcode_source}.",
        )
    if status.required and not status.configured:
        return StandaloneCheck(
            "private-access",
            "Private access gate configured",
            "Fix needed",
            "APP_PRIVATE_MODE is enabled but APP_PRIVATE_PASSCODE is missing.",
        )
    return StandaloneCheck(
        "private-access",
        "Private access gate configured",
        "Warning",
        "No private passcode is set. Fine for local use, but set APP_PRIVATE_PASSCODE before hosting.",
        required=False,
    )


def _openai_key_check() -> StandaloneCheck:
    configured = bool(os.getenv("OPENAI_API_KEY"))
    return StandaloneCheck(
        "openai-key-optional",
        "AI tutor key configured",
        "Pass" if configured else "Optional",
        "OPENAI_API_KEY is set for AI Tutor." if configured else "App still runs without an API key; AI Tutor buttons stay optional/disabled.",
        required=False,
    )


def standalone_checks(app_dir: str | Path = ".", data_dir: str | Path | None = None) -> tuple[StandaloneCheck, ...]:
    app_path = Path(app_dir)
    configured_data = Path(data_dir) if data_dir is not None else app_path / os.getenv("APP_DATA_DIR", "data")
    checks: list[StandaloneCheck] = [_exists_check(app_path, path) for path in REQUIRED_FILES]
    checks.append(_data_dir_check(configured_data))
    checks.append(_sqlite_storage_check(configured_data))
    checks.append(_secret_file_check(app_path))
    checks.append(_private_access_check())
    checks.append(_code_runner_check())
    checks.append(_openai_key_check())
    return tuple(checks)


def standalone_summary(checks: Iterable[StandaloneCheck]) -> str:
    checks = tuple(checks)
    required = [check for check in checks if check.required]
    failed = [check for check in required if check.status != "Pass"]
    warnings = [check for check in checks if check.status == "Warning"]
    if not failed and not warnings:
        return "Standalone basics look ready. Run pytest and launch Streamlit locally before deploying."
    if failed:
        return f"{len(failed)} required standalone check(s) need attention before deployment."
    return f"Required checks passed with {len(warnings)} warning(s) to review."
