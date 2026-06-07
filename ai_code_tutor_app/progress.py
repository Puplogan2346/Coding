from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

from progress_store import default_db_path, load_progress_snapshot, save_progress_snapshot
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DATA_DIR = Path(os.getenv("APP_DATA_DIR", "data"))
PROGRESS_FILE = DATA_DIR / "progress_guest.json"
PROGRESS_DB_FILE = default_db_path(DATA_DIR)
APP_TIMEZONE = os.getenv("APP_TIMEZONE", "America/Los_Angeles")
ALLOWED_SESSION_MINUTES = (10, 30, 45)
ALLOWED_REWARD_STYLES = ("Tiny wins", "Badges", "Quiet progress")

DEFAULT_FOCUS_PREFERENCES: dict[str, Any] = {
    "default_minutes": 30,
    "adhd_friendly_mode": True,
    "low_stimulation_mode": False,
    "break_reminders": True,
    "reward_style": "Tiny wins",
}

DEFAULT_LEARNING_CONTRACT: dict[str, Any] = {
    "daily_minutes_goal": 30,
    "weekly_sessions_goal": 5,
    "finish_line": "Learn Python basics and build a small capstone I can explain.",
    "why_it_matters": "I want coding to become useful, fun, and less intimidating.",
    "preferred_review_style": "Tiny daily proof cards",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def app_timezone() -> ZoneInfo:
    """Return the configured learner-facing timezone, falling back safely to UTC."""
    try:
        return ZoneInfo(os.getenv("APP_TIMEZONE", APP_TIMEZONE))
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def local_today() -> date:
    """Return today's date in the timezone used for streaks and check-ins."""
    return datetime.now(app_timezone()).date()


def app_today() -> date:
    """Backward-compatible alias used by tests and docs."""
    return local_today()


def _clean_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        cleaned = value.strip().lower()
        if cleaned in {"true", "yes", "1", "on"}:
            return True
        if cleaned in {"false", "no", "0", "off"}:
            return False
    return default


def sanitize_default_minutes(value: Any) -> int:
    """Normalize saved session length so old/bad imports cannot crash widgets."""
    try:
        minutes = int(value)
    except (TypeError, ValueError):
        return 30
    if minutes in ALLOWED_SESSION_MINUTES:
        return minutes
    return min(ALLOWED_SESSION_MINUTES, key=lambda item: abs(item - minutes))


def sanitize_focus_preferences(preferences: Dict[str, Any] | None) -> Dict[str, Any]:
    """Return safe focus preferences for Streamlit widgets."""
    incoming = preferences if isinstance(preferences, dict) else {}
    clean = dict(DEFAULT_FOCUS_PREFERENCES)
    clean.update(incoming)
    clean["default_minutes"] = sanitize_default_minutes(clean.get("default_minutes"))
    clean["adhd_friendly_mode"] = _clean_bool(clean.get("adhd_friendly_mode"), True)
    clean["low_stimulation_mode"] = _clean_bool(clean.get("low_stimulation_mode"), False)
    clean["break_reminders"] = _clean_bool(clean.get("break_reminders"), True)
    if clean.get("reward_style") not in ALLOWED_REWARD_STYLES:
        clean["reward_style"] = "Tiny wins"
    return clean




def sanitize_learning_contract(contract: Dict[str, Any] | None) -> Dict[str, Any]:
    """Normalize the learner's private goal/contract settings."""
    incoming = contract if isinstance(contract, dict) else {}
    clean = dict(DEFAULT_LEARNING_CONTRACT)
    clean.update(incoming)
    clean["daily_minutes_goal"] = sanitize_default_minutes(clean.get("daily_minutes_goal", 30))
    try:
        weekly = int(clean.get("weekly_sessions_goal", 5) or 5)
    except (TypeError, ValueError):
        weekly = 5
    clean["weekly_sessions_goal"] = min(max(weekly, 1), 7)
    for key in ("finish_line", "why_it_matters", "preferred_review_style"):
        clean[key] = str(clean.get(key, DEFAULT_LEARNING_CONTRACT[key]) or DEFAULT_LEARNING_CONTRACT[key])[:500]
    return clean


def save_learning_contract(data: Dict[str, Any], contract: Dict[str, Any]) -> None:
    data["learning_contract"] = sanitize_learning_contract(contract)


def learning_contract_summary(data: Dict[str, Any]) -> str:
    contract = sanitize_learning_contract(data.get("learning_contract", {}))
    return (
        f"Goal: {contract['finish_line']} Daily target: {contract['daily_minutes_goal']} minutes, "
        f"{contract['weekly_sessions_goal']} day(s)/week. Why: {contract['why_it_matters']}"
    )

def profile_slug(profile_name: str | None) -> str:
    """Return a filesystem-safe learner profile slug."""
    cleaned = (profile_name or "guest").strip().lower()
    cleaned = re.sub(r"[^a-z0-9_-]+", "-", cleaned)
    cleaned = cleaned.strip("-_")
    return cleaned[:48] or "guest"


def progress_path_for_profile(profile_name: str | None) -> Path:
    return DATA_DIR / f"progress_{profile_slug(profile_name)}.json"


def default_progress(lesson_ids: Iterable[str], profile_name: str = "guest") -> Dict[str, Any]:
    lesson_ids = list(lesson_ids)
    return {
        "created_at": _now(),
        "updated_at": _now(),
        "profile_name": profile_name or "guest",
        "completed_lessons": [],
        "quiz_scores": {},
        "notes": {lesson_id: "" for lesson_id in lesson_ids},
        "prompt_scores": [],
        "official_ai_status": {},
        "official_ai_notes": {},
        "daily_missions": {},
        "daily_checklists": {},
        "daily_reflections": [],
        "lesson_completed_at": {},
        "study_streak": 0,
        "longest_streak": 0,
        "last_session_date": "",
        "focus_preferences": dict(DEFAULT_FOCUS_PREFERENCES),
        "learning_contract": dict(DEFAULT_LEARNING_CONTRACT),
        "focus_checkins": [],
        "parking_lot": [],
        "project_milestones": {},
        "gym_sessions": {},
        "mistake_cards": [],
        "flashcards": {},
        "review_history": [],
    }


def normalize_progress_data(
    raw_data: Dict[str, Any] | None,
    lesson_ids: Iterable[str],
    profile_name: str = "guest",
) -> Dict[str, Any]:
    """Merge loaded/imported progress with the current schema and lesson IDs."""
    lesson_ids = list(lesson_ids)
    data = raw_data if isinstance(raw_data, dict) else {}
    base = default_progress(lesson_ids, profile_name=profile_name)
    base.update(data)
    base["profile_name"] = profile_name or str(base.get("profile_name", "guest") or "guest")

    valid_ids = set(lesson_ids)
    completed = base.get("completed_lessons", [])
    if not isinstance(completed, list):
        completed = []
    base["completed_lessons"] = [lesson_id for lesson_id in completed if lesson_id in valid_ids]

    notes = base.get("notes", {})
    if not isinstance(notes, dict):
        notes = {}
    base["notes"] = notes
    for lesson_id in lesson_ids:
        base["notes"].setdefault(lesson_id, "")

    quiz_scores = base.get("quiz_scores", {})
    if not isinstance(quiz_scores, dict):
        quiz_scores = {}
    base["quiz_scores"] = {
        lesson_id: score
        for lesson_id, score in quiz_scores.items()
        if lesson_id in valid_ids and isinstance(score, dict)
    }

    prompt_scores = base.get("prompt_scores", [])
    base["prompt_scores"] = prompt_scores if isinstance(prompt_scores, list) else []

    for key in (
        "official_ai_status",
        "official_ai_notes",
        "daily_missions",
        "daily_checklists",
        "lesson_completed_at",
        "project_milestones",
        "gym_sessions",
        "flashcards",
    ):
        if not isinstance(base.get(key), dict):
            base[key] = {}

    review_history = base.get("review_history", [])
    base["review_history"] = review_history if isinstance(review_history, list) else []

    daily_reflections = base.get("daily_reflections", [])
    base["daily_reflections"] = daily_reflections if isinstance(daily_reflections, list) else []

    base["lesson_completed_at"] = {
        lesson_id: completed_at
        for lesson_id, completed_at in base.get("lesson_completed_at", {}).items()
        if lesson_id in valid_ids
    }

    try:
        base["study_streak"] = max(int(base.get("study_streak", 0) or 0), 0)
    except (TypeError, ValueError):
        base["study_streak"] = 0
    try:
        base["longest_streak"] = max(int(base.get("longest_streak", 0) or 0), base["study_streak"])
    except (TypeError, ValueError):
        base["longest_streak"] = base["study_streak"]
    base["last_session_date"] = str(base.get("last_session_date", "") or "")
    base["focus_preferences"] = sanitize_focus_preferences(base.get("focus_preferences", {}))
    base["learning_contract"] = sanitize_learning_contract(base.get("learning_contract", {}))

    focus_checkins = base.get("focus_checkins", [])
    base["focus_checkins"] = focus_checkins if isinstance(focus_checkins, list) else []
    parking_lot = base.get("parking_lot", [])
    base["parking_lot"] = parking_lot if isinstance(parking_lot, list) else []
    mistake_cards = base.get("mistake_cards", [])
    base["mistake_cards"] = mistake_cards if isinstance(mistake_cards, list) else []
    return base


def _sqlite_enabled() -> bool:
    return os.getenv("APP_DISABLE_SQLITE_BACKUP", "").strip().lower() not in {"1", "true", "yes", "on"}


def progress_db_path() -> Path:
    return default_db_path(DATA_DIR)


def load_progress(
    lesson_ids: Iterable[str],
    path: Path = PROGRESS_FILE,
    profile_name: str = "guest",
) -> Dict[str, Any]:
    lesson_ids = list(lesson_ids)
    data: Dict[str, Any] = {}
    loaded_from_file = False
    if path.exists():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            data = raw if isinstance(raw, dict) else {}
            loaded_from_file = True
        except (json.JSONDecodeError, OSError):
            data = {}

    expected_profile_path = progress_path_for_profile(profile_name)
    use_profile_store = False
    try:
        use_profile_store = path.resolve() == expected_profile_path.resolve() or path.resolve() == PROGRESS_FILE.resolve()
    except OSError:
        use_profile_store = path == expected_profile_path or path == PROGRESS_FILE

    if not loaded_from_file and _sqlite_enabled() and use_profile_store:
        snapshot = load_progress_snapshot(progress_db_path(), profile_slug(profile_name))
        if isinstance(snapshot, dict):
            data = snapshot

    return normalize_progress_data(data, lesson_ids, profile_name=profile_name)


def save_progress(data: Dict[str, Any], path: Path = PROGRESS_FILE) -> None:
    data["updated_at"] = _now()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    if _sqlite_enabled():
        slug = profile_slug(str(data.get("profile_name", "guest") or "guest"))
        save_progress_snapshot(progress_db_path(), slug, str(data.get("profile_name", slug) or slug), data)


def mark_lesson_complete(data: Dict[str, Any], lesson_id: str) -> None:
    completed = data.setdefault("completed_lessons", [])
    if lesson_id not in completed:
        completed.append(lesson_id)
    data.setdefault("lesson_completed_at", {}).setdefault(lesson_id, _now())


def record_quiz_score(data: Dict[str, Any], lesson_id: str, score: int, total: int) -> None:
    data.setdefault("quiz_scores", {})[lesson_id] = {
        "score": score,
        "total": total,
        "percent": round((score / total) * 100, 1) if total else 0,
        "taken_at": _now(),
    }


def record_review_result(data: Dict[str, Any], score: int, total: int) -> None:
    """Persist a mixed-review-quiz result so progress shows review history."""
    data.setdefault("review_history", []).append(
        {
            "score": score,
            "total": total,
            "percent": round((score / total) * 100, 1) if total else 0,
            "taken_at": _now(),
        }
    )


def save_note(data: Dict[str, Any], lesson_id: str, note: str) -> None:
    data.setdefault("notes", {})[lesson_id] = note


def record_prompt_score(data: Dict[str, Any], score: int, prompt: str) -> None:
    data.setdefault("prompt_scores", []).append(
        {
            "score": score,
            "prompt_preview": prompt[:160],
            "created_at": _now(),
        }
    )


def record_official_ai_resource(
    data: Dict[str, Any],
    resource_id: str,
    status: str,
    note: str = "",
) -> None:
    """Track progress on an external official AI learning resource."""
    allowed_statuses = {"Not started", "Queued", "In progress", "Completed", "Skipped"}
    clean_status = status if status in allowed_statuses else "Not started"
    data.setdefault("official_ai_status", {})[resource_id] = clean_status
    data.setdefault("official_ai_notes", {})[resource_id] = note


def official_ai_completed_count(data: Dict[str, Any]) -> int:
    statuses = data.get("official_ai_status", {}) or {}
    return sum(1 for status in statuses.values() if status == "Completed")


def completion_percent(data: Dict[str, Any], total_lessons: int) -> float:
    if total_lessons <= 0:
        return 0.0
    return round(len(data.get("completed_lessons", [])) / total_lessons, 3)


def lessons_remaining(data: Dict[str, Any], total_lessons: int) -> int:
    return max(total_lessons - len(data.get("completed_lessons", [])), 0)


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def update_study_streak(data: Dict[str, Any], session_date: date | None = None) -> None:
    """Update a simple daily streak counter. Multiple sessions on the same day are idempotent."""
    today = session_date or local_today()
    today_text = today.isoformat()
    previous = _parse_date(str(data.get("last_session_date", "")))

    if previous == today:
        data.setdefault("study_streak", 1)
    elif previous == today - timedelta(days=1):
        data["study_streak"] = int(data.get("study_streak", 0) or 0) + 1
    else:
        data["study_streak"] = 1

    data["last_session_date"] = today_text
    data["longest_streak"] = max(
        int(data.get("longest_streak", 0) or 0),
        int(data.get("study_streak", 0) or 0),
    )


def record_daily_mission(
    data: Dict[str, Any],
    day: int,
    status: str = "Completed",
    mood: str = "Good",
    reflection: str = "",
    session_date: date | None = None,
) -> None:
    """Save progress for a 30-minute daily mission."""
    allowed_statuses = {"Not started", "In progress", "Completed", "Skipped"}
    clean_status = status if status in allowed_statuses else "Completed"
    day_key = str(day)
    data.setdefault("daily_missions", {})[day_key] = {
        "day": day,
        "status": clean_status,
        "mood": mood,
        "reflection": reflection,
        "updated_at": _now(),
    }
    data.setdefault("daily_reflections", []).append(
        {
            "day": day,
            "status": clean_status,
            "mood": mood,
            "reflection": reflection[:500],
            "created_at": _now(),
        }
    )
    if clean_status == "Completed":
        update_study_streak(data, session_date=session_date)


def record_daily_checklist(data: Dict[str, Any], day: int, steps: Dict[str, bool] | Iterable[str]) -> None:
    """Persist the tiny-step checklist for today's mission.

    Accepts either a mapping of ``step_id -> done`` or an iterable of checked
    step IDs for backward compatibility with earlier package versions.
    """
    if isinstance(steps, dict):
        clean_steps = {str(step_id)[:80]: bool(done) for step_id, done in steps.items() if str(step_id).strip()}
    else:
        clean_steps = {str(step_id)[:80]: True for step_id in steps if str(step_id).strip()}
    data.setdefault("daily_checklists", {})[str(day)] = {
        "day": int(day),
        "steps": clean_steps,
        "checked_step_ids": [step_id for step_id, done in clean_steps.items() if done],
        "updated_at": _now(),
    }


def record_gym_session(
    data: Dict[str, Any],
    day: int,
    pace: str,
    status: str,
    proof_note: str,
    next_review: str = "",
    minutes: int = 30,
    lesson_id: str = "",
    step_state: Dict[str, bool] | None = None,
) -> None:
    """Persist the daily coding-gym proof card and workout metadata.

    ``step_state=None`` means preserve the previous checklist state. Passing an
    empty dict intentionally clears the saved checklist for that workout. This
    distinction matters for pause/resume because a learner may switch from a
    longer workout to a 10-minute rescue session and save a different set of
    visible blocks.
    """
    allowed_statuses = {"In workout", "Needs proof", "Ready to save", "Saved", "Skipped"}
    clean_status = status if status in allowed_statuses else "Saved"
    day_key = str(day)
    sessions = data.setdefault("gym_sessions", {})
    existing = sessions.get(day_key, {}) if isinstance(sessions.get(day_key, {}), dict) else {}
    try:
        clean_minutes = max(int(minutes or 0), 0)
    except (TypeError, ValueError):
        clean_minutes = 0
    raw_step_state = existing.get("step_state", {}) if step_state is None else step_state
    sessions[day_key] = {
        "day": int(day),
        "pace": str(pace or existing.get("pace") or "30 min daily")[:80],
        "status": clean_status,
        "proof_note": str(proof_note if proof_note is not None else existing.get("proof_note", ""))[:800],
        "next_review": str(next_review if next_review is not None else existing.get("next_review", ""))[:400],
        "minutes": clean_minutes,
        "lesson_id": str(lesson_id or existing.get("lesson_id", ""))[:120],
        "step_state": {str(key)[:80]: bool(value) for key, value in (raw_step_state or {}).items()},
        "created_at": existing.get("created_at") or _now(),
        "updated_at": _now(),
    }


def gym_session_for_day(data: Dict[str, Any], day: int) -> Dict[str, Any]:
    """Return a safe copy of a saved gym session for a specific day."""
    item = (data.get("gym_sessions", {}) or {}).get(str(day), {}) or {}
    return dict(item) if isinstance(item, dict) else {}


def gym_session_is_saved(data: Dict[str, Any], day: int) -> bool:
    item = gym_session_for_day(data, day)
    return item.get("status") == "Saved"


def gym_session_is_active(data: Dict[str, Any], day: int) -> bool:
    item = gym_session_for_day(data, day)
    return item.get("status") in {"In workout", "Needs proof", "Ready to save"}


def start_gym_session(
    data: Dict[str, Any],
    day: int,
    pace: str,
    minutes: int = 30,
    lesson_id: str = "",
    step_state: Dict[str, bool] | None = None,
) -> None:
    """Mark a daily gym session as started so refreshes can resume it."""
    existing = gym_session_for_day(data, day)
    if existing.get("status") == "Saved":
        return
    record_gym_session(
        data,
        day,
        pace=pace or existing.get("pace", "30 min daily"),
        status="In workout",
        proof_note=existing.get("proof_note", ""),
        next_review=existing.get("next_review", ""),
        minutes=minutes,
        lesson_id=lesson_id or existing.get("lesson_id", ""),
        step_state=existing.get("step_state", {}) if step_state is None else step_state,
    )


def pause_gym_session(
    data: Dict[str, Any],
    day: int,
    pace: str,
    minutes: int = 30,
    lesson_id: str = "",
    step_state: Dict[str, bool] | None = None,
    proof_note: str = "",
    next_review: str = "",
) -> None:
    """Save a workout as resumable without requiring a proof card.

    This is the daily-use escape hatch: learners can stop mid-session, close the
    app, and come back to the same pace, selected lesson, checked blocks, proof
    draft, and next-review note.
    """
    existing = gym_session_for_day(data, day)
    record_gym_session(
        data,
        day,
        pace=pace or existing.get("pace", "30 min daily"),
        status="In workout",
        proof_note=proof_note if proof_note is not None else existing.get("proof_note", ""),
        next_review=next_review if next_review is not None else existing.get("next_review", ""),
        minutes=minutes,
        lesson_id=lesson_id or existing.get("lesson_id", ""),
        step_state=existing.get("step_state", {}) if step_state is None else step_state,
    )
    record_daily_checklist(data, day, step_state or {})
    record_daily_mission(data, day, status="In progress", mood="Paused", reflection=str(proof_note or "Paused for later")[:500])


def add_mistake_card(
    data: Dict[str, Any],
    concept: str,
    mistake: str,
    fix: str,
    lesson_id: str = "",
    source: str = "Daily Coding Gym",
) -> bool:
    """Turn a bug, quiz miss, or confusion into a future review card."""
    clean_mistake = str(mistake or "").strip()
    clean_fix = str(fix or "").strip()
    clean_concept = str(concept or "").strip() or "Python review"
    if not clean_mistake and not clean_fix:
        return False
    data.setdefault("mistake_cards", []).append(
        {
            "concept": clean_concept[:120],
            "mistake": clean_mistake[:500],
            "fix": clean_fix[:500],
            "lesson_id": str(lesson_id or "")[:120],
            "source": str(source or "Daily Coding Gym")[:120],
            "status": "Open",
            "created_at": _now(),
        }
    )
    return True


def close_mistake_card(data: Dict[str, Any], index: int) -> bool:
    cards = data.setdefault("mistake_cards", [])
    if index < 0 or index >= len(cards):
        return False
    cards[index]["status"] = "Closed"
    cards[index]["closed_at"] = _now()
    return True


def daily_checklist_steps(data: Dict[str, Any], day: int) -> Dict[str, bool]:
    item = (data.get("daily_checklists", {}) or {}).get(str(day), {}) or {}
    if isinstance(item.get("steps"), dict):
        return {str(step_id): bool(done) for step_id, done in item.get("steps", {}).items()}
    return {str(step_id): True for step_id in item.get("checked_step_ids", []) or []}


def daily_checklist_completion(data: Dict[str, Any], day: int, step_ids: Iterable[str]) -> float:
    ids = [str(step_id) for step_id in step_ids]
    if not ids:
        return 0.0
    saved = daily_checklist_steps(data, day)
    completed = sum(1 for step_id in ids if saved.get(step_id) is True)
    return round(completed / len(ids), 3)


def completed_daily_missions_count(data: Dict[str, Any]) -> int:
    return sum(
        1
        for item in (data.get("daily_missions", {}) or {}).values()
        if item.get("status") == "Completed"
    )


def save_focus_preferences(data: Dict[str, Any], preferences: Dict[str, Any]) -> None:
    """Save learner focus preferences without losing new default keys."""
    current = sanitize_focus_preferences(data.get("focus_preferences", {}))
    for key in DEFAULT_FOCUS_PREFERENCES:
        if key in preferences:
            current[key] = preferences[key]
    data["focus_preferences"] = sanitize_focus_preferences(current)


def record_focus_checkin(
    data: Dict[str, Any],
    energy: str,
    focus_level: str,
    blockers: str = "",
    win: str = "",
    session_date: date | None = None,
) -> None:
    checkin_date = (session_date or local_today()).isoformat()
    data.setdefault("focus_checkins", []).append(
        {
            "energy": energy,
            "focus_level": focus_level,
            "blockers": blockers[:500],
            "win": win[:500],
            "date": checkin_date,
            "created_at": _now(),
        }
    )


def add_parking_lot_item(
    data: Dict[str, Any],
    thought: str,
    lesson_id: str = "",
    source: str = "Today",
) -> bool:
    clean = str(thought or "").strip()
    if not clean:
        return False
    data.setdefault("parking_lot", []).append(
        {
            "thought": clean[:300],
            "lesson_id": lesson_id,
            "source": source,
            "status": "Open",
            "created_at": _now(),
        }
    )
    return True


def close_parking_lot_item(data: Dict[str, Any], index: int) -> bool:
    items = data.setdefault("parking_lot", [])
    if index < 0 or index >= len(items):
        return False
    items[index]["status"] = "Closed"
    items[index]["closed_at"] = _now()
    return True


def record_project_milestone(
    data: Dict[str, Any],
    project_id: str,
    milestone_id: str,
    status: str = "In progress",
    note: str = "",
) -> None:
    allowed_statuses = {"Not started", "In progress", "Completed", "Skipped"}
    clean_status = status if status in allowed_statuses else "In progress"
    project = data.setdefault("project_milestones", {}).setdefault(project_id, {})
    project[milestone_id] = {
        "status": clean_status,
        "note": note[:500],
        "updated_at": _now(),
    }
