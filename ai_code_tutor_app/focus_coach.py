from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FocusBlock:
    label: str
    minutes: int
    instruction: str
    why_it_helps: str


@dataclass(frozen=True)
class FocusMode:
    id: str
    title: str
    minutes: int
    summary: str


FOCUS_MODES: tuple[FocusMode, ...] = (
    FocusMode("rescue_10", "Rescue Mode", 10, "For low-energy days: start tiny, touch code, save a win."),
    FocusMode("standard_30", "Daily 30", 30, "The default habit loop: warm up, sprint, reset, sprint, reflect."),
    FocusMode("deep_45", "Deep Build", 45, "For high-energy days when you want a longer project sprint."),
)

ADHD_DESIGN_PRINCIPLES: tuple[str, ...] = (
    "One visible job at a time; avoid burying the learner in choices.",
    "Tiny starts beat motivation: make the first action smaller than the resistance.",
    "Externalize memory with checklists, notes, proof prompts, and a parking lot.",
    "Use timed sprints plus planned movement breaks to reduce time-blindness.",
    "Reward proof of learning, not endless clicking or leaderboard chasing.",
    "Make resets shame-free: skipped days are data, not failure.",
    "Offer body-double scripts and reflection prompts for accountability without pressure.",
)

ENERGY_LEVELS = ("Low", "Medium", "High")
FOCUS_LEVELS = ("Scattered", "Warming up", "Locked in")


def normalize_energy(energy: str | None) -> str:
    clean = (energy or "Medium").strip().title()
    return clean if clean in ENERGY_LEVELS else "Medium"


def recommended_focus_mode(energy: str | None, available_minutes: int = 30) -> FocusMode:
    """Choose a session shape that protects the habit on low-energy days."""
    clean_energy = normalize_energy(energy)
    if clean_energy == "Low" or available_minutes < 20:
        return FOCUS_MODES[0]
    if clean_energy == "High" and available_minutes >= 45:
        return FOCUS_MODES[2]
    return FOCUS_MODES[1]


def focus_blocks(minutes: int = 30, energy: str | None = "Medium") -> tuple[FocusBlock, ...]:
    """Return an ADHD-friendly coding session broken into short blocks."""
    clean_energy = normalize_energy(energy)
    if minutes <= 10 or clean_energy == "Low":
        return (
            FocusBlock("Open the app", 1, "Open Today's mission and say: I only have to start.", "Removes the blank-page problem."),
            FocusBlock("Pick one tiny target", 2, "Choose one line to read, one quiz question, or one code change.", "Reduces choice overload."),
            FocusBlock("Touch code", 5, "Type, edit, or trace one small thing. Stopping after this still counts.", "Creates momentum before motivation."),
            FocusBlock("Save proof", 2, "Write one note: what changed, what confused me, or what I tried.", "Turns effort into visible progress."),
        )
    if minutes >= 45 and clean_energy == "High":
        return (
            FocusBlock("Brain dump", 5, "Park distractions and pick the one mission for this session.", "Externalizes loose thoughts."),
            FocusBlock("Warm-up recall", 5, "Explain yesterday's idea from memory before reading notes.", "Builds active recall."),
            FocusBlock("Build sprint 1", 15, "Implement or modify one small feature.", "Uses high-energy focus on creation."),
            FocusBlock("Movement reset", 5, "Stand up, stretch, get water, then return to the exact next step.", "Protects attention without derailing."),
            FocusBlock("Build sprint 2", 12, "Add one test, edge case, or clearer variable name.", "Improves quality while the context is fresh."),
            FocusBlock("Ship note", 3, "Record the tiny win and the next obvious step.", "Closes the loop."),
        )
    return (
        FocusBlock("Brain dump", 3, "Write distracting thoughts in the parking lot before starting.", "Keeps side quests visible but out of the way."),
        FocusBlock("Tiny start", 2, "Open the lesson or code and do the smallest possible action.", "Bypasses all-or-nothing thinking."),
        FocusBlock("Sprint 1", 10, "Read, quiz, or code with only one target on screen.", "Fits a realistic attention window."),
        FocusBlock("Reset", 3, "Stand up, breathe, or walk. Do not open a new app.", "Prevents accidental context switching."),
        FocusBlock("Sprint 2", 10, "Practice or test one thing related to the mission.", "Turns learning into action."),
        FocusBlock("Proof", 2, "Save one sentence: I learned, I built, or I noticed.", "Makes progress emotionally real."),
    )


def total_focus_minutes(blocks: Iterable[FocusBlock]) -> int:
    return sum(block.minutes for block in blocks)


def body_double_script(mission_title: str) -> tuple[str, ...]:
    title = mission_title.strip() or "today's coding mission"
    return (
        f"I am doing {title} for one short session.",
        "My only goal is the next tiny action, not finishing everything.",
        "I will keep distracting thoughts in the parking lot instead of chasing them.",
        "When the timer ends, I will save one proof-of-learning note.",
    )


def focus_checkin_score(energy: str | None, focus_level: str | None) -> int:
    """A lightweight score for trends, not judgment."""
    energy_points = {"Low": 1, "Medium": 2, "High": 3}[normalize_energy(energy)]
    clean_focus = (focus_level or "Warming up").strip().title()
    focus_points = {"Scattered": 1, "Warming Up": 2, "Locked In": 3}.get(clean_focus, 2)
    return energy_points + focus_points
