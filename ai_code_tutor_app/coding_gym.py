from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from daily_coach import next_unfinished_step
from experience import SESSION_LABELS, SessionChoice, session_choice_by_label, session_label_for_minutes


@dataclass(frozen=True)
class GymBlock:
    id: str
    label: str
    minutes: int
    action: str
    proof: str
    why: str


@dataclass(frozen=True)
class GymAction:
    headline: str
    body: str
    proof: str
    stage: str


@dataclass(frozen=True)
class ReviewItem:
    lesson_id: str
    reason: str
    action: str
    intensity: str


@dataclass(frozen=True)
class ProofCard:
    title: str
    summary: str
    next_review: str


@dataclass(frozen=True)
class WorkoutSaveDecision:
    ok: bool
    gym_status: str
    mission_status: str
    message: str


@dataclass(frozen=True)
class GymHistoryItem:
    day: int
    status: str
    pace: str
    minutes: int
    proof_preview: str


@dataclass(frozen=True)
class LessonTimeSuggestion:
    lesson_id: str
    label: str
    reason: str
    priority: int




@dataclass(frozen=True)
class WorkoutResumeSetup:
    pace_label: str
    minutes: int
    locked: bool
    lesson_id: str | None
    status: str
    source: str

@dataclass(frozen=True)
class WorkoutLessonOption:
    lesson_id: str
    label: str
    reason: str
    minutes: int



@dataclass(frozen=True)
class WorkoutResumeSummary:
    day: int
    status: str
    pace: str
    minutes: int
    lesson_id: str
    completion: float
    checked_blocks: int
    total_blocks: int
    proof_preview: str
    next_review: str
    headline: str
    body: str


RESCUE_BLOCKS: tuple[GymBlock, ...] = (
    GymBlock("open", "Show up", 1, "Open the app, breathe once, and name today's mission.", "I showed up.", "Starting is the hard part, so the first rep is intentionally tiny."),
    GymBlock("tiny_rep", "One tiny code rep", 6, "Read, trace, or edit one small piece of Python before looking up the answer.", "I touched one real code idea.", "A short contact point keeps the habit alive without overwhelming you."),
    GymBlock("proof", "Save proof", 3, "Write one sentence: what did I notice, fix, or still not understand?", "One proof sentence exists.", "Proof closes the loop and protects the streak without perfection."),
)

DAILY_BLOCKS: tuple[GymBlock, ...] = (
    GymBlock("warmup", "Warm-up review", 2, "Answer one tiny review question or reread yesterday's proof note.", "One old idea is active again.", "Review before new material helps your brain reconnect the thread quickly."),
    GymBlock("lesson", "Learn one idea", 6, "Read the smallest useful piece of today's lesson and explain it in plain English.", "I can say the idea in one sentence.", "One clear concept beats ten half-open tabs."),
    GymBlock("reps", "Coding reps", 12, "Do one quiz, one code challenge attempt, or one bug fix without copying first.", "I tried a real rep with my own brain.", "Coding sticks when you retrieve, type, test, and fix."),
    GymBlock("ai_prompt", "AI/prompt drill", 5, "Ask for one hint, one test, or one explanation using context and constraints.", "My prompt includes role, task, context, and verification.", "Prompting is a coding skill when it helps you debug instead of outsource thinking."),
    GymBlock("proof", "Proof card", 5, "Save what you learned, one mistake pattern, and the next tiny review target.", "Today's proof card is saved.", "The session is not done until the win is visible."),
)

DEEP_DIVE_BLOCKS: tuple[GymBlock, ...] = (
    GymBlock("warmup", "Warm-up review", 3, "Review one shaky concept and one previous proof note.", "One old idea is warmed up.", "A deep dive still starts small."),
    GymBlock("lesson", "Learn or revisit", 10, "Read the lesson, then write a tiny example from memory.", "One example exists without copy/paste.", "Memory plus typing reveals what is actually understood."),
    GymBlock("project_reps", "Project/code reps", 20, "Work on one project milestone or challenge. Keep the target narrow.", "One tested change or milestone note exists.", "Projects make the skill feel useful, but narrow scope keeps it finishable."),
    GymBlock("debug", "Debug and explain", 7, "Find one bug, test one assumption, or explain one error message.", "One mistake pattern is clearer.", "Debugging is the real coding workout."),
    GymBlock("proof", "Proof card", 5, "Save the result, mistake pattern, and next review target.", "Today's proof card is saved.", "Stopping with a written win prevents unfinished-session fog."),
)


def gym_blocks_for_choice(choice_or_label: SessionChoice | str | None) -> tuple[GymBlock, ...]:
    """Return the workout blocks for rescue, daily, or deep-dive mode."""
    choice = choice_or_label if isinstance(choice_or_label, SessionChoice) else session_choice_by_label(choice_or_label)
    if choice.minutes <= 10:
        return RESCUE_BLOCKS
    if choice.minutes >= 45:
        return DEEP_DIVE_BLOCKS
    return DAILY_BLOCKS


def total_gym_minutes(blocks: Iterable[GymBlock]) -> int:
    return sum(block.minutes for block in blocks)


def _first_incomplete_lesson_id(progress_data: Mapping[str, Any], lesson_ids: Sequence[str]) -> str:
    completed = set(progress_data.get("completed_lessons", []) or [])
    for lesson_id in lesson_ids:
        if lesson_id not in completed:
            return lesson_id
    return lesson_ids[0] if lesson_ids else ""


def lesson_suggestions_for_time(
    progress_data: Mapping[str, Any],
    mission_lesson_id: str | None,
    review_lesson_ids: Sequence[str],
    lesson_ids: Sequence[str],
    minutes: int | str | None,
    limit: int = 5,
) -> list[LessonTimeSuggestion]:
    """Suggest a manageable lesson based on the learner's available time.

    The daily mission remains the default for normal sessions. Rescue sessions
    prefer review/current material so the learner can stop quickly. Deep dives
    include the next incomplete lesson as a stretch option.
    """
    valid_ids = [lesson_id for lesson_id in lesson_ids if lesson_id]
    valid_set = set(valid_ids)
    if not valid_ids:
        return []
    try:
        clean_minutes = int(minutes or 30)
    except (TypeError, ValueError):
        clean_minutes = 30

    completed = [lesson_id for lesson_id in (progress_data.get("completed_lessons", []) or []) if lesson_id in valid_set]
    first_incomplete = _first_incomplete_lesson_id(progress_data, valid_ids)
    suggestions: list[LessonTimeSuggestion] = []
    seen: set[str] = set()

    def add(lesson_id: str | None, label: str, reason: str, priority: int) -> None:
        if lesson_id and lesson_id in valid_set and lesson_id not in seen:
            suggestions.append(LessonTimeSuggestion(lesson_id, label, reason, priority))
            seen.add(lesson_id)

    if clean_minutes <= 10:
        for lesson_id in review_lesson_ids:
            add(lesson_id, "Quick review", "Best fit for a 10-minute rescue session.", 10)
        if completed:
            add(completed[-1], "Recent win review", "Revisit something familiar so stopping is easy.", 20)
        add(mission_lesson_id, "Today's mission", "Use the planned lesson, but only touch one tiny part.", 30)
        add(first_incomplete, "Next small step", "Continue the sequence without opening extra choices.", 40)
    elif clean_minutes >= 45:
        add(mission_lesson_id, "Main lesson", "Use the daily mission as the anchor for your deep dive.", 10)
        add(first_incomplete, "Next incomplete lesson", "Good stretch option when you have project/build energy.", 20)
        for lesson_id in review_lesson_ids:
            add(lesson_id, "Review before build", "Warm up a dependency before project reps.", 30)
        if completed:
            add(completed[-1], "Recent lesson polish", "Use extra time to strengthen a previous lesson.", 40)
    else:
        add(mission_lesson_id, "Recommended daily lesson", "Best fit for the normal 30-minute workout.", 10)
        add(first_incomplete, "Next incomplete lesson", "Keeps the 30-day path moving forward.", 20)
        for lesson_id in review_lesson_ids:
            add(lesson_id, "Short review", "Use this if the planned lesson feels too heavy today.", 30)
        if completed:
            add(completed[-1], "Recent lesson review", "Good if you want a confidence-building session.", 40)

    return sorted(suggestions, key=lambda item: item.priority)[: max(limit, 0)]


def gym_completion(step_state: Mapping[str, bool], blocks: Iterable[GymBlock]) -> float:
    blocks = tuple(blocks)
    if not blocks:
        return 0.0
    done = sum(1 for block in blocks if step_state.get(block.id))
    return round(done / len(blocks), 3)


def gym_progress_label(step_state: Mapping[str, bool], blocks: Iterable[GymBlock]) -> str:
    blocks = tuple(blocks)
    done = sum(1 for block in blocks if step_state.get(block.id))
    return f"{done} of {len(blocks)} blocks"


def next_gym_action(mission_title: str, step_state: Mapping[str, bool], blocks: Sequence[GymBlock], session_saved: bool = False) -> GymAction:
    next_block = next_unfinished_step(dict(step_state), blocks)
    if next_block:
        return GymAction(f"Next rep: {next_block.label}", next_block.action, next_block.proof, "workout")
    if not session_saved:
        return GymAction("Workout complete. Save proof.", f"Write one proof card for '{mission_title}' so today's work becomes visible.", "A proof card is saved.", "proof")
    return GymAction("Workout saved. Stop while it feels good.", "Your next best move is to leave the app with a win, or do one optional review card.", "You protected tomorrow's motivation.", "done")


def gym_motivation_copy(completion: float, choice_label: str | None, session_saved: bool = False) -> str:
    choice = session_choice_by_label(choice_label)
    if session_saved:
        return "Saved. You already did the important part today."
    if completion <= 0:
        if choice.minutes <= 10:
            return "Rescue mode counts. Your only job is to touch code and save proof."
        return "Press Start Today, then only do the first block. No planning required."
    if completion < 0.5:
        return "Momentum is started. Keep the next rep smaller than your resistance."
    if completion < 1:
        return "You are in the workout. Finish one more block, then save proof."
    return "Blocks done. Save the proof card so the session becomes real progress."


def workout_save_decision(completion: float, proof_note: str, mission_status: str | None) -> WorkoutSaveDecision:
    """Validate whether the daily gym can be saved as completed.

    The UI lets learners park an in-progress session, but a completed workout
    needs both finished blocks and at least one proof sentence. This prevents
    accidental empty wins while still supporting ADHD-friendly rescue days.
    """
    clean_status = (mission_status or "Completed").strip()
    if clean_status not in {"Completed", "In progress", "Skipped"}:
        clean_status = "Completed"

    if clean_status == "Skipped":
        return WorkoutSaveDecision(True, "Skipped", "Skipped", "Skipped saved. No shame; restart with rescue mode next time.")

    if clean_status == "In progress":
        return WorkoutSaveDecision(True, "In workout", "In progress", "Workout parked. Resume from the next block when you return.")

    if completion < 1:
        return WorkoutSaveDecision(False, "In workout", "In progress", "Finish each visible block first, or switch to 10 min rescue and complete that smaller workout.")

    if not (proof_note or "").strip():
        return WorkoutSaveDecision(False, "Needs proof", "In progress", "Write one sentence proof before saving as complete.")

    return WorkoutSaveDecision(True, "Saved", "Completed", "Proof saved. Stop while the win is visible.")


def gym_session_history(progress_data: Mapping[str, Any], limit: int = 5) -> list[GymHistoryItem]:
    """Return recent daily gym sessions for a small habit-history panel."""
    raw_sessions = progress_data.get("gym_sessions", {}) if isinstance(progress_data, Mapping) else {}
    if not isinstance(raw_sessions, Mapping):
        return []

    parsed: list[tuple[int, Mapping[str, Any]]] = []
    for day_key, session in raw_sessions.items():
        if not isinstance(session, Mapping):
            continue
        try:
            day = int(day_key)
        except (TypeError, ValueError):
            day = int(session.get("day", 0) or 0)
        if day > 0:
            parsed.append((day, session))

    items: list[GymHistoryItem] = []
    for day, session in sorted(parsed, key=lambda item: item[0], reverse=True)[: max(limit, 0)]:
        try:
            minutes = int(session.get("minutes", 0) or 0)
        except (TypeError, ValueError):
            minutes = 0
        proof = str(session.get("proof_note", "") or "").strip()
        items.append(
            GymHistoryItem(
                day=day,
                status=str(session.get("status", "In workout") or "In workout"),
                pace=str(session.get("pace", "30 min daily") or "30 min daily"),
                minutes=minutes,
                proof_preview=(proof[:90] if proof else "No proof note yet."),
            )
        )
    return items


def gym_history_summary(progress_data: Mapping[str, Any], limit: int = 7) -> str:
    history = gym_session_history(progress_data, limit=limit)
    if not history:
        return "No gym sessions saved yet. Today can be the first proof card."
    saved = sum(1 for item in history if item.status == "Saved")
    parked = sum(1 for item in history if item.status == "In workout")
    skipped = sum(1 for item in history if item.status == "Skipped")
    bits = [f"{saved} saved"]
    if parked:
        bits.append(f"{parked} parked")
    if skipped:
        bits.append(f"{skipped} skipped")
    return ", ".join(bits) + f" in your last {len(history)} gym entries."


def build_review_items(progress_data: dict, lesson_ids: Iterable[str], max_items: int = 3) -> list[ReviewItem]:
    """Build a small review queue from missed quizzes, manual cards, proof notes, and recent lessons."""
    lesson_ids = list(lesson_ids)
    items: list[ReviewItem] = []
    quiz_scores = progress_data.get("quiz_scores", {}) or {}
    for lesson_id in lesson_ids:
        score = quiz_scores.get(lesson_id, {}) or {}
        percent = float(score.get("percent", 100) or 0)
        if lesson_id in quiz_scores and percent < 80:
            items.append(ReviewItem(lesson_id, f"Quiz score {percent:g}%", "Redo one missed idea, then write the correct pattern from memory.", "shaky"))
    mistake_cards = progress_data.get("mistake_cards", []) or []
    for card in mistake_cards:
        lesson_id = card.get("lesson_id") or (lesson_ids[0] if lesson_ids else "")
        if lesson_id in lesson_ids:
            items.append(ReviewItem(lesson_id, f"Mistake card: {card.get('concept', 'review')}", "Read the mistake, cover the fix, and rewrite the correct pattern.", "personal"))

    for session in gym_session_history(progress_data, limit=5):
        raw_session = (progress_data.get("gym_sessions", {}) or {}).get(str(session.day), {}) or {}
        lesson_id = raw_session.get("lesson_id") or (lesson_ids[0] if lesson_ids else "")
        next_review = str(raw_session.get("next_review", "") or "").strip()
        if lesson_id in lesson_ids and next_review:
            items.append(ReviewItem(lesson_id, f"Proof card review: {next_review[:80]}", "Do one tiny rep connected to your saved next-review note.", "planned"))

    completed = progress_data.get("completed_lessons", []) or []
    for lesson_id in reversed(completed[-3:]):
        if lesson_id in lesson_ids:
            items.append(ReviewItem(lesson_id, "Recent lesson", "Explain the lesson in one sentence before starting new work.", "warmup"))

    deduped: list[ReviewItem] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        key = (item.lesson_id, item.reason)
        if key not in seen:
            deduped.append(item)
            seen.add(key)
        if len(deduped) >= max_items:
            break
    return deduped


def workout_resume_summary(progress_data: Mapping[str, Any], day: int) -> WorkoutResumeSummary | None:
    """Summarize an in-progress workout so the UI can make resume state obvious.

    This helper is intentionally read-only. The app uses it to reassure the
    learner that Stop & save for later actually persisted the selected pace,
    lesson, checklist, proof draft, and next-review note.
    """
    sessions = progress_data.get("gym_sessions", {}) if isinstance(progress_data, Mapping) else {}
    if not isinstance(sessions, Mapping):
        return None
    raw = sessions.get(str(day), {}) or {}
    if not isinstance(raw, Mapping):
        return None
    status = str(raw.get("status", "") or "")
    if status not in {"In workout", "Needs proof", "Ready to save"}:
        return None

    setup = workout_resume_setup(raw, raw.get("minutes", 30), ())
    pace = setup.pace_label
    blocks = gym_blocks_for_choice(pace)
    step_state = {str(key): bool(value) for key, value in (raw.get("step_state", {}) or {}).items()}
    completion = gym_completion(step_state, blocks)
    checked = sum(1 for block in blocks if step_state.get(block.id))
    total = len(blocks)
    try:
        minutes = int(raw.get("minutes", total_gym_minutes(blocks)) or total_gym_minutes(blocks))
    except (TypeError, ValueError):
        minutes = total_gym_minutes(blocks)
    proof = str(raw.get("proof_note", "") or "").strip()
    next_review = str(raw.get("next_review", "") or "").strip()
    if checked <= 0:
        headline = "Resume saved workout"
        body = "You stopped before finishing the first block. Start with the first tiny rep."
    elif completion < 1:
        headline = f"Resume where you stopped: {checked}/{total} blocks done"
        body = "Your pace, lesson, checked blocks, proof draft, and review note are saved."
    elif not proof:
        headline = "Workout blocks done. Add proof to finish."
        body = "Your checklist is complete; write one proof sentence before saving the workout."
    else:
        headline = "Workout ready to save"
        body = "Your blocks and proof are waiting. Save the proof card when you are ready."
    return WorkoutResumeSummary(
        day=int(day),
        status=status,
        pace=pace,
        minutes=max(minutes, 0),
        lesson_id=str(raw.get("lesson_id", "") or ""),
        completion=completion,
        checked_blocks=checked,
        total_blocks=total,
        proof_preview=(proof[:120] if proof else "No proof draft yet."),
        next_review=(next_review[:120] if next_review else "No next-review note yet."),
        headline=headline,
        body=body,
    )


def workout_resume_setup(
    existing_session: Mapping[str, Any] | None,
    preferred_minutes: int | str | None,
    valid_lesson_ids: Sequence[str],
) -> WorkoutResumeSetup:
    """Resolve the workout pace/lesson for Today in a resume-safe way.

    If a learner already started or saved today's workout, the UI should lock
    the workout length and lesson so their checklist, proof draft, and saved
    block IDs still match when they return later. Older progress files may have
    a missing/invalid pace label, so this also recovers the pace from the saved
    minute value.
    """
    session = existing_session if isinstance(existing_session, Mapping) else {}
    status = str(session.get("status", "") or "")
    locked = status in {"In workout", "Needs proof", "Ready to save", "Saved"}
    source = "preference"

    if locked:
        raw_pace = str(session.get("pace", "") or "")
        if raw_pace in SESSION_LABELS:
            pace_label = raw_pace
            source = "saved_pace"
        else:
            pace_label = session_label_for_minutes(session.get("minutes"))
            source = "saved_minutes"
    else:
        pace_label = session_label_for_minutes(preferred_minutes)

    choice = session_choice_by_label(pace_label)
    valid_set = set(valid_lesson_ids or ())
    raw_lesson_id = str(session.get("lesson_id", "") or "")
    lesson_id = raw_lesson_id if locked and raw_lesson_id in valid_set else None

    return WorkoutResumeSetup(
        pace_label=choice.label,
        minutes=choice.minutes,
        locked=locked,
        lesson_id=lesson_id,
        status=status,
        source=source,
    )


def workout_lesson_options(
    progress_data: Mapping[str, Any],
    lessons: Sequence[Any],
    mission: Any,
    minutes: int,
    review_lesson_ids: Sequence[str] | None = None,
    current_lesson_id: str | None = None,
    max_options: int = 6,
) -> list[WorkoutLessonOption]:
    """Return lesson choices that match the time available for today's workout.

    The Daily Coding Gym should not make a tired learner decide from the full
    curriculum. This helper narrows the choices based on session length:
    rescue sessions bias toward review/touching code, daily sessions bias
    toward today's mission, and deep dives include stretch/project-ready work.
    """
    lesson_map = {str(getattr(lesson, "id", "")): lesson for lesson in lessons if getattr(lesson, "id", "")}
    if not lesson_map:
        return []

    completed = [lesson_id for lesson_id in progress_data.get("completed_lessons", []) or [] if lesson_id in lesson_map]
    incomplete = [lesson_id for lesson_id in lesson_map if lesson_id not in set(completed)]
    next_incomplete = incomplete[0] if incomplete else (list(lesson_map)[-1])
    mission_lesson_id = getattr(mission, "lesson_id", None)
    review_ids = [lesson_id for lesson_id in (review_lesson_ids or ()) if lesson_id in lesson_map]

    options: list[WorkoutLessonOption] = []
    seen: set[str] = set()

    def add(lesson_id: str | None, reason: str) -> None:
        if not lesson_id or lesson_id not in lesson_map or lesson_id in seen:
            return
        lesson = lesson_map[lesson_id]
        title = str(getattr(lesson, "title", lesson_id))
        options.append(WorkoutLessonOption(lesson_id, f"{title} — {reason}", reason, int(minutes)))
        seen.add(lesson_id)

    if current_lesson_id:
        add(current_lesson_id, "resume saved workout")

    clean_minutes = int(minutes or 30)
    if clean_minutes <= 10:
        for lesson_id in review_ids:
            add(lesson_id, "10 min rescue review")
        if completed:
            add(completed[-1], "10 min rescue review")
        add(mission_lesson_id, "touch today’s lesson")
        add(next_incomplete, "tiny next step")
    elif clean_minutes >= 45:
        add(mission_lesson_id, "today’s full lesson")
        add(next_incomplete, "next incomplete lesson")
        for lesson_id in review_ids:
            add(lesson_id, "warm-up review")
        start_index = list(lesson_map).index(next_incomplete) if next_incomplete in lesson_map else 0
        for lesson_id in list(lesson_map)[start_index + 1 : start_index + 3]:
            add(lesson_id, "deep-dive stretch")
    else:
        add(mission_lesson_id, "today’s plan")
        add(next_incomplete, "next incomplete lesson")
        for lesson_id in review_ids:
            add(lesson_id, "warm-up review")
        if completed:
            add(completed[-1], "quick confidence review")

    add(next_incomplete, "safe fallback")
    return options[: max(1, int(max_options or 1))]


def proof_card_summary(day: int, mission_title: str, proof_note: str, next_review: str = "") -> ProofCard:
    clean_note = (proof_note or "").strip()
    summary = clean_note if clean_note else "I showed up and touched code today."
    clean_review = (next_review or "").strip() or "Review today's smallest shaky idea tomorrow."
    return ProofCard(f"Day {day} proof: {mission_title}", summary[:240], clean_review[:180])


def workout_finish_status(completion: float, proof_note: str, session_saved: bool = False) -> tuple[str, str]:
    if session_saved:
        return "Saved", "Daily coding gym complete. Done is better than more."
    if completion < 1:
        return "In workout", "Finish the next block or switch to rescue mode."
    if not (proof_note or "").strip():
        return "Needs proof", "Write one sentence proof to close the session."
    return "Ready to save", "Save the proof card and stop."
