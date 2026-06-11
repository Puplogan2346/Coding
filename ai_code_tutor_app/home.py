"""Home dashboard logic — the auto-generated command center.

Pure functions (no Streamlit) that assemble the Home tab's sections from the
learner's progress, mirroring a bootcamp-dashboard structure: a task list for
today, open "bugs" (mistake cards), and project snapshots. The Home tab renders
these; keeping the selection logic here makes it unit-testable.
"""
from __future__ import annotations

from typing import Any, List, Mapping

from curriculum import get_lesson_by_id
from flashcards import stats as flashcard_stats
from projects import PROJECTS, next_project_milestone, project_completion_percent, recommended_project_id
from review import lessons_to_review, next_lesson_to_study
from study_plan import next_mission


def build_todo_items(progress_data: Mapping[str, Any]) -> List[dict]:
    """Auto-generate today's short to-do list from real progress.

    Capped at six items so the dashboard stays glanceable: today's mission,
    the next lesson, up to two quizzes worth passing, due flashcards, and the
    next checkpoint on the recommended project.
    """
    items: List[dict] = []

    mission = next_mission(progress_data)
    items.append({"icon": "🏠", "label": f"Day {mission.day} workout: {mission.title}", "where": "Today"})

    next_lesson = next_lesson_to_study(progress_data)
    completed = set(progress_data.get("completed_lessons", []) or [])
    if next_lesson.id not in completed:
        items.append({"icon": "📚", "label": f"Study: {next_lesson.title}", "where": "Lessons"})

    for lesson in lessons_to_review(progress_data)[:2]:
        items.append({"icon": "✏️", "label": f"Pass the quiz: {lesson.title}", "where": "Review"})

    due = flashcard_stats(progress_data)["due"]
    if due:
        items.append({"icon": "🃏", "label": f"Review {due} flashcard{'s' if due != 1 else ''}", "where": "Review"})

    project = next(p for p in PROJECTS if p.id == recommended_project_id(progress_data))
    milestone = next_project_milestone(progress_data, project.id)
    items.append({"icon": "🛠️", "label": f"{project.title}: {milestone.title}", "where": "Projects"})

    return items[:6]


def open_mistakes(progress_data: Mapping[str, Any], limit: int = 3) -> List[dict]:
    """Newest open mistake cards — the dashboard's 'Bugs & Issues' section."""
    cards = [
        card
        for card in (progress_data.get("mistake_cards", []) or [])
        if isinstance(card, dict) and card.get("status", "Open") == "Open"
    ]
    return list(reversed(cards))[:limit]


def project_rows(progress_data: Mapping[str, Any]) -> List[dict]:
    """Per-project snapshot rows: title, level, completion %, next milestone."""
    recommended = recommended_project_id(progress_data)
    rows = []
    for project in PROJECTS:
        rows.append(
            {
                "title": project.title,
                "level": project.level,
                "percent": int(project_completion_percent(progress_data, project.id) * 100),
                "next_milestone": next_project_milestone(progress_data, project.id).title,
                "recommended": project.id == recommended,
            }
        )
    # Recommended first, then by progress (active work floats up).
    return sorted(rows, key=lambda row: (not row["recommended"], -row["percent"]))


def lesson_title(lesson_id: str) -> str:
    try:
        return get_lesson_by_id(lesson_id).title
    except Exception:
        return lesson_id or "General"
