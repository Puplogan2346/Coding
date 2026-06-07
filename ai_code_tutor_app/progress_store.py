from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class StorageSnapshot:
    profile_slug: str
    updated_at: str
    data: dict[str, Any]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_db_path(data_dir: Path | str) -> Path:
    return Path(data_dir) / "ai_code_tutor_progress.sqlite3"


def init_db(db_path: Path | str) -> Path:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress_snapshots (
                profile_slug TEXT PRIMARY KEY,
                profile_name TEXT NOT NULL,
                data_json TEXT NOT NULL,
                schema_version INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_slug TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
    return path


def save_progress_snapshot(db_path: Path | str, profile_slug: str, profile_name: str, data: dict[str, Any]) -> None:
    path = init_db(db_path)
    payload = json.dumps(data, sort_keys=True)
    updated_at = str(data.get("updated_at") or _now())
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            INSERT INTO progress_snapshots(profile_slug, profile_name, data_json, schema_version, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(profile_slug) DO UPDATE SET
                profile_name=excluded.profile_name,
                data_json=excluded.data_json,
                schema_version=excluded.schema_version,
                updated_at=excluded.updated_at
            """,
            (str(profile_slug), str(profile_name or profile_slug), payload, SCHEMA_VERSION, updated_at),
        )


def load_progress_snapshot(db_path: Path | str, profile_slug: str) -> dict[str, Any] | None:
    path = Path(db_path)
    if not path.exists():
        return None
    try:
        with sqlite3.connect(path) as conn:
            row = conn.execute(
                "SELECT data_json FROM progress_snapshots WHERE profile_slug = ?",
                (str(profile_slug),),
            ).fetchone()
    except sqlite3.Error:
        return None
    if not row:
        return None
    try:
        data = json.loads(row[0])
    except (TypeError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def record_event(db_path: Path | str, profile_slug: str, event_type: str, event: dict[str, Any]) -> None:
    path = init_db(db_path)
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO app_events(profile_slug, event_type, event_json, created_at) VALUES (?, ?, ?, ?)",
            (str(profile_slug), str(event_type), json.dumps(event, sort_keys=True), _now()),
        )


def list_profile_slugs(db_path: Path | str) -> list[str]:
    path = Path(db_path)
    if not path.exists():
        return []
    try:
        with sqlite3.connect(path) as conn:
            rows = conn.execute("SELECT profile_slug FROM progress_snapshots ORDER BY updated_at DESC").fetchall()
    except sqlite3.Error:
        return []
    return [str(row[0]) for row in rows]


def storage_health(db_path: Path | str, required_tables: Iterable[str] = ("progress_snapshots", "app_events")) -> dict[str, Any]:
    path = Path(db_path)
    if not path.exists():
        try:
            init_db(path)
        except sqlite3.Error as exc:
            return {"ok": False, "path": str(path), "message": f"Could not initialize SQLite store: {exc}"}
    try:
        with sqlite3.connect(path) as conn:
            rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    except sqlite3.Error as exc:
        return {"ok": False, "path": str(path), "message": f"Could not read SQLite store: {exc}"}
    tables = {str(row[0]) for row in rows}
    missing = [table for table in required_tables if table not in tables]
    if missing:
        return {"ok": False, "path": str(path), "message": f"Missing tables: {', '.join(missing)}"}
    return {"ok": True, "path": str(path), "message": "SQLite progress store is ready."}
