from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from progress import profile_slug


@dataclass(frozen=True)
class ProgressBackup:
    path: Path
    created_at: str
    size_bytes: int


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def backup_dir_for(data_dir: str | Path) -> Path:
    return Path(data_dir) / "backups"


def create_progress_backup(
    progress_data: Mapping[str, Any],
    data_dir: str | Path,
    profile_name: str = "guest",
    max_backups: int = 10,
) -> ProgressBackup:
    """Write a timestamped JSON backup and prune old backups for this profile."""
    backup_dir = backup_dir_for(data_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    slug = profile_slug(profile_name)
    path = backup_dir / f"progress_{slug}_{_timestamp()}.json"
    payload = {
        "backup_schema": 1,
        "profile_name": profile_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "progress": dict(progress_data),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    prune_progress_backups(data_dir, profile_name=profile_name, keep=max_backups)
    return ProgressBackup(path=path, created_at=payload["created_at"], size_bytes=path.stat().st_size)


def list_progress_backups(data_dir: str | Path, profile_name: str = "guest") -> tuple[ProgressBackup, ...]:
    backup_dir = backup_dir_for(data_dir)
    slug = profile_slug(profile_name)
    backups: list[ProgressBackup] = []
    if not backup_dir.exists():
        return ()
    for path in backup_dir.glob(f"progress_{slug}_*.json"):
        try:
            stat = path.stat()
        except OSError:
            continue
        backups.append(
            ProgressBackup(
                path=path,
                created_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                size_bytes=stat.st_size,
            )
        )
    return tuple(sorted(backups, key=lambda item: item.path.name, reverse=True))


def prune_progress_backups(data_dir: str | Path, profile_name: str = "guest", keep: int = 10) -> None:
    keep_count = max(int(keep or 0), 1)
    for backup in list_progress_backups(data_dir, profile_name=profile_name)[keep_count:]:
        try:
            backup.path.unlink()
        except OSError:
            continue


def backup_summary(data_dir: str | Path, profile_name: str = "guest") -> str:
    backups = list_progress_backups(data_dir, profile_name=profile_name)
    if not backups:
        return "No backups yet. Create one before major changes or deployment."
    latest = backups[0]
    return f"{len(backups)} backup(s). Latest: {latest.path.name} ({latest.size_bytes} bytes)."
