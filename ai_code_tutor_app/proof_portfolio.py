from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from learning_path import (
    GRADUATION_PROMISE,
    graduation_readiness,
    learning_outcomes,
    milestone_statuses,
    skill_statuses,
)


@dataclass(frozen=True)
class PortfolioStats:
    completed_lessons: int
    total_lessons: int
    saved_proofs: int
    completed_daily_missions: int
    passed_quizzes: int
    project_checkpoints: int
    mistake_cards: int
    strong_prompts: int
    graduation_status: str
    graduation_percent: float


def _now_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _lesson_title_map(lessons: Iterable[Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for lesson in lessons:
        lesson_id = str(getattr(lesson, "id", "") or "")
        title = str(getattr(lesson, "title", lesson_id) or lesson_id)
        if lesson_id:
            mapping[lesson_id] = title
    return mapping


def _saved_gym_sessions(progress_data: Mapping[str, Any]) -> list[dict[str, Any]]:
    sessions = []
    for day_text, item in (progress_data.get("gym_sessions", {}) or {}).items():
        if not isinstance(item, Mapping) or item.get("status") != "Saved":
            continue
        try:
            day = int(item.get("day", day_text))
        except (TypeError, ValueError):
            day = 0
        sessions.append({"day": day, **dict(item)})
    return sorted(sessions, key=lambda item: item.get("day", 0))


def _completed_daily_missions(progress_data: Mapping[str, Any]) -> int:
    return sum(
        1
        for item in (progress_data.get("daily_missions", {}) or {}).values()
        if isinstance(item, Mapping) and item.get("status") == "Completed"
    )


def _passed_quizzes(progress_data: Mapping[str, Any], minimum_percent: float = 70) -> int:
    total = 0
    for item in (progress_data.get("quiz_scores", {}) or {}).values():
        if not isinstance(item, Mapping):
            continue
        try:
            percent = float(item.get("percent", 0) or 0)
        except (TypeError, ValueError):
            percent = 0
        if percent >= minimum_percent:
            total += 1
    return total


def _project_checkpoint_count(progress_data: Mapping[str, Any]) -> int:
    total = 0
    projects = progress_data.get("project_milestones", {}) or {}
    if not isinstance(projects, Mapping):
        return 0
    for project in projects.values():
        if not isinstance(project, Mapping):
            continue
        total += sum(1 for item in project.values() if isinstance(item, Mapping) and item.get("status") == "Completed")
    return total


def _mistake_count(progress_data: Mapping[str, Any]) -> int:
    return sum(1 for item in (progress_data.get("mistake_cards", []) or []) if isinstance(item, Mapping))


def _strong_prompt_count(progress_data: Mapping[str, Any]) -> int:
    total = 0
    for item in (progress_data.get("prompt_scores", []) or []):
        if not isinstance(item, Mapping):
            continue
        try:
            score = int(item.get("score", 0) or 0)
        except (TypeError, ValueError):
            score = 0
        if score >= 7:
            total += 1
    return total


def portfolio_stats(progress_data: Mapping[str, Any], total_lessons: int = 12) -> PortfolioStats:
    ready = graduation_readiness(progress_data, total_lessons=total_lessons)
    return PortfolioStats(
        completed_lessons=len(progress_data.get("completed_lessons", []) or []),
        total_lessons=total_lessons,
        saved_proofs=len(_saved_gym_sessions(progress_data)),
        completed_daily_missions=_completed_daily_missions(progress_data),
        passed_quizzes=_passed_quizzes(progress_data),
        project_checkpoints=_project_checkpoint_count(progress_data),
        mistake_cards=_mistake_count(progress_data),
        strong_prompts=_strong_prompt_count(progress_data),
        graduation_status=ready.status,
        graduation_percent=ready.percent,
    )


def proof_portfolio_markdown(progress_data: Mapping[str, Any], lessons: Iterable[Any], profile_name: str = "Learner") -> str:
    lesson_titles = _lesson_title_map(lessons)
    total_lessons = len(lesson_titles) or 12
    stats = portfolio_stats(progress_data, total_lessons=total_lessons)
    ready = graduation_readiness(progress_data, total_lessons=total_lessons)
    lines: list[str] = [
        f"# AI Code Tutor Proof Portfolio - {profile_name}",
        "",
        f"Generated: {_now_text()}",
        "",
        "## Learning goal",
        GRADUATION_PROMISE,
        "",
        "## Progress summary",
        f"- Graduation status: **{stats.graduation_status}** ({round(stats.graduation_percent * 100)}%)",
        f"- Lessons completed: {stats.completed_lessons}/{stats.total_lessons}",
        f"- Daily coding-gym sessions completed: {stats.completed_daily_missions}",
        f"- Proof cards saved: {stats.saved_proofs}",
        f"- Quizzes passed: {stats.passed_quizzes}",
        f"- Project checkpoints completed: {stats.project_checkpoints}",
        f"- Mistake/review cards logged: {stats.mistake_cards}",
        f"- Strong prompt reps: {stats.strong_prompts}",
        "",
        "## Graduation checklist",
    ]
    for req in ready.requirements:
        mark = "x" if req.complete else " "
        lines.append(f"- [{mark}] {req.title}: {req.current}/{req.target} — {req.proof}")
    lines.extend(["", f"Next action: {ready.next_action}", "", "## Milestone evidence"])
    for status in milestone_statuses(progress_data):
        lines.append(f"### {status.milestone.title}")
        lines.append(f"Status: {status.status} ({round(status.percent * 100)}%)")
        lines.append(f"Goal: {status.milestone.goal}")
        lines.append(f"Proof target: {status.milestone.proof}")
        lines.append("Evidence: " + "; ".join(status.evidence))
        lines.append(f"Next: {status.next_action}")
        lines.append("")
    lines.append("## Skill outcomes")
    for skill in skill_statuses(progress_data):
        lines.append(f"- {skill.status}: {skill.skill.title} — {skill.skill.description}")
    lines.extend(["", "## Lessons completed"])
    completed = set(str(item) for item in progress_data.get("completed_lessons", []) or [])
    for lesson_id, title in lesson_titles.items():
        mark = "x" if lesson_id in completed else " "
        lines.append(f"- [{mark}] {title} (`{lesson_id}`)")
    lines.extend(["", "## Recent proof cards"])
    proofs = _saved_gym_sessions(progress_data)[-10:]
    if not proofs:
        lines.append("No proof cards saved yet.")
    for item in proofs:
        proof = str(item.get("proof_note", "") or "").strip() or "No proof note saved."
        next_review = str(item.get("next_review", "") or "").strip()
        lesson_id = str(item.get("lesson_id", "") or "")
        lesson_title = lesson_titles.get(lesson_id, lesson_id or "No linked lesson")
        lines.append(f"### Day {item.get('day', '?')} - {lesson_title}")
        lines.append(f"Pace: {item.get('pace', 'n/a')} | Minutes: {item.get('minutes', 'n/a')}")
        lines.append(f"Proof: {proof}")
        if next_review:
            lines.append(f"Next review: {next_review}")
        lines.append("")
    mistakes = [item for item in (progress_data.get("mistake_cards", []) or []) if isinstance(item, Mapping)]
    lines.append("## Mistake notebook highlights")
    if not mistakes:
        lines.append("No mistake cards logged yet.")
    for item in mistakes[-10:]:
        lines.append(f"- {item.get('concept', 'Review')}: {item.get('mistake', '')} → {item.get('fix', '')}")
    lines.extend(["", "## What I should know by the end"])
    for outcome in learning_outcomes():
        lines.append(f"- {outcome}")
    return "\n".join(lines).strip() + "\n"


def graduation_certificate_markdown(progress_data: Mapping[str, Any], lessons: Iterable[Any], profile_name: str = "Learner") -> str:
    total_lessons = len(_lesson_title_map(lessons)) or 12
    ready = graduation_readiness(progress_data, total_lessons=total_lessons)
    status_line = "Ready to graduate" if ready.status == "Ready to graduate" else f"In progress: {round(ready.percent * 100)}% ready"
    lines = [
        "# AI Code Tutor Completion Certificate",
        "",
        f"Learner: **{profile_name}**",
        f"Generated: {_now_text()}",
        f"Status: **{status_line}**",
        "",
        "This certificate is a private proof-of-learning artifact from the AI Code Tutor daily coding gym.",
        "",
        "## Completion promise",
        GRADUATION_PROMISE,
        "",
        "## Evidence summary",
    ]
    for req in ready.requirements:
        mark = "Complete" if req.complete else "In progress"
        lines.append(f"- {mark}: {req.title} ({req.current}/{req.target})")
    lines.extend(["", f"Next action: {ready.next_action}"])
    return "\n".join(lines).strip() + "\n"
