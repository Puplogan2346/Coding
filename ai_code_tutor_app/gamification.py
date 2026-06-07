from __future__ import annotations

from dataclasses import dataclass

from projects import completed_project_milestones_count


@dataclass(frozen=True)
class Badge:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class LevelBand:
    threshold: int
    title: str


LEVEL_BANDS: tuple[LevelBand, ...] = (
    LevelBand(0, "Level 1 - New Coder"),
    LevelBand(150, "Level 2 - Habit Builder"),
    LevelBand(450, "Level 3 - Python Explorer"),
    LevelBand(800, "Level 4 - Project Builder"),
    LevelBand(1200, "Level 5 - AI App Maker"),
    LevelBand(1800, "Level 6 - Capstone Builder"),
    LevelBand(2100, "Level 7 - Learning App Builder"),
)


BADGES: tuple[Badge, ...] = (
    Badge("first_step", "First Step", "Completed your first Python lesson."),
    Badge("daily_gym", "Daily Gym", "Saved your first daily coding-gym proof card."),
    Badge("mistake_mapper", "Mistake Mapper", "Turned a bug or confusion into a review card."),
    Badge("quiz_starter", "Quiz Starter", "Finished your first quiz."),
    Badge("focus_reset", "Focus Reset", "Used the Focus Coach or saved a focus check-in."),
    Badge("code_runner", "Code Explorer", "Completed three lessons or more."),
    Badge("prompt_builder", "Prompt Builder", "Scored 8 or higher in Prompt Lab."),
    Badge("project_starter", "Project Starter", "Completed your first project milestone."),
    Badge("week_one", "Week One", "Completed seven daily missions."),
    Badge("halfway", "Halfway There", "Completed fifteen daily missions."),
    Badge("python_foundation", "Python Foundation", "Completed all core Python lessons."),
    Badge("ai_track", "AI Track Starter", "Started an official AI resource."),
    Badge("capstone_ready", "Capstone Ready", "Completed the 30-day mission plan."),
    Badge("capstone_shipper", "Capstone Shipper", "Completed five or more project milestones."),
)


def calculate_xp(progress_data: dict) -> int:
    lesson_xp = 50 * len(progress_data.get("completed_lessons", []) or [])
    quiz_xp = 0
    for score in (progress_data.get("quiz_scores", {}) or {}).values():
        quiz_xp += int(round(score.get("percent", 0) / 10))
    prompt_xp = sum(int(item.get("score", 0)) for item in progress_data.get("prompt_scores", []) or [])
    mission_xp = 25 * sum(
        1
        for item in (progress_data.get("daily_missions", {}) or {}).values()
        if item.get("status") == "Completed"
    )
    official_xp = 20 * sum(
        1
        for status in (progress_data.get("official_ai_status", {}) or {}).values()
        if status in {"Queued", "In progress", "Completed"}
    )
    gym_xp = 15 * sum(
        1
        for item in (progress_data.get("gym_sessions", {}) or {}).values()
        if item.get("status") == "Saved"
    )
    mistake_xp = min(5 * len(progress_data.get("mistake_cards", []) or []), 100)
    focus_xp = min(5 * len(progress_data.get("focus_checkins", []) or []), 100)
    project_xp = 30 * completed_project_milestones_count(progress_data)
    return lesson_xp + quiz_xp + prompt_xp + mission_xp + gym_xp + mistake_xp + official_xp + focus_xp + project_xp


def current_level_band(xp: int) -> LevelBand:
    clean_xp = max(int(xp or 0), 0)
    current = LEVEL_BANDS[0]
    for band in LEVEL_BANDS:
        if clean_xp >= band.threshold:
            current = band
    return current


def next_level_band(xp: int) -> LevelBand | None:
    clean_xp = max(int(xp or 0), 0)
    for band in LEVEL_BANDS:
        if clean_xp < band.threshold:
            return band
    return None


def level_for_xp(xp: int) -> str:
    return current_level_band(xp).title


def xp_to_next_level(xp: int) -> int:
    next_band = next_level_band(xp)
    if next_band is None:
        return 0
    return max(next_band.threshold - max(int(xp or 0), 0), 0)


def level_progress_percent(xp: int) -> float:
    clean_xp = max(int(xp or 0), 0)
    current = current_level_band(clean_xp)
    next_band = next_level_band(clean_xp)
    if next_band is None:
        return 1.0
    span = max(next_band.threshold - current.threshold, 1)
    return round((clean_xp - current.threshold) / span, 3)


def earned_badges(progress_data: dict, total_lessons: int) -> list[Badge]:
    completed_lessons = progress_data.get("completed_lessons", []) or []
    quiz_scores = progress_data.get("quiz_scores", {}) or {}
    prompt_scores = progress_data.get("prompt_scores", []) or []
    daily_missions = progress_data.get("daily_missions", {}) or {}
    gym_sessions = progress_data.get("gym_sessions", {}) or {}
    mistake_cards = progress_data.get("mistake_cards", []) or []
    official_status = progress_data.get("official_ai_status", {}) or {}
    completed_missions = sum(1 for item in daily_missions.values() if item.get("status") == "Completed")
    project_milestones = completed_project_milestones_count(progress_data)

    earned_ids: set[str] = set()
    if completed_lessons:
        earned_ids.add("first_step")
    if any(item.get("status") == "Saved" for item in gym_sessions.values()):
        earned_ids.add("daily_gym")
    if mistake_cards:
        earned_ids.add("mistake_mapper")
    if quiz_scores:
        earned_ids.add("quiz_starter")
    if progress_data.get("focus_checkins"):
        earned_ids.add("focus_reset")
    if len(completed_lessons) >= 3:
        earned_ids.add("code_runner")
    if any(item.get("score", 0) >= 8 for item in prompt_scores):
        earned_ids.add("prompt_builder")
    if project_milestones >= 1:
        earned_ids.add("project_starter")
    if completed_missions >= 7:
        earned_ids.add("week_one")
    if completed_missions >= 15:
        earned_ids.add("halfway")
    if len(completed_lessons) >= total_lessons:
        earned_ids.add("python_foundation")
    if any(status in {"Queued", "In progress", "Completed"} for status in official_status.values()):
        earned_ids.add("ai_track")
    if completed_missions >= 30:
        earned_ids.add("capstone_ready")
    if project_milestones >= 5:
        earned_ids.add("capstone_shipper")

    return [badge for badge in BADGES if badge.id in earned_ids]
