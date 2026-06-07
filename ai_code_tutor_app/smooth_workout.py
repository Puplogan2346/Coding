from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class FocusWorkoutCard:
    """The single next rep the learner should see in the daily coding gym."""

    block_id: str
    label: str
    minutes: int
    action: str
    proof: str
    why: str
    step_number: int
    total_steps: int
    completion: float
    is_complete: bool
    headline: str
    nudge: str


@dataclass(frozen=True)
class SmoothnessCheck:
    name: str
    status: str
    detail: str


@dataclass(frozen=True)
class ResumeSafetyReport:
    can_resume: bool
    saved_pace: str
    saved_lesson_id: str
    saved_blocks: int
    proof_saved: bool
    detail: str


def _blocks_tuple(blocks: Iterable[Any]) -> tuple[Any, ...]:
    return tuple(blocks or ())


def clean_step_state(step_state: Mapping[str, Any] | None, blocks: Iterable[Any]) -> dict[str, bool]:
    """Return only step IDs that exist in the current workout blocks."""
    raw = step_state if isinstance(step_state, Mapping) else {}
    allowed = {str(getattr(block, "id", "")) for block in _blocks_tuple(blocks)}
    return {str(key): bool(value) for key, value in raw.items() if str(key) in allowed}


def current_focus_card(step_state: Mapping[str, Any] | None, blocks: Iterable[Any], session_saved: bool = False) -> FocusWorkoutCard:
    """Return the next visible workout block for a low-decision focus mode.

    If every block is already checked, the proof-card step becomes the active
    card so the learner sees exactly what to do to finish.
    """
    clean_blocks = _blocks_tuple(blocks)
    total = len(clean_blocks)
    if total <= 0:
        return FocusWorkoutCard(
            block_id="done",
            label="No blocks",
            minutes=0,
            action="There is no workout block to show.",
            proof="Nothing to save.",
            why="The workout plan is empty.",
            step_number=0,
            total_steps=0,
            completion=0.0,
            is_complete=True,
            headline="No workout loaded",
            nudge="Pick a session length and start again.",
        )

    clean_steps = clean_step_state(step_state, clean_blocks)
    completed = sum(1 for block in clean_blocks if clean_steps.get(str(getattr(block, "id", ""))))
    completion = round(completed / total, 3)
    if session_saved:
        return FocusWorkoutCard(
            block_id="done",
            label="Saved",
            minutes=0,
            action="Today is already saved. You can stop or do an optional tiny review.",
            proof="Daily proof card is saved.",
            why="Stopping after a complete session protects the habit.",
            step_number=total,
            total_steps=total,
            completion=1.0,
            is_complete=True,
            headline="Workout saved — stop here if you want",
            nudge="Done is better than more. A short review is optional, not required.",
        )

    for index, block in enumerate(clean_blocks, start=1):
        block_id = str(getattr(block, "id", ""))
        if not clean_steps.get(block_id):
            return FocusWorkoutCard(
                block_id=block_id,
                label=str(getattr(block, "label", "Workout rep")),
                minutes=int(getattr(block, "minutes", 0) or 0),
                action=str(getattr(block, "action", "Do the next tiny rep.")),
                proof=str(getattr(block, "proof", "Save one sentence of proof.")),
                why=str(getattr(block, "why", "This keeps the session small and finishable.")),
                step_number=index,
                total_steps=total,
                completion=completion,
                is_complete=False,
                headline=f"Step {index} of {total}: {getattr(block, 'label', 'Workout rep')}",
                nudge="Do only this rep. Then save or move to the next rep.",
            )

    final_block = clean_blocks[-1]
    return FocusWorkoutCard(
        block_id=str(getattr(final_block, "id", "proof")),
        label="Proof card",
        minutes=int(getattr(final_block, "minutes", 0) or 0),
        action="All workout reps are checked. Write one proof sentence and save the proof card.",
        proof="One sentence saying what you learned, fixed, or still need to review.",
        why="The proof card turns a session into visible learning evidence.",
        step_number=total,
        total_steps=total,
        completion=1.0,
        is_complete=True,
        headline="All reps done — save proof",
        nudge="Do not add extra work. Save the proof card and stop.",
    )


def mark_focus_step_done(step_state: Mapping[str, Any] | None, blocks: Iterable[Any]) -> dict[str, bool]:
    """Return a new step state with the current focus card marked done."""
    clean_blocks = _blocks_tuple(blocks)
    state = clean_step_state(step_state, clean_blocks)
    card = current_focus_card(state, clean_blocks)
    if card.block_id and card.block_id != "done":
        state[card.block_id] = True
    return state


def focus_completion_sentence(card: FocusWorkoutCard) -> str:
    if card.total_steps <= 0:
        return "No workout loaded."
    if card.completion >= 1:
        return "All workout reps are done. Save proof to finish."
    return f"{card.step_number - 1} of {card.total_steps} reps done. Next: {card.label}."


def resume_safety_report(session: Mapping[str, Any] | None, blocks: Iterable[Any]) -> ResumeSafetyReport:
    raw = session if isinstance(session, Mapping) else {}
    clean_blocks = _blocks_tuple(blocks)
    state = clean_step_state(raw.get("step_state", {}), clean_blocks)
    saved_blocks = sum(1 for block in clean_blocks if state.get(str(getattr(block, "id", ""))))
    status = str(raw.get("status", "") or "")
    can_resume = status in {"In workout", "Needs proof", "Ready to save"}
    proof = str(raw.get("proof_note", "") or "").strip()
    pace = str(raw.get("pace", "") or "")
    lesson_id = str(raw.get("lesson_id", "") or "")
    if can_resume:
        detail = "Resume-safe: pace, lesson, checked reps, proof draft, and review note were found."
    elif status == "Saved":
        detail = "Already saved. No resume needed."
    else:
        detail = "No active saved workout found."
    return ResumeSafetyReport(
        can_resume=can_resume,
        saved_pace=pace,
        saved_lesson_id=lesson_id,
        saved_blocks=saved_blocks,
        proof_saved=bool(proof),
        detail=detail,
    )


def daily_use_smoothness_checks(
    progress_data: Mapping[str, Any],
    day: int,
    blocks: Sequence[Any],
    preferred_minutes: int,
) -> list[SmoothnessCheck]:
    """Small private QA checklist for daily-use readiness."""
    session = ((progress_data.get("gym_sessions", {}) or {}).get(str(day), {}) or {}) if isinstance(progress_data, Mapping) else {}
    focus_preferences = progress_data.get("focus_preferences", {}) if isinstance(progress_data, Mapping) else {}
    default_minutes = focus_preferences.get("default_minutes") if isinstance(focus_preferences, Mapping) else None
    checks: list[SmoothnessCheck] = []
    checks.append(
        SmoothnessCheck(
            "Default workout length",
            "Pass" if int(default_minutes or preferred_minutes or 30) in {10, 30, 45} else "Warning",
            f"Current default: {default_minutes or preferred_minutes or 30} minutes.",
        )
    )
    report = resume_safety_report(session, blocks)
    checks.append(
        SmoothnessCheck(
            "Stop/resume state",
            "Pass" if report.can_resume or str(session.get("status", "")) in {"", "Saved"} else "Warning",
            report.detail,
        )
    )
    checks.append(
        SmoothnessCheck(
            "One-step focus mode",
            "Pass" if len(blocks) > 0 else "Warning",
            "The Today screen can show one current rep instead of forcing checklist scanning.",
        )
    )
    checks.append(
        SmoothnessCheck(
            "Proof habit",
            "Pass" if str(session.get("proof_note", "") or "").strip() or str(session.get("status", "")) != "Saved" else "Warning",
            "Saved sessions should have a proof sentence so learning progress is visible.",
        )
    )
    return checks
