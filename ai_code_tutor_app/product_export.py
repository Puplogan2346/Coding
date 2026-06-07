from __future__ import annotations

import io
import json
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Sequence

from gamification import calculate_xp, earned_badges, level_for_xp
from learning_path import graduation_readiness, milestone_statuses, learning_outcomes
from projects import completed_project_milestones_count
from study_plan import completed_mission_days

APP_EXPORT_VERSION = "16.0"


@dataclass(frozen=True)
class ExportArtifact:
    filename: str
    content: str
    mime: str = "text/plain"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def unwrap_progress_import(payload: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """Accept either raw progress JSON or a v16 backup wrapper."""
    if not isinstance(payload, Mapping):
        return None
    if isinstance(payload.get("progress"), Mapping):
        return dict(payload["progress"])
    if "completed_lessons" in payload or "gym_sessions" in payload or "daily_missions" in payload:
        return dict(payload)
    return None


def progress_backup_payload(profile_name: str, profile_slug: str, progress_data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "app": "AI Code Tutor",
        "export_version": APP_EXPORT_VERSION,
        "exported_at": _now(),
        "profile_name": profile_name,
        "profile_slug": profile_slug,
        "kind": "private_learning_backup",
        "progress": dict(progress_data),
    }


def _lesson_title(lesson: Any) -> str:
    return str(getattr(lesson, "title", lesson))


def _lesson_id(lesson: Any) -> str:
    return str(getattr(lesson, "id", ""))


def learning_transcript_markdown(
    profile_name: str,
    progress_data: Mapping[str, Any],
    lessons: Sequence[Any],
    daily_plan: Sequence[Any],
) -> str:
    lesson_ids = [_lesson_id(lesson) for lesson in lessons]
    completed = set(progress_data.get("completed_lessons", []) or [])
    readiness = graduation_readiness(dict(progress_data), total_lessons=len(lessons))
    xp = calculate_xp(dict(progress_data))
    badge_titles = [badge.title for badge in earned_badges(dict(progress_data), len(lessons))]
    gym_sessions = progress_data.get("gym_sessions", {}) or {}
    saved_sessions = [item for item in gym_sessions.values() if isinstance(item, Mapping) and item.get("status") == "Saved"]
    proof_lines = []
    for item in sorted(saved_sessions, key=lambda raw: int(raw.get("day", 0) or 0))[-10:]:
        proof = str(item.get("proof_note", "") or "").strip() or "Proof saved."
        proof_lines.append(f"- Day {item.get('day')}: {proof[:180]}")

    lines = [
        f"# AI Code Tutor Learning Transcript: {profile_name}",
        "",
        f"Exported: {_now()}",
        f"Graduation status: **{readiness.status}** ({int(readiness.percent * 100)}%)",
        f"XP / level: **{xp} XP** — {level_for_xp(xp)}",
        f"Daily missions complete: **{len(completed_mission_days(dict(progress_data)))}/{len(daily_plan)}**",
        f"Project milestones complete: **{completed_project_milestones_count(dict(progress_data))}**",
        "",
        "## Learning promise",
        "By the end of this path, the learner should be able to read and write basic Python, debug beginner errors, break problems into steps, use tests, build small projects, and use AI as a learning partner rather than a shortcut.",
        "",
        "## Completed lessons",
    ]
    for lesson in lessons:
        check = "x" if _lesson_id(lesson) in completed else " "
        lines.append(f"- [{check}] {_lesson_title(lesson)}")
    lines.extend(["", "## Milestones"])
    for status in milestone_statuses(dict(progress_data)):
        lines.append(f"- **{status.milestone.title}** — {status.status} ({int(status.percent * 100)}%). Next: {status.next_action}")
    lines.extend(["", "## Outcomes practiced"])
    for outcome in learning_outcomes():
        lines.append(f"- {outcome}")
    lines.extend(["", "## Recent proof cards"])
    if proof_lines:
        lines.extend(proof_lines)
    else:
        lines.append("- No saved proof cards yet.")
    lines.extend(["", "## Badge shelf"])
    if badge_titles:
        lines.extend(f"- {title}" for title in badge_titles)
    else:
        lines.append("- No badges yet.")
    lines.extend(["", "## Next action", readiness.next_action, ""])
    return "\n".join(lines)


def certificate_markdown(profile_name: str, progress_data: Mapping[str, Any], lessons: Sequence[Any]) -> str:
    readiness = graduation_readiness(dict(progress_data), total_lessons=len(lessons))
    xp = calculate_xp(dict(progress_data))
    status_line = "Ready to graduate" if readiness.status == "Ready to graduate" else f"In progress: {int(readiness.percent * 100)}% ready"
    return "\n".join(
        [
            "# AI Code Tutor Graduation Certificate",
            "",
            f"Learner: **{profile_name}**",
            f"Status: **{status_line}**",
            f"Generated: {_now()}",
            "",
            "This certificate represents private learning proof from the AI Code Tutor app. It is not an accredited credential; it is a personal evidence record of Python basics, coding habits, debugging, project practice, and AI-assisted learning skills.",
            "",
            "## Evidence summary",
            f"- Lessons completed: {len(progress_data.get('completed_lessons', []) or [])}/{len(lessons)}",
            f"- Daily missions completed: {len(completed_mission_days(dict(progress_data)))}",
            f"- Proof cards saved: {sum(1 for item in (progress_data.get('gym_sessions', {}) or {}).values() if isinstance(item, Mapping) and item.get('status') == 'Saved')}",
            f"- Project milestones completed: {completed_project_milestones_count(dict(progress_data))}",
            f"- XP: {xp}",
            "",
            "## Graduation promise",
            "I can explain basic Python concepts, write small scripts, debug beginner mistakes, use tests/checklists, build a small project, and use AI for hints, review, and verification without skipping understanding.",
            "",
            f"Next action: {readiness.next_action}",
            "",
        ]
    )


def backup_zip_bytes(
    profile_name: str,
    profile_slug: str,
    progress_data: Mapping[str, Any],
    lessons: Sequence[Any],
    daily_plan: Sequence[Any],
) -> bytes:
    backup = progress_backup_payload(profile_name, profile_slug, progress_data)
    transcript = learning_transcript_markdown(profile_name, progress_data, lessons, daily_plan)
    certificate = certificate_markdown(profile_name, progress_data, lessons)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("progress_backup.json", json.dumps(backup, indent=2, sort_keys=True))
        zf.writestr("learning_transcript.md", transcript)
        zf.writestr("graduation_certificate.md", certificate)
        zf.writestr("README.txt", "This private backup contains your AI Code Tutor progress, transcript, and certificate preview. Keep it private.\n")
    return buffer.getvalue()
