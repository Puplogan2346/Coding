from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from curriculum import LESSONS


def first_incomplete_lesson_id(progress_data: dict) -> str:
    """Return the first lesson the learner has not yet completed.

    Falls back to the final lesson once everything is done. Lives here in the
    learning-progression module so both ``app.py`` and per-tab modules can share
    it without importing each other.
    """
    completed = set(progress_data.get("completed_lessons", []))
    for lesson_item in LESSONS:
        if lesson_item.id not in completed:
            return lesson_item.id
    return LESSONS[-1].id


GRADUATION_PROMISE = (
    "By the end, you should be able to read beginner Python, write small scripts, "
    "use variables, conditionals, loops, functions, lists, dictionaries, files, JSON, "
    "basic tests, simple classes, and use AI as a learning partner without skipping understanding."
)


@dataclass(frozen=True)
class SkillOutcome:
    id: str
    title: str
    description: str
    lesson_ids: tuple[str, ...]
    practice_goal: str
    proof_prompt: str


@dataclass(frozen=True)
class SkillStatus:
    skill: SkillOutcome
    completed_lessons: int
    total_lessons: int
    percent: float
    status: str
    next_lesson_id: str | None




@dataclass(frozen=True)
class LearningMilestone:
    id: str
    title: str
    goal: str
    day_range: tuple[int, int]
    lesson_ids: tuple[str, ...]
    proof: str
    project_ids: tuple[str, ...] = ()
    required_saved_workouts: int = 0
    required_quiz_passes: int = 0
    required_project_milestones: int = 0


@dataclass(frozen=True)
class MilestoneStatus:
    milestone: LearningMilestone
    percent: float
    status: str
    completed_requirements: int
    total_requirements: int
    next_action: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class GraduationRequirement:
    id: str
    title: str
    target: int
    current: int
    proof: str

    @property
    def complete(self) -> bool:
        return self.current >= self.target

    @property
    def percent(self) -> float:
        if self.target <= 0:
            return 1.0
        return round(min(self.current / self.target, 1.0), 3)


@dataclass(frozen=True)
class GraduationReadiness:
    percent: float
    status: str
    requirements: tuple[GraduationRequirement, ...]
    summary: str
    next_action: str


MILESTONES: tuple[LearningMilestone, ...] = (
    LearningMilestone(
        id="m1-python-start",
        title="Milestone 1 - Python starting line",
        goal="Read simple Python, run tiny changes, and treat errors as clues.",
        day_range=(1, 3),
        lesson_ids=("01-python-mindset", "02-variables-types", "03-conditionals"),
        proof="You can explain print, variables, basic types, and one if/else decision in plain English.",
        required_saved_workouts=2,
        required_quiz_passes=2,
    ),
    LearningMilestone(
        id="m2-control-flow",
        title="Milestone 2 - Control flow and functions",
        goal="Make code choose, repeat, and reuse steps.",
        day_range=(4, 9),
        lesson_ids=("03-conditionals", "04-loops", "05-functions"),
        proof="You can write a small function that uses a condition or loop and returns a value.",
        project_ids=("quiz_scorekeeper",),
        required_saved_workouts=4,
        required_quiz_passes=3,
        required_project_milestones=1,
    ),
    LearningMilestone(
        id="m3-data-debugging",
        title="Milestone 3 - Data, debugging, and tests",
        goal="Store information, inspect bugs, and prove code works with tests.",
        day_range=(10, 14),
        lesson_ids=("06-data-structures", "07-debugging-tests"),
        proof="You can choose between a list and dictionary, read an error, and write one assert.",
        project_ids=("quiz_scorekeeper", "habit_tracker_json"),
        required_saved_workouts=4,
        required_quiz_passes=2,
        required_project_milestones=2,
    ),
    LearningMilestone(
        id="m4-real-world-python",
        title="Milestone 4 - Real-world Python shapes",
        goal="Understand saved data, JSON/API shapes, and object thinking.",
        day_range=(15, 19),
        lesson_ids=("08-files-json-apis", "09-oop"),
        proof="You can sketch structured data, explain request/response, and describe a simple class/object.",
        project_ids=("habit_tracker_json",),
        required_saved_workouts=3,
        required_quiz_passes=2,
        required_project_milestones=2,
    ),
    LearningMilestone(
        id="m5-ai-assisted-coding",
        title="Milestone 5 - AI-assisted coding habits",
        goal="Use AI for hints, tests, debugging, and planning without skipping your own thinking.",
        day_range=(20, 27),
        lesson_ids=("10-ai-prompting", "11-mini-projects", "12-ai-apps-streamlit"),
        proof="You can write a useful coding prompt with task, context, constraints, format, and verification.",
        project_ids=("prompt_coach", "gumloop_workflow_planner"),
        required_saved_workouts=4,
        required_quiz_passes=2,
        required_project_milestones=2,
    ),
    LearningMilestone(
        id="m6-capstone-graduation",
        title="Milestone 6 - Capstone graduation",
        goal="Build or clearly prototype a small Python/AI learning app feature and explain what it does.",
        day_range=(28, 30),
        lesson_ids=("11-mini-projects", "12-ai-apps-streamlit"),
        proof="You have a demo note, a test/checklist, and a next-step plan for a small capstone.",
        project_ids=("personal_ai_code_tutor",),
        required_saved_workouts=2,
        required_quiz_passes=1,
        required_project_milestones=3,
    ),
)


LEARNING_MILESTONES = MILESTONES
CAPSTONE_PROJECT_ID = "personal_ai_code_tutor"


SKILL_OUTCOMES: tuple[SkillOutcome, ...] = (
    SkillOutcome("python_mindset", "Python mindset", "Read errors, run tiny experiments, and explain what a program does.", ("01-python-mindset",), "Run tiny examples and change one thing at a time.", "Explain one error message without shame."),
    SkillOutcome("values_and_types", "Values, variables, and types", "Use names, strings, numbers, booleans, assignment, and comparison.", ("02-variables-types",), "Create variables and predict each value type.", "Write a tiny price, tax, or greeting function."),
    SkillOutcome("control_flow", "Control flow", "Make decisions with if/elif/else and combine simple conditions.", ("03-conditionals",), "Write one rule that returns a different result for different inputs.", "Build a pass/fail or grade-feedback function."),
    SkillOutcome("loops", "Loops", "Repeat work with for/while loops and trace how a value changes.", ("04-loops",), "Loop over a range or list and accumulate a result.", "Write a function that counts, filters, or totals values."),
    SkillOutcome("functions", "Functions", "Package logic into reusable steps with inputs, return values, and names.", ("05-functions",), "Write a function, test it with two inputs, and explain the return value.", "Refactor repeated code into one function."),
    SkillOutcome("collections", "Lists and dictionaries", "Store groups of values and look up structured information.", ("06-data-structures",), "Use a list for many items and a dictionary for labeled facts.", "Create a mini dataset and summarize it."),
    SkillOutcome("debugging_testing", "Debugging and testing", "Use error messages, asserts, and tiny tests to prove code works.", ("07-debugging-tests",), "Turn one bug into a mistake card and one passing test.", "Write an assert that catches a bad result."),
    SkillOutcome("real_world_data", "Files, JSON, and APIs", "Understand local files, JSON-shaped data, and basic API thinking.", ("08-files-json-apis",), "Design JSON-like data and explain how it would be saved.", "Make a tiny habit tracker or data summary plan."),
    SkillOutcome("object_modeling", "Objects and structure", "Use simple classes/objects when data and behavior belong together.", ("09-oop",), "Create a class with attributes and one useful method.", "Explain when a class is helpful and when a dictionary is enough."),
    SkillOutcome("ai_prompting", "AI-assisted coding", "Ask AI for hints, debugging help, examples, and checks without copying blindly.", ("10-ai-prompting",), "Write a prompt with task, context, constraints, format, and verification.", "Ask for a hint first, then explain the fix in your own words."),
    SkillOutcome("projects", "Project building", "Combine multiple ideas into a small script or app with proof of understanding.", ("11-mini-projects", "12-ai-apps-streamlit"), "Build one small project, test one edge case, and save a demo note.", "Ship a tiny app feature or project checkpoint with a proof card."),
    SkillOutcome("data_and_resilience", "Resilient code and data analysis", "Handle errors gracefully, transform data with comprehensions, and summarize real datasets.", ("13-error-handling", "14-comprehensions", "15-pandas-data"), "Catch one error, write one comprehension, and summarize a tiny dataset.", "Show a function that survives bad input and a small grouped data summary."),
    SkillOutcome("real_world_toolkit", "Real-world toolkit", "Work with dates and times, match patterns with regex, and write clean, readable code.", ("16-dates-times", "17-regex", "18-clean-code"), "Measure a date gap, extract data with a regex, and refactor one function.", "Show a dated calculation, a regex extraction, and a clean type-hinted function."),
    SkillOutcome("testing_apis_capstone", "Testing, APIs, and shipping", "Write automated tests, call web APIs and read JSON responses, and combine skills into a working tool.", ("19-pytest-testing", "20-web-apis", "21-capstone-text-analyzer"), "Write one test, parse one API response, and build one small analyzer.", "Show a passing test, a safe JSON read, and a working mini-tool."),
    SkillOutcome("agentic_coding", "Agentic coding", "Understand AI agents, direct them with context/prompt/model, and verify their work before shipping.", ("22-ai-agents", "23-directing-agents", "24-agentic-workflows"), "Trace one agent loop, write one executable spec, and verify one AI-made change.", "Show a spec you wrote, the agent's diff, and the check output that proved it."),
)


def _completed_lessons(progress_data: Mapping[str, Any]) -> set[str]:
    return {str(item) for item in (progress_data.get("completed_lessons", []) or [])}


def _completed_daily_days(progress_data: Mapping[str, Any]) -> set[int]:
    completed: set[int] = set()
    for key, item in (progress_data.get("daily_missions", {}) or {}).items():
        if not isinstance(item, Mapping) or item.get("status") != "Completed":
            continue
        try:
            completed.add(int(key))
        except (TypeError, ValueError):
            try:
                completed.add(int(item.get("day", 0) or 0))
            except (TypeError, ValueError):
                continue
    return completed


def _saved_gym_days(progress_data: Mapping[str, Any]) -> set[int]:
    saved: set[int] = set()
    for key, item in (progress_data.get("gym_sessions", {}) or {}).items():
        if not isinstance(item, Mapping) or item.get("status") != "Saved":
            continue
        try:
            saved.add(int(key))
        except (TypeError, ValueError):
            try:
                saved.add(int(item.get("day", 0) or 0))
            except (TypeError, ValueError):
                continue
    return saved


def _quiz_passes_for_lessons(progress_data: Mapping[str, Any], lesson_ids: Iterable[str], minimum_percent: float = 70) -> int:
    quiz_scores = progress_data.get("quiz_scores", {}) or {}
    total = 0
    for lesson_id in lesson_ids:
        score = quiz_scores.get(lesson_id, {}) if isinstance(quiz_scores, Mapping) else {}
        try:
            percent = float(score.get("percent", 0) or 0)
        except (TypeError, ValueError):
            percent = 0
        if percent >= minimum_percent:
            total += 1
    return total


def _project_milestone_count(progress_data: Mapping[str, Any], project_ids: Iterable[str]) -> int:
    projects = progress_data.get("project_milestones", {}) or {}
    total = 0
    for project_id in project_ids:
        raw_project = projects.get(project_id, {}) if isinstance(projects, Mapping) else {}
        if not isinstance(raw_project, Mapping):
            continue
        total += sum(1 for item in raw_project.values() if isinstance(item, Mapping) and item.get("status") == "Completed")
    return total


def _days_in_range(day_range: tuple[int, int]) -> tuple[int, ...]:
    start, end = day_range
    return tuple(range(start, end + 1))


def _first_incomplete(lesson_ids: Iterable[str], completed: set[str]) -> str | None:
    for lesson_id in lesson_ids:
        if lesson_id not in completed:
            return lesson_id
    return None


def _status_for_percent(percent: float) -> str:
    if percent >= 1:
        return "Complete"
    if percent > 0:
        return "In progress"
    return "Not started"


def skill_statuses(progress_data: Mapping[str, Any]) -> tuple[SkillStatus, ...]:
    completed = _completed_lessons(progress_data)
    statuses: list[SkillStatus] = []
    for skill in SKILL_OUTCOMES:
        total = len(skill.lesson_ids)
        done = sum(1 for lesson_id in skill.lesson_ids if lesson_id in completed)
        percent = round(done / total, 3) if total else 0.0
        statuses.append(
            SkillStatus(
                skill=skill,
                completed_lessons=done,
                total_lessons=total,
                percent=percent,
                status=_status_for_percent(percent),
                next_lesson_id=_first_incomplete(skill.lesson_ids, completed),
            )
        )
    return tuple(statuses)



def milestone_status(progress_data: Mapping[str, Any], milestone: LearningMilestone) -> MilestoneStatus:
    completed_lessons = _completed_lessons(progress_data)
    completed_days = _completed_daily_days(progress_data)
    saved_gym_days = _saved_gym_days(progress_data)
    milestone_days = set(_days_in_range(milestone.day_range))

    evidence: list[str] = []
    completed_requirements = 0
    total_requirements = 0

    lesson_total = len(milestone.lesson_ids)
    lesson_done = sum(1 for lesson_id in milestone.lesson_ids if lesson_id in completed_lessons)
    total_requirements += lesson_total
    completed_requirements += lesson_done
    evidence.append(f"Lessons: {lesson_done}/{lesson_total}")

    day_total = len(milestone_days)
    day_done = len(milestone_days & completed_days)
    total_requirements += day_total
    completed_requirements += day_done
    evidence.append(f"Daily missions: {day_done}/{day_total}")

    if milestone.required_saved_workouts:
        saved_workouts = len(milestone_days & saved_gym_days)
        total_requirements += milestone.required_saved_workouts
        completed_requirements += min(saved_workouts, milestone.required_saved_workouts)
        evidence.append(f"Proof cards: {saved_workouts}/{milestone.required_saved_workouts}")

    if milestone.required_quiz_passes:
        quiz_passes = _quiz_passes_for_lessons(progress_data, milestone.lesson_ids)
        total_requirements += milestone.required_quiz_passes
        completed_requirements += min(quiz_passes, milestone.required_quiz_passes)
        evidence.append(f"Quiz passes: {quiz_passes}/{milestone.required_quiz_passes}")

    if milestone.required_project_milestones:
        project_count = _project_milestone_count(progress_data, milestone.project_ids)
        total_requirements += milestone.required_project_milestones
        completed_requirements += min(project_count, milestone.required_project_milestones)
        evidence.append(f"Project checkpoints: {project_count}/{milestone.required_project_milestones}")

    percent = round(completed_requirements / total_requirements, 3) if total_requirements else 0.0
    if percent >= 1:
        status = "Complete"
        next_action = "Celebrate it, then use the next milestone to choose tomorrow's workout."
    elif completed_requirements == 0:
        status = "Not started"
        next_action = f"Start Day {milestone.day_range[0]} and save one proof card."
    else:
        status = "In progress"
        if lesson_done < lesson_total:
            missing_lesson = next(lesson_id for lesson_id in milestone.lesson_ids if lesson_id not in completed_lessons)
            next_action = f"Finish the linked lesson: {missing_lesson}."
        elif day_done < day_total:
            missing_day = next(day for day in sorted(milestone_days) if day not in completed_days)
            next_action = f"Complete Day {missing_day} in the Daily Coding Gym."
        elif milestone.required_quiz_passes and _quiz_passes_for_lessons(progress_data, milestone.lesson_ids) < milestone.required_quiz_passes:
            next_action = "Pass one linked quiz at 70% or higher."
        elif milestone.required_project_milestones and _project_milestone_count(progress_data, milestone.project_ids) < milestone.required_project_milestones:
            next_action = "Complete one project checkpoint and save proof."
        else:
            next_action = "Save one proof card for this milestone."

    return MilestoneStatus(
        milestone=milestone,
        percent=percent,
        status=status,
        completed_requirements=completed_requirements,
        total_requirements=total_requirements,
        next_action=next_action,
        evidence=tuple(evidence),
    )


def milestone_statuses(progress_data: Mapping[str, Any], milestones: Sequence[LearningMilestone] = MILESTONES) -> tuple[MilestoneStatus, ...]:
    return tuple(milestone_status(progress_data, milestone) for milestone in milestones)


def current_milestone_status(progress_data: Mapping[str, Any]) -> MilestoneStatus:
    statuses = milestone_statuses(progress_data)
    for status in statuses:
        if status.status != "Complete":
            return status
    return statuses[-1]


def completed_milestones_count(progress_data: Mapping[str, Any]) -> int:
    return sum(1 for status in milestone_statuses(progress_data) if status.status == "Complete")


def overall_learning_percent(progress_data: Mapping[str, Any]) -> float:
    statuses = milestone_statuses(progress_data)
    if not statuses:
        return 0.0
    return round(sum(status.percent for status in statuses) / len(statuses), 3)


def graduation_requirements(progress_data: Mapping[str, Any], total_lessons: int = 12) -> tuple[GraduationRequirement, ...]:
    completed_lessons = len(_completed_lessons(progress_data))
    completed_days = len(_completed_daily_days(progress_data))
    saved_proofs = len(_saved_gym_days(progress_data))
    quiz_scores = progress_data.get("quiz_scores", {}) or {}
    passed_quizzes = _quiz_passes_for_lessons(progress_data, quiz_scores.keys() if isinstance(quiz_scores, Mapping) else [])
    mistake_cards = sum(1 for card in (progress_data.get("mistake_cards", []) or []) if isinstance(card, Mapping))
    project_milestones = _project_milestone_count(progress_data, ("quiz_scorekeeper", "habit_tracker_json", "prompt_coach", "personal_ai_code_tutor"))
    prompt_scores = progress_data.get("prompt_scores", []) or []
    strong_prompts = 0
    for item in prompt_scores:
        if not isinstance(item, Mapping):
            continue
        try:
            score = int(item.get("score", 0) or 0)
        except (TypeError, ValueError):
            score = 0
        if score >= 7:
            strong_prompts += 1

    return (
        GraduationRequirement("lessons", "Complete the Python basics lessons", total_lessons, completed_lessons, "All core Python topics have been touched."),
        GraduationRequirement("daily", "Complete daily gym sessions", 24, completed_days, "At least 24 completed daily missions proves a real habit."),
        GraduationRequirement("proof", "Save proof cards", 20, saved_proofs, "Proof cards show what you learned, not just what you clicked."),
        GraduationRequirement("quiz", "Pass lesson quizzes", 8, passed_quizzes, "Quiz passes show basic recall and comprehension."),
        GraduationRequirement("project", "Complete project checkpoints", 8, project_milestones, "Projects show you can combine skills."),
        GraduationRequirement("debug", "Log mistake/review cards", 5, mistake_cards, "Mistake cards prove you are learning how to debug."),
        GraduationRequirement("prompt", "Practice strong AI prompts", 3, strong_prompts, "Prompt reps show you can use AI as a learning assistant."),
    )


def graduation_readiness(progress_data: Mapping[str, Any], total_lessons: int = 12, total_days: int | None = None) -> GraduationReadiness:
    requirements = graduation_requirements(progress_data, total_lessons=total_lessons)
    if not requirements:
        return GraduationReadiness(0.0, "Not ready", (), "No requirements configured.", "Start Day 1.")
    percent = round(sum(req.percent for req in requirements) / len(requirements), 3)
    complete_count = sum(1 for req in requirements if req.complete)
    if complete_count == len(requirements):
        status = "Ready to graduate"
        summary = "You have enough evidence to say you learned the Python basics and can keep building."
        next_action = "Do the capstone demo note and choose your next learning path."
    elif percent >= 0.7:
        status = "Close"
        summary = f"{complete_count}/{len(requirements)} graduation requirements are complete."
        next_action = next((req.title for req in requirements if not req.complete), "Finish one remaining requirement.")
    else:
        status = "Building"
        summary = f"{complete_count}/{len(requirements)} graduation requirements are complete. Keep the daily gym simple."
        next_action = next((req.title for req in requirements if not req.complete), "Start today's workout.")
    return GraduationReadiness(percent, status, requirements, summary, next_action)


def learning_outcomes() -> tuple[str, ...]:
    return (
        "Read and write simple Python scripts.",
        "Use variables, types, conditionals, loops, functions, lists, and dictionaries.",
        "Debug common beginner errors by reading messages and isolating the smallest failing line.",
        "Write simple tests or manual checks for expected behavior.",
        "Understand basic files, JSON/API shapes, and object-oriented vocabulary.",
        "Handle errors with try/except and validate input so code fails politely.",
        "Transform data with comprehensions and summarize datasets (including pandas basics).",
        "Use AI for hints, explanations, tests, and planning without outsourcing all thinking.",
        "Build and explain a small beginner project or capstone feature.",
    )
