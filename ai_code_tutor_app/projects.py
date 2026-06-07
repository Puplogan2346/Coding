from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectMilestone:
    id: str
    title: str
    proof: str


@dataclass(frozen=True)
class ProjectTrack:
    id: str
    title: str
    level: str
    minutes: int
    description: str
    skills: tuple[str, ...]
    milestones: tuple[ProjectMilestone, ...]


PROJECTS: tuple[ProjectTrack, ...] = (
    ProjectTrack(
        "quiz_scorekeeper",
        "Quiz Scorekeeper",
        "Beginner",
        90,
        "A tiny app/script that scores answers, calculates a percent, and gives friendly feedback.",
        ("variables", "conditionals", "functions", "tests"),
        (
            ProjectMilestone("plan", "Plan inputs and outputs", "Write the inputs, output, and one example score."),
            ProjectMilestone("score", "Write the score function", "A function returns score and percent."),
            ProjectMilestone("feedback", "Add friendly feedback", "Different messages appear for high, medium, and low scores."),
            ProjectMilestone("test", "Test one edge case", "An assert or manual test covers all-correct or none-correct."),
            ProjectMilestone("demo", "Demo it", "Save a 60-second demo note or screenshot idea."),
        ),
    ),
    ProjectTrack(
        "habit_tracker_json",
        "JSON Habit Tracker",
        "Beginner+",
        120,
        "Track small daily habits and save progress in JSON-like structured data.",
        ("dictionaries", "lists", "loops", "JSON", "files"),
        (
            ProjectMilestone("data", "Design the data shape", "A sample habit dictionary exists."),
            ProjectMilestone("add", "Add a habit", "A function adds or updates one habit."),
            ProjectMilestone("summary", "Summarize progress", "A loop prints or returns a short progress summary."),
            ProjectMilestone("save", "Save/load plan", "You can explain how JSON would save this data."),
            ProjectMilestone("reflect", "Reflect on privacy", "Write what data should stay local/private."),
        ),
    ),
    ProjectTrack(
        "prompt_coach",
        "Prompt Coach",
        "Intermediate starter",
        120,
        "A rubric-based helper that checks whether a prompt includes task, context, constraints, format, and verification.",
        ("strings", "functions", "rubrics", "AI prompting", "testing"),
        (
            ProjectMilestone("rubric", "Define the rubric", "List the criteria and point values."),
            ProjectMilestone("detect", "Detect missing pieces", "Code or pseudocode finds at least two missing criteria."),
            ProjectMilestone("feedback", "Generate feedback", "The app suggests one improvement without rewriting everything."),
            ProjectMilestone("examples", "Add examples", "Include one weak prompt and one improved prompt."),
            ProjectMilestone("ai", "Optional AI upgrade", "Write the safety rule: AI helps, learner decides."),
        ),
    ),
    ProjectTrack(
        "gumloop_workflow_planner",
        "Gumloop Workflow Planner",
        "AI workflow",
        90,
        "Plan a no-code AI workflow before building it in Gumloop: trigger, steps, human review, and risk checks.",
        ("workflow design", "AI automation", "prompting", "risk review"),
        (
            ProjectMilestone("use_case", "Pick a useful use case", "Write who it helps and what it saves time on."),
            ProjectMilestone("trigger", "Define trigger and inputs", "List the starting event and required fields."),
            ProjectMilestone("steps", "Map the workflow", "Write 3-5 nodes/steps in plain English."),
            ProjectMilestone("review", "Add human review", "Decide what should be checked before output is trusted."),
            ProjectMilestone("official", "Connect official learning", "Queue or complete one Gumloop official resource."),
        ),
    ),
    ProjectTrack(
        "personal_ai_code_tutor",
        "Personal AI Code Tutor Capstone",
        "Capstone",
        180,
        "Improve this learning app itself: add one feature, test it, and explain the user benefit.",
        ("Streamlit", "Python modules", "tests", "UX", "AI safety"),
        (
            ProjectMilestone("problem", "Choose one learner problem", "Name the problem and the person it helps."),
            ProjectMilestone("tiny_feature", "Build the smallest feature", "The feature can be described or implemented in one screen."),
            ProjectMilestone("test", "Add a test or checklist", "A test, QA note, or manual checklist proves it works."),
            ProjectMilestone("accessibility", "Check accessibility", "Review contrast, labels, cognitive load, and mobile use."),
            ProjectMilestone("demo", "Demo and next step", "Record a demo note plus the next improvement."),
        ),
    ),
)


def project_by_id(project_id: str) -> ProjectTrack:
    for project in PROJECTS:
        if project.id == project_id:
            return project
    raise KeyError(f"Unknown project id: {project_id}")


def project_progress(progress_data: dict, project_id: str) -> dict:
    return (progress_data.get("project_milestones", {}) or {}).get(project_id, {})


def completed_project_milestones_count(progress_data: dict) -> int:
    total = 0
    for milestones in (progress_data.get("project_milestones", {}) or {}).values():
        total += sum(1 for item in milestones.values() if item.get("status") == "Completed")
    return total


def project_completion_percent(progress_data: dict, project_id: str) -> float:
    project = project_by_id(project_id)
    saved = project_progress(progress_data, project_id)
    complete = sum(1 for milestone in project.milestones if saved.get(milestone.id, {}).get("status") == "Completed")
    return round(complete / len(project.milestones), 3)


def next_project_milestone(progress_data: dict, project_id: str) -> ProjectMilestone:
    project = project_by_id(project_id)
    saved = project_progress(progress_data, project_id)
    for milestone in project.milestones:
        if saved.get(milestone.id, {}).get("status") != "Completed":
            return milestone
    return project.milestones[-1]


def recommended_project_id(progress_data: dict) -> str:
    completed_lessons = len(progress_data.get("completed_lessons", []) or [])
    if completed_lessons >= 10:
        return "personal_ai_code_tutor"
    if completed_lessons >= 7:
        return "prompt_coach"
    if completed_lessons >= 4:
        return "habit_tracker_json"
    return "quiz_scorekeeper"
