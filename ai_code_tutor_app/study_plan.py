from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class TimeBlock:
    label: str
    minutes: int
    instruction: str


@dataclass(frozen=True)
class DailyMission:
    day: int
    title: str
    focus: str
    lesson_id: str | None
    blocks: tuple[TimeBlock, ...]
    fun_challenge: str
    proof: str
    review_lesson_ids: tuple[str, ...] = ()
    official_resource_ids: tuple[str, ...] = ()

    @property
    def total_minutes(self) -> int:
        return sum(block.minutes for block in self.blocks)


DEFAULT_BLOCKS = (
    TimeBlock("Warm up", 5, "Recall yesterday's key idea before reading anything."),
    TimeBlock("Learn", 10, "Read the lesson or inspect the worked example."),
    TimeBlock("Practice", 10, "Write or modify code. Small experiments count."),
    TimeBlock("Reflect", 5, "Write one note, one question, and one tiny win."),
)

BUILD_BLOCKS = (
    TimeBlock("Warm up", 5, "Rewrite one idea from memory."),
    TimeBlock("Build", 15, "Make a tiny feature, script, or improvement."),
    TimeBlock("Test", 5, "Run, inspect, or mentally trace one test case."),
    TimeBlock("Reflect", 5, "Record what worked and what broke."),
)

REVIEW_BLOCKS = (
    TimeBlock("Recall", 8, "Answer a quiz or explain a concept without notes."),
    TimeBlock("Repair", 7, "Review only the part you missed."),
    TimeBlock("Practice", 10, "Do a short coding repetition."),
    TimeBlock("Reflect", 5, "Write the mistake pattern you want to catch next time."),
)

DAILY_PLAN: tuple[DailyMission, ...] = (
    DailyMission(1, "Start Python without fear", "New lesson", "01-python-mindset", DEFAULT_BLOCKS, "Change a print message three times and predict the output first.", "You can explain what print does and how to read a simple error."),
    DailyMission(2, "Variables are labels", "New lesson", "02-variables-types", DEFAULT_BLOCKS, "Make three variables about a favorite meal, game, song, or hobby.", "You can tell the difference between a string, number, and boolean."),
    DailyMission(3, "First review plus tiny decisions", "Review", "03-conditionals", REVIEW_BLOCKS, "Write a tiny age, score, or weather decision.", "You can explain why if, elif, and else run in order.", ("01-python-mindset", "02-variables-types")),
    DailyMission(4, "Make choices in code", "New lesson", "03-conditionals", DEFAULT_BLOCKS, "Build a mood-to-message function with at least three branches.", "You can use comparisons and indentation correctly."),
    DailyMission(5, "Repeat work with loops", "New lesson", "04-loops", DEFAULT_BLOCKS, "Print a countdown, then change it into a list of hype messages.", "You can explain when to use a for loop."),
    DailyMission(6, "Mini game day", "Build", "04-loops", BUILD_BLOCKS, "Make a tiny guessing-game outline using variables and if statements.", "You can combine variables, decisions, and loops in one small idea.", ("02-variables-types", "03-conditionals")),
    DailyMission(7, "Week 1 checkpoint", "Review", "04-loops", REVIEW_BLOCKS, "Teach a rubber duck how your best loop works.", "You can solve one challenge from starter code without checking the solution first.", ("01-python-mindset", "02-variables-types", "03-conditionals", "04-loops")),
    DailyMission(8, "Functions make reusable moves", "New lesson", "05-functions", DEFAULT_BLOCKS, "Turn one repeated idea into a function named with a verb.", "You can describe parameters and return values."),
    DailyMission(9, "Function reps", "Practice", "05-functions", BUILD_BLOCKS, "Create three tiny helper functions for a pretend app.", "You can call your function with different inputs and predict results.", ("03-conditionals", "04-loops")),
    DailyMission(10, "Lists and dictionaries", "New lesson", "06-data-structures", DEFAULT_BLOCKS, "Make a list of favorites and a dictionary profile for yourself or a character.", "You can choose between list and dictionary for simple data."),
    DailyMission(11, "Data structure reps", "Practice", "06-data-structures", BUILD_BLOCKS, "Loop over a list of snacks, songs, workouts, or quests and format each one.", "You can access, update, and loop through stored data.", ("04-loops", "05-functions")),
    DailyMission(12, "Debug like a detective", "New lesson", "07-debugging-tests", DEFAULT_BLOCKS, "Create one intentional bug, read the error, then fix it.", "You can name the error type and the line to inspect first."),
    DailyMission(13, "Testing is a superpower", "Practice", "07-debugging-tests", BUILD_BLOCKS, "Write one assert for a function you already made.", "You can explain how a test proves expected behavior.", ("05-functions", "06-data-structures")),
    DailyMission(14, "Week 2 build checkpoint", "Build", "07-debugging-tests", BUILD_BLOCKS, "Improve a previous challenge by adding one edge case.", "You can run through a read-practice-test-reflect loop.", ("01-python-mindset", "05-functions", "06-data-structures", "07-debugging-tests")),
    DailyMission(15, "Files and JSON", "New lesson", "08-files-json-apis", DEFAULT_BLOCKS, "Sketch a tiny habit tracker that could save data as JSON.", "You can explain why apps save structured data."),
    DailyMission(16, "JSON mini-tool", "Build", "08-files-json-apis", BUILD_BLOCKS, "Create a dictionary and convert it to a JSON-looking string in your notes.", "You can identify keys, values, and nested data.", ("06-data-structures", "07-debugging-tests")),
    DailyMission(17, "APIs without overwhelm", "Practice", "08-files-json-apis", DEFAULT_BLOCKS, "Write a pretend API response and pull one value out of it.", "You can describe request, response, and JSON in plain English."),
    DailyMission(18, "Classes and objects", "New lesson", "09-oop", DEFAULT_BLOCKS, "Invent a Pet, Player, Plant, or Playlist object with two attributes.", "You can explain object, class, attribute, and method."),
    DailyMission(19, "Object practice", "Practice", "09-oop", BUILD_BLOCKS, "Add one method to your object that returns a friendly sentence.", "You can create an instance and call a method.", ("05-functions", "06-data-structures", "09-oop")),
    DailyMission(20, "Prompt engineering for learning", "New lesson", "10-ai-prompting", DEFAULT_BLOCKS, "Rewrite a weak prompt into the Prompt Lab formula.", "You can include task, context, constraints, format, and verification."),
    DailyMission(21, "AI debugging partner", "Practice", "10-ai-prompting", BUILD_BLOCKS, "Write a prompt that asks for a hint, not the answer.", "You can use AI to learn without skipping the thinking step.", ("07-debugging-tests", "10-ai-prompting"), ("openai_prompting_guide",)),
    DailyMission(22, "Mini project part 1", "Build", "11-mini-projects", BUILD_BLOCKS, "Design the inputs and outputs for a quiz scorer.", "You can break a project into small functions."),
    DailyMission(23, "Mini project part 2", "Build", "11-mini-projects", BUILD_BLOCKS, "Add one feature to the quiz scorer idea: percent, grade, or feedback.", "You can explain your project flow from input to output.", ("05-functions", "06-data-structures", "07-debugging-tests")),
    DailyMission(24, "Refactor and test", "Review", "11-mini-projects", REVIEW_BLOCKS, "Make one function name clearer and add one test idea.", "You can improve code without changing what it does.", ("08-files-json-apis", "09-oop", "11-mini-projects")),
    DailyMission(25, "Streamlit app basics", "New lesson", "12-ai-apps-streamlit", DEFAULT_BLOCKS, "Sketch one screen for an app you would actually use.", "You can name the parts of a simple Streamlit app."),
    DailyMission(26, "AI app design", "Build", "12-ai-apps-streamlit", BUILD_BLOCKS, "Write a one-screen app spec: user, input, output, risk, test.", "You can describe what AI should and should not do in your app.", ("10-ai-prompting", "12-ai-apps-streamlit")),
    DailyMission(27, "Official AI resource day", "External track", "10-ai-prompting", DEFAULT_BLOCKS, "Queue one Gumloop or Claude resource and write why it matters.", "You can connect Python learning with official AI learning paths.", ("10-ai-prompting",), ("gumloop_ai_fundamentals", "anthropic_academy")),
    DailyMission(28, "Capstone plan", "Build", "12-ai-apps-streamlit", BUILD_BLOCKS, "Choose a tiny capstone: quiz, habit tracker, prompt coach, or automation planner.", "You can write a 5-step build plan."),
    DailyMission(29, "Capstone build sprint", "Build", "12-ai-apps-streamlit", BUILD_BLOCKS, "Build or pseudocode the smallest useful version of your capstone.", "You can show a working or well-tested tiny feature.", ("05-functions", "07-debugging-tests", "12-ai-apps-streamlit")),
    DailyMission(30, "Demo day and next path", "Review", "12-ai-apps-streamlit", REVIEW_BLOCKS, "Record a 60-second demo script for what you learned and what you will build next.", "You can explain your code journey and pick the next official AI step.", ("01-python-mindset", "06-data-structures", "10-ai-prompting", "12-ai-apps-streamlit"), ("gumloop_getting_started", "openai_academy")),
)


def mission_by_day(day: int) -> DailyMission:
    if day < 1 or day > len(DAILY_PLAN):
        raise ValueError(f"day must be between 1 and {len(DAILY_PLAN)}")
    return DAILY_PLAN[day - 1]


def completed_mission_days(progress_data: dict) -> set[int]:
    completed: set[int] = set()
    for key, item in (progress_data.get("daily_missions", {}) or {}).items():
        try:
            day = int(key)
        except (TypeError, ValueError):
            continue
        if item.get("status") == "Completed":
            completed.add(day)
    return completed


def resolved_mission_days(progress_data: dict) -> set[int]:
    resolved: set[int] = set()
    for key, item in (progress_data.get("daily_missions", {}) or {}).items():
        try:
            day = int(key)
        except (TypeError, ValueError):
            continue
        if item.get("status") in {"Completed", "Skipped"}:
            resolved.add(day)
    return resolved


def next_mission_day(progress_data: dict) -> int:
    resolved = resolved_mission_days(progress_data)
    for day in range(1, len(DAILY_PLAN) + 1):
        if day not in resolved:
            return day
    return len(DAILY_PLAN)


def next_mission(progress_data: dict) -> DailyMission:
    return mission_by_day(next_mission_day(progress_data))


def plan_completion_percent(progress_data: dict) -> float:
    return round(len(completed_mission_days(progress_data)) / len(DAILY_PLAN), 3)


def review_queue(progress_data: dict, fallback_lesson_ids: Sequence[str], limit: int = 3) -> list[str]:
    """Return lesson IDs worth reviewing today.

    The mission's explicit review list comes first. If that is empty, use the
    most recently completed lessons so a new learner always has something useful
    to revisit.
    """
    mission = next_mission(progress_data)
    queue = list(mission.review_lesson_ids)
    completed_lessons = list(progress_data.get("completed_lessons", []) or [])
    for lesson_id in reversed(completed_lessons):
        if lesson_id not in queue:
            queue.append(lesson_id)
    for lesson_id in fallback_lesson_ids:
        if lesson_id not in queue:
            queue.append(lesson_id)
    return queue[:limit]


def total_plan_minutes(plan: Iterable[DailyMission] = DAILY_PLAN) -> int:
    return sum(mission.total_minutes for mission in plan)
