from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


class MissionLike(Protocol):
    day: int
    title: str
    focus: str
    proof: str
    fun_challenge: str


@dataclass(frozen=True)
class CoachStep:
    id: str
    label: str
    minutes: int
    action: str
    proof: str


DEFAULT_DAILY_STEPS: tuple[CoachStep, ...] = (
    CoachStep(
        "open",
        "Open and orient",
        2,
        "Open Today's mission and say out loud what you are doing.",
        "I know today's one job.",
    ),
    CoachStep(
        "brain_dump",
        "Brain dump",
        3,
        "Park distracting thoughts before they become side quests.",
        "One distraction is written down or the parking lot is empty.",
    ),
    CoachStep(
        "learn",
        "Learn one idea",
        10,
        "Read or re-read the lesson section connected to today's mission.",
        "I can explain the idea in one sentence.",
    ),
    CoachStep(
        "practice",
        "Practice one rep",
        10,
        "Do one quiz question, code edit, or challenge attempt before checking answers.",
        "I tried one thing with my own brain first.",
    ),
    CoachStep(
        "check",
        "Check and fix",
        3,
        "Compare your result to a test, hint, or explanation, then fix one mistake.",
        "I know one mistake pattern to watch for.",
    ),
    CoachStep(
        "reflect",
        "Save proof",
        2,
        "Write one sentence about what you learned, built, or noticed.",
        "A note or mission reflection is saved.",
    ),
)

RESCUE_DAILY_STEPS: tuple[CoachStep, ...] = (
    CoachStep("open", "Open the app", 1, "Open the app and do not negotiate with the whole course.", "The app is open."),
    CoachStep("tiny", "Tiny target", 2, "Pick one line, one quiz answer, or one variable name.", "One tiny target exists."),
    CoachStep("touch", "Touch code", 5, "Type, edit, read, or trace one small code idea.", "I touched the material."),
    CoachStep("proof", "Save proof", 2, "Write one note, even if it says what confused you.", "A tiny proof note exists."),
)


def daily_session_checklist(mission: MissionLike, energy: str | None = "Medium") -> tuple[CoachStep, ...]:
    """Return a concrete checklist for today's coding session.

    Low-energy days intentionally shrink the task. The habit is protected even
    when the learner cannot do the full 30-minute version.
    """
    clean_energy = (energy or "Medium").strip().title()
    if clean_energy == "Low":
        return RESCUE_DAILY_STEPS
    return DEFAULT_DAILY_STEPS


def total_step_minutes(steps: Iterable[CoachStep]) -> int:
    return sum(step.minutes for step in steps)


def next_unfinished_step(saved_steps: dict[str, bool], steps: Iterable[CoachStep]) -> CoachStep | None:
    for step in steps:
        if not saved_steps.get(step.id):
            return step
    return None


def daily_session_nudge(saved_steps: dict[str, bool], steps: Iterable[CoachStep]) -> str:
    next_step = next_unfinished_step(saved_steps, steps)
    if next_step is None:
        return "Session checklist complete. Save the mission reflection and stop while the win is visible."
    return f"Next tiny action: {next_step.label.lower()} - {next_step.action}"


def streak_repair_message(streak: int, longest_streak: int) -> str:
    """Return a shame-free message for streaks and missed days."""
    if streak <= 0:
        return "No streak pressure. Start with one tiny proof-of-learning note today."
    if streak == 1 and longest_streak > 1:
        return "You restarted. That counts. The skill is returning, not being perfect."
    if streak < 7:
        return "Protect the habit with today's smallest useful rep."
    return "Strong momentum. Keep it boring, repeatable, and kind."
