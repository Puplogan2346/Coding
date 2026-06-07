from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from daily_coach import CoachStep, next_unfinished_step, total_step_minutes
from study_plan import DAILY_PLAN, next_mission_day


@dataclass(frozen=True)
class SessionChoice:
    label: str
    minutes: int
    energy_override: str | None
    description: str


@dataclass(frozen=True)
class ActionCard:
    headline: str
    instruction: str
    proof: str
    button_label: str
    tone: str = "primary"


@dataclass(frozen=True)
class TimelineDay:
    day: int
    status: str
    label: str


SESSION_CHOICES: tuple[SessionChoice, ...] = (
    SessionChoice(
        "10 min rescue",
        10,
        "Low",
        "Keep the habit alive on low-energy days with one tiny proof of learning.",
    ),
    SessionChoice(
        "30 min daily",
        30,
        None,
        "The normal read-practice-check-reflect session for steady progress.",
    ),
    SessionChoice(
        "45 min deep dive",
        45,
        None,
        "Extra time for project work, review, or finishing a tricky challenge.",
    ),
)


SESSION_LABELS: tuple[str, ...] = tuple(choice.label for choice in SESSION_CHOICES)


def session_choice_by_label(label: str | None) -> SessionChoice:
    for choice in SESSION_CHOICES:
        if choice.label == label:
            return choice
    return SESSION_CHOICES[1]


def session_label_for_minutes(minutes: int | str | None) -> str:
    """Return the closest session label for a saved/default minute value."""
    try:
        clean_minutes = int(minutes)
    except (TypeError, ValueError):
        return SESSION_CHOICES[1].label
    closest = min(SESSION_CHOICES, key=lambda choice: abs(choice.minutes - clean_minutes))
    return closest.label


def session_index_for_minutes(minutes: int | str | None) -> int:
    """Return the UI option index for a saved/default minute value."""
    label = session_label_for_minutes(minutes)
    return SESSION_LABELS.index(label)


def effective_energy_for_session(session_label: str | None, selected_energy: str | None) -> str:
    choice = session_choice_by_label(session_label)
    if choice.energy_override:
        return choice.energy_override
    return (selected_energy or "Medium").strip().title()


def clamp_percent(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def percent_label(value: float) -> str:
    return f"{int(round(clamp_percent(value) * 100))}%"


def today_progress_label(completed_steps: Mapping[str, bool], steps: Iterable[CoachStep]) -> str:
    steps = tuple(steps)
    if not steps:
        return "0 of 0 steps"
    done = sum(1 for step in steps if completed_steps.get(step.id))
    return f"{done} of {len(steps)} steps"


def next_action_card(
    mission_title: str,
    saved_steps: Mapping[str, bool],
    steps: Iterable[CoachStep],
    mission_is_complete: bool = False,
) -> ActionCard:
    steps = tuple(steps)
    next_step = next_unfinished_step(dict(saved_steps), steps)
    if next_step:
        return ActionCard(
            headline=f"Do this now: {next_step.label}",
            instruction=next_step.action,
            proof=next_step.proof,
            button_label="Save checklist after this step",
        )
    if not mission_is_complete:
        return ActionCard(
            headline="Checklist done. Save the mission.",
            instruction=f"Write one sentence about what changed in your brain during '{mission_title}'.",
            proof="Today's reflection is saved.",
            button_label="Save today's mission",
            tone="success",
        )
    return ActionCard(
        headline="You are done for today.",
        instruction="Stop while the win is visible, or do one optional review item if you still have energy.",
        proof="Habit protected without overdoing it.",
        button_label="Come back tomorrow",
        tone="quiet",
    )


def mission_is_complete(progress_data: dict, day: int) -> bool:
    item = (progress_data.get("daily_missions", {}) or {}).get(str(day), {})
    return item.get("status") == "Completed"


def daily_timeline(progress_data: dict, total_days: int = 30) -> list[TimelineDay]:
    current_day = next_mission_day(progress_data)
    missions = progress_data.get("daily_missions", {}) or {}
    days: list[TimelineDay] = []
    for day in range(1, total_days + 1):
        saved = missions.get(str(day), {}) or {}
        saved_status = saved.get("status")
        if saved_status == "Completed":
            status = "complete"
            label = f"Day {day}: complete"
        elif saved_status == "Skipped":
            status = "skipped"
            label = f"Day {day}: skipped"
        elif day == current_day:
            status = "current"
            label = f"Day {day}: current"
        elif day < current_day:
            status = "missed"
            label = f"Day {day}: unfinished"
        else:
            status = "upcoming"
            label = f"Day {day}: upcoming"
        days.append(TimelineDay(day, status, label))
    return days


def streak_microcopy(streak: int, longest_streak: int) -> str:
    if streak <= 0:
        return "No streak yet. One tiny session starts it."
    if streak == 1 and longest_streak > 1:
        return "Restarted. Returning is the real skill."
    if streak < 3:
        return "Momentum is forming. Keep it tiny."
    if streak < 7:
        return "Nice streak. Protect it with a rescue session when needed."
    return "Strong rhythm. Keep the system boring and repeatable."


def mission_stage_cards(mission, saved_steps: Mapping[str, bool], steps: Iterable[CoachStep]) -> tuple[tuple[str, str], ...]:
    steps = tuple(steps)
    next_step = next_unfinished_step(dict(saved_steps), steps)
    now = next_step.action if next_step else "Save your mission reflection."
    next_label = "Then"
    if next_step:
        remaining = [step for step in steps if not saved_steps.get(step.id)]
        if len(remaining) > 1:
            next_text = remaining[1].action
        else:
            next_text = "Write one sentence reflection and stop."
    else:
        next_text = "Stop or do one review item from the queue."
    return (
        ("Now", now),
        (next_label, next_text),
        ("Proof", mission.proof),
    )


def plan_progress_sentence(progress_data: dict) -> str:
    completed = sum(
        1
        for item in (progress_data.get("daily_missions", {}) or {}).values()
        if item.get("status") == "Completed"
    )
    remaining = max(len(DAILY_PLAN) - completed, 0)
    return f"{completed} done, {remaining} left in the 30-day plan."


def session_minutes_total(steps: Iterable[CoachStep]) -> int:
    return total_step_minutes(tuple(steps))


def checklist_completion_from_state(step_state: Mapping[str, bool], steps: Iterable[CoachStep]) -> float:
    steps = tuple(steps)
    if not steps:
        return 0.0
    done = sum(1 for step in steps if step_state.get(step.id))
    return round(done / len(steps), 3)


def pace_label_with_minutes(label: str | None) -> str:
    choice = session_choice_by_label(label)
    return f"{choice.label} ({choice.minutes} min)"


def pace_coach_copy(label: str | None) -> str:
    choice = session_choice_by_label(label)
    if choice.minutes <= 10:
        return "Rescue mode counts. Touch the material, save proof, and leave while it still feels possible."
    if choice.minutes >= 45:
        return "Deep dive mode is for build energy. Keep the target narrow so extra time does not become extra tabs."
    return "Daily mode is the default habit loop: learn one idea, practice one rep, save one proof note."


def merge_step_state(saved_steps: Mapping[str, bool], session_values: Mapping[str, object], day: int, steps: Iterable[CoachStep]) -> dict[str, bool]:
    """Merge saved checklist data with current Streamlit widget values.

    Streamlit reruns immediately when a checkbox changes. Using the current
    session values makes the coach card and nudge feel responsive before the
    learner presses Save checklist.
    """
    merged = {str(key): bool(value) for key, value in dict(saved_steps).items()}
    for step in steps:
        widget_key = f"coach_step_{day}_{step.id}"
        if widget_key in session_values:
            merged[step.id] = bool(session_values[widget_key])
    return merged


def quick_win_message(checklist_completion: float, mission_complete: bool = False) -> str:
    clean = clamp_percent(checklist_completion)
    if mission_complete:
        return "Win saved. Your best next move is stopping or doing one tiny review, not overbuilding."
    if clean <= 0:
        return "Start with the first two-minute action. Opening the app already lowered the wall."
    if clean < 0.34:
        return "You started. Keep the next action smaller than your resistance."
    if clean < 0.67:
        return "Momentum is visible. Finish one more proof step before switching tasks."
    if clean < 1:
        return "Almost there. Save the proof note so your brain can see the win."
    return "Checklist done. Save today’s mission reflection to lock in the streak and XP."


def coach_header_summary(mission_title: str, checklist_completion: float, session_label: str | None, streak: int) -> tuple[str, str, str]:
    """Return dashboard copy for the top coach card."""
    headline = f"Today’s job: {mission_title}"
    subline = quick_win_message(checklist_completion)
    streak_text = streak_microcopy(streak, streak)
    return headline, f"{pace_label_with_minutes(session_label)} — {pace_coach_copy(session_label)}", f"{subline} {streak_text}"


def timeline_legend_counts(days: Iterable[TimelineDay]) -> dict[str, int]:
    counts = {"complete": 0, "current": 0, "upcoming": 0, "skipped": 0, "missed": 0}
    for day in days:
        if day.status in counts:
            counts[day.status] += 1
    return counts
