"""Guided project builds — the step-by-step "Build Studio" content.

Each :class:`ProjectBuild` turns a project track from ``projects.py`` into a
real guided build: the learner grows one Python program across ordered steps,
each with instructions, static structure checks (see ``build_checks.py``),
assert-based tests for the local runner, and a cumulative sample solution.
Step ids match the milestone ids of the same project so passing a build step
also completes the matching capstone checkpoint.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from build_checks import StepCheck


@dataclass(frozen=True)
class BuildStep:
    id: str  # must match a ProjectMilestone id of the same project
    title: str
    goal: str
    instructions: tuple[str, ...]
    lesson_ids: tuple[str, ...]
    checks: tuple[StepCheck, ...]
    tests: str  # assert-based, stdlib only, appended after the learner's code
    sample_solution: str  # the FULL program as it should look after this step
    hint: str


@dataclass(frozen=True)
class ProjectBuild:
    project_id: str  # must match a ProjectTrack id in projects.py
    intro: str
    scaffold: str  # initial editor contents for step 1
    run_hint: str  # how to run the finished file outside the app
    filename: str  # download name, e.g. "quiz_scorekeeper.py"
    steps: tuple[BuildStep, ...]


# --------------------------------------------------------------------------
# Quiz Scorekeeper (quiz_scorekeeper)
# --------------------------------------------------------------------------
_QUIZ_SCAFFOLD = '''\
"""Quiz Scorekeeper — grade quiz answers, compute a percent, coach the student.

Build order: plan -> score -> feedback -> test -> demo.
"""

# TODO (plan): create ANSWER_KEY — a dict mapping question ids ("q1", "q2", ...)
# to the correct answer letters.

# TODO (plan): def score_quiz(answers, answer_key) — stub with a docstring,
# returning a placeholder like (0, 0.0) for now.

# TODO (plan): def feedback_message(percent) — stub with a docstring,
# returning a placeholder like "" for now.
'''

_QUIZ_SAMPLE_PLAN = '''\
"""Quiz Scorekeeper — grade quiz answers, compute a percent, coach the student."""

ANSWER_KEY = {
    "q1": "b",
    "q2": "a",
    "q3": "d",
    "q4": "c",
}


def score_quiz(answers, answer_key):
    """Count how many answers match the key; return (correct_count, percent)."""
    return 0, 0.0  # placeholder — real logic arrives in the next step


def feedback_message(percent):
    """Turn a percent into one short, friendly coaching sentence."""
    return ""  # placeholder — real tiers arrive in the feedback step
'''

_QUIZ_SAMPLE_SCORE = '''\
"""Quiz Scorekeeper — grade quiz answers, compute a percent, coach the student."""

ANSWER_KEY = {
    "q1": "b",
    "q2": "a",
    "q3": "d",
    "q4": "c",
}


def score_quiz(answers, answer_key):
    """Count how many answers match the key; return (correct_count, percent)."""
    if not answer_key:
        return 0, 0.0  # an empty quiz scores zero instead of dividing by zero
    correct = 0
    for question, right_answer in answer_key.items():
        if answers.get(question) == right_answer:
            correct = correct + 1
    percent = round(correct / len(answer_key) * 100, 1)
    return correct, percent


def feedback_message(percent):
    """Turn a percent into one short, friendly coaching sentence."""
    return ""  # placeholder — real tiers arrive in the feedback step
'''

_QUIZ_SAMPLE_FEEDBACK = '''\
"""Quiz Scorekeeper — grade quiz answers, compute a percent, coach the student."""

ANSWER_KEY = {
    "q1": "b",
    "q2": "a",
    "q3": "d",
    "q4": "c",
}


def score_quiz(answers, answer_key):
    """Count how many answers match the key; return (correct_count, percent)."""
    if not answer_key:
        return 0, 0.0  # an empty quiz scores zero instead of dividing by zero
    correct = 0
    for question, right_answer in answer_key.items():
        if answers.get(question) == right_answer:
            correct = correct + 1
    percent = round(correct / len(answer_key) * 100, 1)
    return correct, percent


def feedback_message(percent):
    """Turn a percent into one short, friendly coaching sentence."""
    if percent >= 90:
        return "Outstanding! You really know this material."
    elif percent >= 70:
        return "Nice work! One more quick review and you will have it locked in."
    elif percent >= 50:
        return "Good effort — you are over halfway there. Keep going!"
    else:
        return "Tough round. Take a breath, review the basics, and try again."
'''

_QUIZ_SAMPLE_TEST = '''\
"""Quiz Scorekeeper — grade quiz answers, compute a percent, coach the student."""

ANSWER_KEY = {
    "q1": "b",
    "q2": "a",
    "q3": "d",
    "q4": "c",
}


def score_quiz(answers, answer_key):
    """Count how many answers match the key; return (correct_count, percent)."""
    if not answer_key:
        return 0, 0.0  # an empty quiz scores zero instead of dividing by zero
    correct = 0
    for question, right_answer in answer_key.items():
        if answers.get(question) == right_answer:
            correct = correct + 1
    percent = round(correct / len(answer_key) * 100, 1)
    return correct, percent


def feedback_message(percent):
    """Turn a percent into one short, friendly coaching sentence."""
    if percent >= 90:
        return "Outstanding! You really know this material."
    elif percent >= 70:
        return "Nice work! One more quick review and you will have it locked in."
    elif percent >= 50:
        return "Good effort — you are over halfway there. Keep going!"
    else:
        return "Tough round. Take a breath, review the basics, and try again."


def run_checks():
    """My own safety net: edge cases the grader must survive."""
    all_wrong = {"q1": "z", "q2": "z", "q3": "z", "q4": "z"}
    assert score_quiz(all_wrong, ANSWER_KEY) == (0, 0.0)
    assert score_quiz({}, {}) == (0, 0.0)
    assert feedback_message(0) != feedback_message(100)
    print("run_checks: all edge cases passed.")
'''

_QUIZ_SAMPLE_DEMO = '''\
"""Quiz Scorekeeper — grade quiz answers, compute a percent, coach the student."""

ANSWER_KEY = {
    "q1": "b",
    "q2": "a",
    "q3": "d",
    "q4": "c",
}


def score_quiz(answers, answer_key):
    """Count how many answers match the key; return (correct_count, percent)."""
    if not answer_key:
        return 0, 0.0  # an empty quiz scores zero instead of dividing by zero
    correct = 0
    for question, right_answer in answer_key.items():
        if answers.get(question) == right_answer:
            correct = correct + 1
    percent = round(correct / len(answer_key) * 100, 1)
    return correct, percent


def feedback_message(percent):
    """Turn a percent into one short, friendly coaching sentence."""
    if percent >= 90:
        return "Outstanding! You really know this material."
    elif percent >= 70:
        return "Nice work! One more quick review and you will have it locked in."
    elif percent >= 50:
        return "Good effort — you are over halfway there. Keep going!"
    else:
        return "Tough round. Take a breath, review the basics, and try again."


def run_checks():
    """My own safety net: edge cases the grader must survive."""
    all_wrong = {"q1": "z", "q2": "z", "q3": "z", "q4": "z"}
    assert score_quiz(all_wrong, ANSWER_KEY) == (0, 0.0)
    assert score_quiz({}, {}) == (0, 0.0)
    assert feedback_message(0) != feedback_message(100)
    print("run_checks: all edge cases passed.")


def report_card(student_name, answers, answer_key):
    """Build a short, friendly report-card string for one student."""
    correct, percent = score_quiz(answers, answer_key)
    message = feedback_message(percent)
    return (
        f"Report card for {student_name}\\n"
        f"Score: {correct}/{len(answer_key)} correct ({percent}%)\\n"
        f"Coach says: {message}"
    )


if __name__ == "__main__":
    run_checks()
    student_answers = {"q1": "b", "q2": "a", "q3": "d", "q4": "x"}
    print(report_card("Jordan", student_answers, ANSWER_KEY))
'''


_QUIZ_BUILD = ProjectBuild(
    project_id="quiz_scorekeeper",
    intro=(
        "Your first real program: a quiz grader. You will grow one file across five "
        "steps — plan the shape with stub functions, implement the scoring loop, add "
        "friendly if/elif/else feedback, write your own edge-case checks, and finish "
        "with a demo that prints a report card. Every professional program starts "
        "exactly like this: sketch, fill in, test, show off."
    ),
    scaffold=_QUIZ_SCAFFOLD,
    run_hint=(
        "Run it from a terminal with: python quiz_scorekeeper.py — it runs your "
        "run_checks() safety net first, then prints Jordan's report card."
    ),
    filename="quiz_scorekeeper.py",
    steps=(
        BuildStep(
            id="plan",
            title="Plan the program with stubs",
            goal="Create ANSWER_KEY and write empty 'stub' versions of both functions so the program's shape exists before any logic.",
            instructions=(
                "Create ANSWER_KEY: a dict where keys are question ids like \"q1\" and values are the correct answer letters like \"b\". Give it at least 3 questions — this is the single source of truth the whole program grades against.",
                "Write def score_quiz(answers, answer_key): with a one-line docstring saying what it WILL do, and have it return a placeholder (0, 0.0) for now. A stub like this lets you design the program before writing any hard logic.",
                "Write def feedback_message(percent): the same way — docstring first, then return \"\" as a placeholder.",
                "Why stubs? Sketching function names, parameters, and return shapes first is how real developers plan: you decide WHAT each piece does before worrying about HOW.",
            ),
            lesson_ids=("01-python-mindset", "05-functions", "06-data-structures"),
            checks=(
                StepCheck("uses", "dict", "Create ANSWER_KEY as a dict literal ({...})."),
                StepCheck("defines_function", "score_quiz", "Define a stub function called score_quiz."),
                StepCheck("defines_function", "feedback_message", "Define a stub function called feedback_message."),
                StepCheck("uses", "return", "Each stub should return a placeholder value."),
            ),
            tests='''\
assert isinstance(ANSWER_KEY, dict), "ANSWER_KEY should be a dict of question -> correct answer"
assert len(ANSWER_KEY) >= 3, "Give your quiz at least 3 questions"
assert callable(score_quiz), "score_quiz should be a function"
assert callable(feedback_message), "feedback_message should be a function"
assert score_quiz.__doc__, "Give score_quiz a docstring saying what it will do"
assert feedback_message.__doc__, "Give feedback_message a docstring too"
''',
            sample_solution=_QUIZ_SAMPLE_PLAN,
            hint="A stub is just def name(params): + a docstring + return <placeholder> — three lines per function, no logic yet.",
        ),
        BuildStep(
            id="score",
            title="Implement score_quiz",
            goal="Loop over the answer key, count matching answers, and return (correct_count, percent).",
            instructions=(
                "Start score_quiz with a guard: if answer_key is empty, return (0, 0.0) right away. Without this, the percent math below would divide by zero on an empty quiz.",
                "Set correct = 0, then loop with for question, right_answer in answer_key.items(): — looping over the KEY (not the student's answers) means extra or missing student answers can never break the grading.",
                "Inside the loop, compare answers.get(question) to right_answer and add 1 to correct when they match. Using .get() instead of answers[question] returns None for unanswered questions instead of crashing.",
                "After the loop, compute percent = round(correct / len(answer_key) * 100, 1) and return correct, percent — a tuple, so callers get both numbers in one call.",
            ),
            lesson_ids=("04-loops", "06-data-structures"),
            checks=(
                StepCheck("uses", "for", "Loop over the answer key with a for loop."),
                StepCheck("uses", "if", "Use if to compare each answer (and to guard the empty quiz)."),
                StepCheck("calls", "round", "Round the percent with round(..., 1)."),
            ),
            tests='''\
_test_key = {"q1": "b", "q2": "a", "q3": "d", "q4": "c"}
assert score_quiz({"q1": "b", "q2": "a", "q3": "d", "q4": "c"}, _test_key) == (4, 100.0), "all correct should be (4, 100.0)"
assert score_quiz({"q1": "b", "q2": "x", "q3": "d", "q4": "x"}, _test_key) == (2, 50.0), "half right should be (2, 50.0)"
assert score_quiz({}, _test_key) == (0, 0.0), "no answers at all should be (0, 0.0)"
assert score_quiz({"q1": "b", "bonus": "z"}, _test_key) == (1, 25.0), "answers not in the key should be ignored"
_three_key = {"q1": "a", "q2": "b", "q3": "c"}
assert score_quiz({"q1": "a"}, _three_key) == (1, 33.3), "percent should be rounded to 1 decimal place"
''',
            sample_solution=_QUIZ_SAMPLE_SCORE,
            hint="Loop over answer_key.items() and compare answers.get(question) == right_answer — then percent is round(correct / len(answer_key) * 100, 1).",
        ),
        BuildStep(
            id="feedback",
            title="Implement feedback_message",
            goal="Turn a percent into one of four friendly messages using an if/elif/else ladder.",
            instructions=(
                "Replace the stub body with an if/elif/else ladder over percent: >= 90 gets a celebratory message, >= 70 gets an encouraging one, >= 50 gets a keep-going one, and else gets a gentle try-again.",
                "Order matters: Python takes the FIRST branch that is true, so check the highest tier first. If you checked >= 50 first, a 95% student would get the mediocre message.",
                "Each branch should return its own distinct string — returning ends the function immediately, so no break or extra logic is needed.",
                "Write messages you would actually want to read after a quiz: specific, warm, and short. This function is the personality of your program.",
            ),
            lesson_ids=("03-conditionals",),
            checks=(
                StepCheck("defines_function", "feedback_message", "Keep the feedback_message function."),
                StepCheck("uses", "if", "Use an if/elif/else ladder to pick the tier."),
                StepCheck("uses", "return", "Each branch should return its message string."),
            ),
            tests='''\
assert feedback_message(100) == feedback_message(90), "100 and 90 belong to the same top tier"
assert feedback_message(89) == feedback_message(70), "89 and 70 belong to the same tier"
assert feedback_message(69) == feedback_message(50), "69 and 50 belong to the same tier"
assert feedback_message(49) == feedback_message(0), "49 and 0 belong to the same bottom tier"
assert feedback_message(90) != feedback_message(89), "90 should be the boundary of the top tier"
assert feedback_message(70) != feedback_message(69), "70 should be a tier boundary"
assert feedback_message(50) != feedback_message(49), "50 should be a tier boundary"
_msg = feedback_message(75)
assert isinstance(_msg, str) and len(_msg) > 3, "feedback_message should return a real sentence"
''',
            sample_solution=_QUIZ_SAMPLE_FEEDBACK,
            hint="Check the tiers from highest to lowest: if percent >= 90: ... elif percent >= 70: ... elif percent >= 50: ... else: ... — each branch returns its own string.",
        ),
        BuildStep(
            id="test",
            title="Write your own safety net",
            goal="Add a run_checks() function full of your OWN asserts that pin the nasty edge cases.",
            instructions=(
                "Define run_checks() with a short docstring. It takes no arguments and simply runs asserts — if any assert is false, Python stops with an AssertionError pointing at the exact broken expectation.",
                "Edge case 1 — all wrong: build a dict with the same questions as ANSWER_KEY but junk answers (like \"z\"), and assert score_quiz(all_wrong, ANSWER_KEY) == (0, 0.0).",
                "Edge case 2 — empty quiz: assert score_quiz({}, {}) == (0, 0.0). This proves the guard you wrote in the score step really protects against dividing by zero.",
                "Add one assert about feedback too, like assert feedback_message(0) != feedback_message(100) — bottom and top tiers must never share a message.",
                "Finish run_checks() with a print like \"run_checks: all edge cases passed.\" so a clean run tells you the net held. Writing checks for your own code is the habit that separates hobby scripts from software.",
            ),
            lesson_ids=("07-debugging-tests",),
            checks=(
                StepCheck("defines_function", "run_checks", "Define a run_checks function for your own asserts."),
                StepCheck("uses", "assert", "Use assert statements inside run_checks."),
                StepCheck("calls", "score_quiz", "run_checks should actually call score_quiz."),
            ),
            tests='''\
assert callable(run_checks), "run_checks should be a function"
run_checks()  # your own asserts must all pass without raising
assert score_quiz({}, {}) == (0, 0.0), "an empty quiz should score safely, not crash"
_all_wrong = {"q1": "zzz", "q2": "zzz"}
assert score_quiz(_all_wrong, {"q1": "a", "q2": "b"}) == (0, 0.0), "all-wrong answers should be (0, 0.0)"
''',
            sample_solution=_QUIZ_SAMPLE_TEST,
            hint="Inside run_checks, build an all-wrong answers dict and assert score_quiz(...) == (0, 0.0), then assert score_quiz({}, {}) == (0, 0.0) for the empty quiz.",
        ),
        BuildStep(
            id="demo",
            title="Demo it with a report card",
            goal="Add a report_card() helper plus a main-guard that grades a hardcoded student and prints an f-string report card.",
            instructions=(
                "Define report_card(student_name, answers, answer_key): call score_quiz and feedback_message, then RETURN one f-string with the name, the score as correct/total plus the percent, and the coaching message. Returning the string (instead of printing inside) keeps it testable.",
                "Use \\n inside the f-string (or join several f-strings) so the card prints as a tidy multi-line block.",
                "At the bottom, add if __name__ == \"__main__\": — code under this guard runs when you execute the file directly but NOT when another program imports your functions.",
                "Inside the guard, call run_checks() first (safety net before the show), then make a hardcoded student_answers dict with one wrong answer and print(report_card(\"Jordan\", student_answers, ANSWER_KEY)).",
                "Run the file: you should see the run_checks message, then Jordan's 3/4 report card with the encouraging tier. That is a complete, demo-ready program.",
            ),
            lesson_ids=("11-mini-projects", "18-clean-code"),
            checks=(
                StepCheck("defines_function", "report_card", "Define report_card to build the report string."),
                StepCheck("uses", "f-string", "Build the report card with an f-string."),
                StepCheck("uses", "main-guard", 'Add the if __name__ == "__main__": block at the bottom.'),
                StepCheck("calls", "print", "Print the report card inside the main guard."),
            ),
            tests='''\
_demo_key = {"q1": "b", "q2": "a"}
_card = report_card("Test Student", {"q1": "b", "q2": "a"}, _demo_key)
assert isinstance(_card, str), "report_card should RETURN a string (print it in the main guard)"
assert "Test Student" in _card, "the card should include the student's name"
assert "2/2" in _card, "the card should show the score as correct/total, like 2/2"
assert "100.0" in _card, "the card should include the percent"
assert feedback_message(100.0) in _card, "the card should include the feedback message"
_partial = report_card("Test Student", {"q1": "b", "q2": "x"}, _demo_key)
assert "1/2" in _partial and "50.0" in _partial, "a half-right student should see 1/2 and 50.0"
''',
            sample_solution=_QUIZ_SAMPLE_DEMO,
            hint='report_card returns f"Report card for {student_name}\\n..." built from score_quiz and feedback_message; the main guard just calls run_checks() and print(report_card(...)).',
        ),
    ),
)


# --------------------------------------------------------------------------
# JSON Habit Tracker (habit_tracker_json)
# --------------------------------------------------------------------------
_HABIT_SCAFFOLD = '''"""JSON Habit Tracker — build it step by step.

You will grow this one file across 5 steps:
data -> add -> summary -> save -> reflect.
"""

# TODO (step 1): create a HABITS list that holds a few habit dicts.
# Each habit dict needs: "name" (str), "streak" (int), "done_today" (bool).

# TODO (later steps): add_habit(), check_off(), summarize(),
# to_json(), from_json(), and a demo under a main-guard at the bottom.
'''


_HABIT_SAMPLE_DATA = '''"""JSON Habit Tracker — a tiny script that tracks daily habits."""

HABITS = [
    {"name": "meditate", "streak": 4, "done_today": False},
    {"name": "read", "streak": 2, "done_today": True},
    {"name": "stretch", "streak": 0, "done_today": False},
]
'''


_HABIT_SAMPLE_ADD = '''"""JSON Habit Tracker — a tiny script that tracks daily habits."""

HABITS = [
    {"name": "meditate", "streak": 4, "done_today": False},
    {"name": "read", "streak": 2, "done_today": True},
    {"name": "stretch", "streak": 0, "done_today": False},
]


def add_habit(habits, name):
    """Add a new habit with a fresh streak; refuse duplicates."""
    for habit in habits:
        if habit["name"] == name:
            return False
    habits.append({"name": name, "streak": 0, "done_today": False})
    return True


def check_off(habits, name):
    """Mark a habit done today and bump its streak (only once per day)."""
    for habit in habits:
        if habit["name"] == name:
            if not habit["done_today"]:
                habit["done_today"] = True
                habit["streak"] += 1
            return True
    return False
'''


_HABIT_SAMPLE_SUMMARY = '''"""JSON Habit Tracker — a tiny script that tracks daily habits."""

HABITS = [
    {"name": "meditate", "streak": 4, "done_today": False},
    {"name": "read", "streak": 2, "done_today": True},
    {"name": "stretch", "streak": 0, "done_today": False},
]


def add_habit(habits, name):
    """Add a new habit with a fresh streak; refuse duplicates."""
    for habit in habits:
        if habit["name"] == name:
            return False
    habits.append({"name": name, "streak": 0, "done_today": False})
    return True


def check_off(habits, name):
    """Mark a habit done today and bump its streak (only once per day)."""
    for habit in habits:
        if habit["name"] == name:
            if not habit["done_today"]:
                habit["done_today"] = True
                habit["streak"] += 1
            return True
    return False


def summarize(habits):
    """Return one readable progress line per habit."""
    lines = []
    for habit in habits:
        status = "done" if habit["done_today"] else "not yet"
        lines.append(f"{habit['name']}: {habit['streak']}-day streak ({status})")
    return lines
'''


_HABIT_SAMPLE_SAVE = '''"""JSON Habit Tracker — a tiny script that tracks daily habits."""

import json

HABITS = [
    {"name": "meditate", "streak": 4, "done_today": False},
    {"name": "read", "streak": 2, "done_today": True},
    {"name": "stretch", "streak": 0, "done_today": False},
]


def add_habit(habits, name):
    """Add a new habit with a fresh streak; refuse duplicates."""
    for habit in habits:
        if habit["name"] == name:
            return False
    habits.append({"name": name, "streak": 0, "done_today": False})
    return True


def check_off(habits, name):
    """Mark a habit done today and bump its streak (only once per day)."""
    for habit in habits:
        if habit["name"] == name:
            if not habit["done_today"]:
                habit["done_today"] = True
                habit["streak"] += 1
            return True
    return False


def summarize(habits):
    """Return one readable progress line per habit."""
    lines = []
    for habit in habits:
        status = "done" if habit["done_today"] else "not yet"
        lines.append(f"{habit['name']}: {habit['streak']}-day streak ({status})")
    return lines


def to_json(habits):
    """Turn the habit list into a JSON string — what a save file would hold."""
    return json.dumps(habits, indent=2)


def from_json(text):
    """Parse a JSON string back into a habit list."""
    return json.loads(text)
'''


_HABIT_SAMPLE_REFLECT = '''"""JSON Habit Tracker — a tiny script that tracks daily habits.

Privacy note: habit data is personal. Keep this file and its JSON on
your own machine — do not paste real entries into shared chats or
upload them anywhere.
"""

import json

HABITS = [
    {"name": "meditate", "streak": 4, "done_today": False},
    {"name": "read", "streak": 2, "done_today": True},
    {"name": "stretch", "streak": 0, "done_today": False},
]


def add_habit(habits, name):
    """Add a new habit with a fresh streak; refuse duplicates."""
    for habit in habits:
        if habit["name"] == name:
            return False
    habits.append({"name": name, "streak": 0, "done_today": False})
    return True


def check_off(habits, name):
    """Mark a habit done today and bump its streak (only once per day)."""
    for habit in habits:
        if habit["name"] == name:
            if not habit["done_today"]:
                habit["done_today"] = True
                habit["streak"] += 1
            return True
    return False


def summarize(habits):
    """Return one readable progress line per habit."""
    lines = []
    for habit in habits:
        status = "done" if habit["done_today"] else "not yet"
        lines.append(f"{habit['name']}: {habit['streak']}-day streak ({status})")
    return lines


def to_json(habits):
    """Turn the habit list into a JSON string — what a save file would hold."""
    return json.dumps(habits, indent=2)


def from_json(text):
    """Parse a JSON string into a habit list; return [] if the text is bad."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return []


if __name__ == "__main__":
    today = from_json(to_json(HABITS))  # round-trip = load a saved copy
    add_habit(today, "journal")
    check_off(today, "meditate")
    check_off(today, "journal")
    print("== Habit report ==")
    for line in summarize(today):
        print(line)
    print(f"A save file would hold {len(to_json(today))} characters of JSON.")
'''


_HABIT_BUILD = ProjectBuild(
    project_id="habit_tracker_json",
    intro=(
        "Build a habit tracker the way real apps store data: a list of small "
        "dictionaries that round-trips through JSON. You'll design the data shape, "
        "write functions that update it safely, summarize progress with a loop, "
        "and finish by making the loader crash-proof and privacy-aware."
    ),
    scaffold=_HABIT_SCAFFOLD,
    run_hint="Run it from a terminal with: python habit_tracker.py — the demo prints a small habit report.",
    filename="habit_tracker.py",
    steps=(
        BuildStep(
            id="data",
            title="Design the data shape",
            goal="Create a HABITS list where each habit is a small dict with the same three keys.",
            instructions=(
                "At the top of the file (under the docstring), create a variable named "
                "HABITS that holds a list — square brackets — of habit dictionaries.",
                'Give every habit dict exactly three keys: "name" (a string like '
                '"meditate"), "streak" (a whole number of days), and "done_today" '
                "(True or False).",
                "Add at least three habits so later steps have something to loop over — "
                "pick real habits you care about.",
                "Keep the shape identical for every habit. Consistent keys are what let "
                "one function handle every habit the same way — and what makes the data "
                "easy to turn into JSON later.",
            ),
            lesson_ids=("02-variables-types", "06-data-structures"),
            checks=(
                StepCheck("uses", "list", "Create a HABITS list with square brackets."),
                StepCheck("uses", "dict", "Each habit should be a dictionary with curly braces."),
            ),
            tests=(
                "assert isinstance(HABITS, list), 'HABITS should be a list'\n"
                "assert len(HABITS) >= 3, 'add at least three habits'\n"
                "for _habit in HABITS:\n"
                "    assert isinstance(_habit, dict), 'each habit should be a dict'\n"
                "    assert set(_habit.keys()) == {'name', 'streak', 'done_today'}\n"
                "    assert isinstance(_habit['name'], str) and _habit['name']\n"
                "    assert isinstance(_habit['streak'], int) and _habit['streak'] >= 0\n"
                "    assert isinstance(_habit['done_today'], bool)\n"
            ),
            sample_solution=_HABIT_SAMPLE_DATA,
            hint=(
                "Start with HABITS = [ ... ] and put one dict per habit inside, e.g. "
                '{"name": "meditate", "streak": 4, "done_today": False}.'
            ),
        ),
        BuildStep(
            id="add",
            title="Add and check off habits",
            goal="Write add_habit() and check_off() so the list only changes in safe, predictable ways.",
            instructions=(
                "Define add_habit(habits, name): loop over habits and, if any dict "
                "already has that name, return False — no duplicates allowed.",
                'If the name is new, habits.append() a fresh dict with streak 0 and '
                "done_today False, then return True so callers know it worked.",
                "Define check_off(habits, name): find the habit with that name; if it "
                "is not done yet, set done_today to True and add 1 to its streak.",
                "Return True when you found the habit and False when you didn't — and "
                "make sure checking off twice in one day doesn't bump the streak twice. "
                "Guarding updates like this is how you keep data trustworthy.",
            ),
            lesson_ids=("05-functions", "04-loops", "03-conditionals"),
            checks=(
                StepCheck("defines_function", "add_habit", "Define add_habit(habits, name)."),
                StepCheck("defines_function", "check_off", "Define check_off(habits, name)."),
                StepCheck("calls", "append", "Use habits.append(...) to add the new habit dict."),
                StepCheck("uses", "if", "Use an if to refuse duplicates and guard the streak bump."),
            ),
            tests=(
                "_crew = [{'name': 'meditate', 'streak': 4, 'done_today': False}]\n"
                "assert add_habit(_crew, 'read') is True\n"
                "assert len(_crew) == 2\n"
                "assert _crew[1] == {'name': 'read', 'streak': 0, 'done_today': False}\n"
                "assert add_habit(_crew, 'read') is False, 'no duplicate habits'\n"
                "assert len(_crew) == 2, 'duplicates should not be appended'\n"
                "assert check_off(_crew, 'meditate') is True\n"
                "assert _crew[0]['streak'] == 5 and _crew[0]['done_today'] is True\n"
                "assert check_off(_crew, 'meditate') is True\n"
                "assert _crew[0]['streak'] == 5, 'no double-count on the same day'\n"
                "assert check_off(_crew, 'nap') is False, 'unknown habits return False'\n"
            ),
            sample_solution=_HABIT_SAMPLE_ADD,
            hint=(
                "Both functions start the same way: for habit in habits: if "
                'habit["name"] == name: — what happens inside that if is the only difference.'
            ),
        ),
        BuildStep(
            id="summary",
            title="Summarize progress",
            goal="Write summarize() that turns the habit list into short, human-readable progress lines.",
            instructions=(
                "Define summarize(habits) and start it with an empty list called lines.",
                "Loop over the habits with a for loop and build one f-string per habit, "
                'like "meditate: 4-day streak (done)" — pull the name and streak '
                "straight out of each dict.",
                'Use done_today to vary the wording, e.g. "(done)" vs "(not yet)", '
                "so the report tells you what still needs doing today.",
                "Append each line to lines and return the list — returning data instead "
                "of print()ing keeps the function reusable (a web app could show the "
                "same lines on screen).",
            ),
            lesson_ids=("04-loops", "06-data-structures"),
            checks=(
                StepCheck("defines_function", "summarize", "Define summarize(habits)."),
                StepCheck("uses", "for", "Loop over the habits with a for loop."),
                StepCheck("uses", "f-string", "Build each line with an f-string."),
            ),
            tests=(
                "_sample = [\n"
                "    {'name': 'meditate', 'streak': 4, 'done_today': True},\n"
                "    {'name': 'read', 'streak': 0, 'done_today': False},\n"
                "]\n"
                "_lines = summarize(_sample)\n"
                "assert isinstance(_lines, list), 'return a list of lines'\n"
                "assert len(_lines) == 2, 'one line per habit'\n"
                "assert all(isinstance(_line, str) for _line in _lines)\n"
                "assert 'meditate' in _lines[0] and '4' in _lines[0]\n"
                "assert 'read' in _lines[1] and '0' in _lines[1]\n"
                "assert _lines[0] != _lines[1], 'lines should reflect each habit'\n"
                "assert summarize([]) == [], 'no habits means no lines'\n"
            ),
            sample_solution=_HABIT_SAMPLE_SUMMARY,
            hint=(
                "Inside the loop, f\"{habit['name']}: {habit['streak']}-day streak\" gets "
                "you most of the way — then append it to your lines list."
            ),
        ),
        BuildStep(
            id="save",
            title="Save and load with JSON",
            goal="Write to_json() and from_json() so the whole habit list round-trips through one JSON string.",
            instructions=(
                "Add import json at the top of the file, just under the docstring.",
                "Define to_json(habits) that returns json.dumps(habits, indent=2) — a "
                "plain string. That exact string is what you would write into a save "
                "file on disk; JSON is just structured text.",
                "Define from_json(text) that returns json.loads(text), turning the "
                "string back into a real Python list of dicts.",
                "Your consistent data shape from step 1 pays off here: lists, dicts, "
                "strings, ints, and booleans are exactly the types JSON understands, so "
                "the round-trip loses nothing.",
            ),
            lesson_ids=("08-files-json-apis", "06-data-structures"),
            checks=(
                StepCheck("defines_function", "to_json", "Define to_json(habits)."),
                StepCheck("defines_function", "from_json", "Define from_json(text)."),
                StepCheck("calls", "json.dumps", "to_json should call json.dumps(...)."),
                StepCheck("calls", "json.loads", "from_json should call json.loads(...)."),
            ),
            tests=(
                "import json as _json\n"
                "_sample = [{'name': 'read', 'streak': 3, 'done_today': True}]\n"
                "_text = to_json(_sample)\n"
                "assert isinstance(_text, str), 'to_json returns a string'\n"
                "assert _json.loads(_text) == _sample, 'the JSON must hold the same data'\n"
                "assert from_json(_text) == _sample, 'from_json undoes to_json'\n"
                "_copy = from_json(to_json(HABITS))\n"
                "assert _copy == HABITS, 'the full list round-trips unchanged'\n"
                "assert _copy is not HABITS, 'loading builds a fresh list'\n"
            ),
            sample_solution=_HABIT_SAMPLE_SAVE,
            hint=(
                "Each function is one return line: json.dumps(...) turns data into a "
                "string, json.loads(...) turns the string back into data."
            ),
        ),
        BuildStep(
            id="reflect",
            title="Make it resilient and private",
            goal="Handle broken JSON gracefully, note why this data stays local, and add a main-guard demo.",
            instructions=(
                "Real save files get corrupted, so make from_json forgiving: wrap the "
                "json.loads call in try/except json.JSONDecodeError and return [] (an "
                "empty habit list) instead of crashing on bad text.",
                "Extend the module docstring at the very top with a privacy note: habit "
                "data is personal, so it should stay local on your machine — never "
                "pasted into shared chats or uploaded.",
                'Add if __name__ == "__main__": at the bottom. Inside it, load a copy '
                "with from_json(to_json(HABITS)), add_habit() one new habit, check_off() "
                "a couple, then print each line from summarize().",
                "The main-guard means the demo only runs when you execute the file "
                "directly — another program could import your functions without "
                "triggering it.",
            ),
            lesson_ids=("13-error-handling", "18-clean-code"),
            checks=(
                StepCheck("uses", "try", "Wrap json.loads in a try/except inside from_json."),
                StepCheck("uses", "main-guard", 'Add an if __name__ == "__main__": demo block.'),
                StepCheck("calls", "print", "The demo should print() the habit report."),
            ),
            tests=(
                "assert from_json('this is not json') == [], 'bad text returns a safe default'\n"
                "assert from_json('') == [], 'empty text returns a safe default'\n"
                "assert from_json('[{\"name\": \"read\", \"streak\": 1, \"done_today\": false}]') == [\n"
                "    {'name': 'read', 'streak': 1, 'done_today': False}\n"
                "], 'good JSON still loads normally'\n"
                "_docs = (__doc__ or '') + (from_json.__doc__ or '')\n"
                "assert any(_word in _docs.lower() for _word in ('personal', 'private', 'local')), (\n"
                "    'add a docstring note that habit data is personal and stays local'\n"
                ")\n"
            ),
            sample_solution=_HABIT_SAMPLE_REFLECT,
            hint=(
                "Inside from_json: try: return json.loads(text) / except "
                "json.JSONDecodeError: return [] — then write the docstring and demo."
            ),
        ),
    ),
)


# --------------------------------------------------------------------------
# Prompt Coach (prompt_coach)
# --------------------------------------------------------------------------
_PROMPT_SCAFFOLD = '''"""Prompt Coach — score AI prompts against a five-part rubric.

You will grow this file step by step:
1. RUBRIC: the five criteria and their signal keywords.
2. missing_criteria(): find which criteria a prompt skips.
3. coach_feedback(): a score plus one concrete suggestion.
4. WEAK_PROMPT vs STRONG_PROMPT: prove the rubric works.
5. coach_report(): the full report, plus the AI safety rule.
"""

# TODO (Step 1): define RUBRIC — a dict mapping each criterion
# ("task", "context", "constraints", "format", "verification")
# to a list of lowercase signal keywords.
'''


_PROMPT_STEP1_SOLUTION = '''"""Prompt Coach: score an AI prompt against a five-part rubric.

Checks whether a prompt covers task, context, constraints, format,
and verification, then coaches you on the first thing to fix.
"""

RUBRIC = {
    "task": ["task", "summarize", "write", "explain"],
    "context": ["context", "audience", "background"],
    "constraints": ["constraints", "limit", "avoid", "at most"],
    "format": ["format", "bullet", "table", "json"],
    "verification": ["verification", "verify", "check", "cite"],
}
'''


_PROMPT_STEP2_SOLUTION = _PROMPT_STEP1_SOLUTION + '''

def missing_criteria(prompt_text):
    """Return the rubric criteria whose keywords never appear in the prompt."""
    lowered = prompt_text.lower()
    missing = []
    for criterion, keywords in RUBRIC.items():
        found = any(keyword in lowered for keyword in keywords)
        if not found:
            missing.append(criterion)
    return missing
'''


_PROMPT_STEP3_SOLUTION = _PROMPT_STEP2_SOLUTION + '''

SUGGESTIONS = {
    "task": "State the task in one clear sentence, e.g. 'Summarize this email in two lines.'",
    "context": "Add context: say who the audience is and what background matters.",
    "constraints": "Add constraints: a length limit, a tone, or things to avoid.",
    "format": "Name the output format you want: bullet points, a table, or JSON.",
    "verification": "Ask the AI to verify its answer, e.g. 'cite your source for each claim.'",
}


def score_prompt(prompt_text):
    """Score a prompt: one point for each rubric criterion it covers."""
    return len(RUBRIC) - len(missing_criteria(prompt_text))


def coach_feedback(prompt_text):
    """Return a score line plus one concrete suggestion for the first gap."""
    score = score_prompt(prompt_text)
    missing = missing_criteria(prompt_text)
    if missing:
        suggestion = SUGGESTIONS[missing[0]]
    else:
        suggestion = "Nothing to fix — every criterion is covered."
    return f"Score: {score}/5\\nSuggestion: {suggestion}"
'''


_PROMPT_STEP4_SOLUTION = _PROMPT_STEP3_SOLUTION + '''

WEAK_PROMPT = "Write something good about dogs."

STRONG_PROMPT = (
    "Task: summarize this article about dog training. "
    "Context: the audience is first-time dog owners. "
    "Constraints: keep it under 100 words and avoid jargon. "
    "Format: three bullet points. "
    "Verification: double-check each claim and cite the paragraph it came from."
)


def compare_examples():
    """Score the weak and strong example prompts side by side."""
    return {
        "weak": score_prompt(WEAK_PROMPT),
        "strong": score_prompt(STRONG_PROMPT),
    }
'''


_PROMPT_STEP5_SOLUTION = _PROMPT_STEP4_SOLUTION + '''

AI_RULE = "AI suggests, the learner decides — review every suggestion before you use it."


def coach_report(prompt_text):
    """Combine the score, the top suggestion, and the safety rule."""
    header = "=== Prompt Coach report ==="
    return f"{header}\\n{coach_feedback(prompt_text)}\\nRule: {AI_RULE}"


if __name__ == "__main__":
    print(coach_report(WEAK_PROMPT))
    print()
    print(coach_report(STRONG_PROMPT))
    print()
    scores = compare_examples()
    print(f"Weak prompt: {scores['weak']}/5 vs strong prompt: {scores['strong']}/5.")
'''


_PROMPT_BUILD = ProjectBuild(
    project_id="prompt_coach",
    intro=(
        "Build a rubric-based prompt checker. Great AI prompts cover five things: "
        "the task, the context, the constraints, the output format, and a way to "
        "verify the answer. You'll encode that rubric as data, detect what a prompt "
        "is missing, score it out of 5, and coach the writer on the first thing to "
        "fix — one suggestion at a time, never a full rewrite."
    ),
    scaffold=_PROMPT_SCAFFOLD,
    run_hint=(
        "Run it from a terminal with: python prompt_coach.py — the demo scores the "
        "weak and strong example prompts and prints both coaching reports."
    ),
    filename="prompt_coach.py",
    steps=(
        BuildStep(
            id="rubric",
            title="Define the rubric",
            goal="Encode the five criteria of a strong prompt as a dict of keyword lists.",
            instructions=(
                'Create a dict named RUBRIC with exactly five keys, in this order: "task", "context", "constraints", "format", "verification" — the five things every solid AI prompt should cover.',
                "Map each key to a list of lowercase signal keywords: words that, when they show up in a prompt, suggest that criterion is covered. Storing the rubric as data (instead of hard-coding if-statements) makes it easy to tune later.",
                'Always include the criterion\'s own name as its first keyword (so "task" is in the task list) — that way a prompt that literally says "Task: ..." always matches.',
                'Give every criterion at least two keywords. Good starters: task → "summarize", "write", "explain"; context → "audience", "background"; constraints → "limit", "avoid", "at most"; format → "bullet", "table", "json"; verification → "verify", "check", "cite".',
                "Keep every keyword lowercase — in the next step we lowercase the whole prompt before matching, so an uppercase keyword could never match anything.",
            ),
            lesson_ids=("02-variables-types", "06-data-structures"),
            checks=(
                StepCheck("uses", "dict", "Define RUBRIC as a dict literal ({...})."),
                StepCheck("uses", "list", "Each criterion should map to a list of keywords ([...])."),
            ),
            tests=(
                'assert isinstance(RUBRIC, dict), "RUBRIC should be a dict"\n'
                'assert list(RUBRIC.keys()) == ["task", "context", "constraints", "format", "verification"], "RUBRIC needs the five criteria, in order"\n'
                "for criterion, keywords in RUBRIC.items():\n"
                '    assert isinstance(keywords, list), f"{criterion} should map to a list"\n'
                '    assert len(keywords) >= 2, f"give {criterion} at least two keywords"\n'
                '    assert criterion in keywords, f"include {criterion!r} itself in its keyword list"\n'
                '    assert all(word == word.lower() for word in keywords), f"{criterion} keywords must be lowercase"\n'
                'assert "bullet" in RUBRIC["format"], "format keywords should include \'bullet\'"'
            ),
            sample_solution=_PROMPT_STEP1_SOLUTION,
            hint='A dict literal with list values is all you need: RUBRIC = {"task": ["task", "summarize", ...], ...} — five keys, each mapped to a list of lowercase words.',
        ),
        BuildStep(
            id="detect",
            title="Detect missing pieces",
            goal="Write missing_criteria(prompt_text): the criteria whose keywords never appear.",
            instructions=(
                "Define missing_criteria(prompt_text) — it will return a list of the rubric criteria the prompt fails to cover.",
                'First line inside: lowered = prompt_text.lower(). Lowercasing once up front makes matching case-insensitive, so "TASK" and "task" count the same.',
                'Loop over RUBRIC.items() with a for loop, and for each criterion ask whether ANY of its keywords appears in lowered — the "in" operator does substring matching on strings.',
                "When no keyword matched, append that criterion to a missing list; return the list at the end. An empty list means the prompt covered everything.",
            ),
            lesson_ids=("04-loops", "06-data-structures"),
            checks=(
                StepCheck("defines_function", "missing_criteria", "Define missing_criteria(prompt_text)."),
                StepCheck("uses", "for", "Loop over the rubric with a for loop."),
                StepCheck("calls", "lower", "Call .lower() on the prompt so matching is case-insensitive."),
            ),
            tests=(
                'assert missing_criteria("") == ["task", "context", "constraints", "format", "verification"], "an empty prompt misses everything, in rubric order"\n'
                'assert missing_criteria("task context constraints format verification") == [], "naming all five criteria should cover everything"\n'
                'result = missing_criteria("TASK: Explain Python lists, please.")\n'
                'assert isinstance(result, list), "missing_criteria should return a list"\n'
                'assert "task" not in result, "matching should be case-insensitive (TASK counts as task)"\n'
                'assert "format" in result and "verification" in result, "criteria with no keyword hits should be reported missing"'
            ),
            sample_solution=_PROMPT_STEP2_SOLUTION,
            hint="any(keyword in lowered for keyword in keywords) is a one-line way to ask: did at least one of this criterion's keywords show up?",
        ),
        BuildStep(
            id="feedback",
            title="Generate feedback",
            goal="Score the prompt out of 5 and suggest one fix for the first missing criterion.",
            instructions=(
                "Define score_prompt(prompt_text) that returns len(RUBRIC) - len(missing_criteria(prompt_text)) — one point per criterion covered. Reusing missing_criteria means one source of truth for what counts.",
                'Add a SUGGESTIONS dict with one concrete, actionable suggestion per criterion — advice on what to ADD, not a rewrite. Make the "context" suggestion mention the audience, since that\'s the most common gap.',
                "Define coach_feedback(prompt_text): compute the score and the missing list, then pick SUGGESTIONS[missing[0]] — the FIRST missing criterion only. A good coach fixes one thing at a time instead of overwhelming the writer.",
                'If nothing is missing, use a friendly "nothing to fix" message instead.',
                'Return one f-string like f"Score: {score}/5\\nSuggestion: {suggestion}" so callers get both the number and the advice.',
            ),
            lesson_ids=("03-conditionals", "05-functions", "10-ai-prompting"),
            checks=(
                StepCheck("defines_function", "score_prompt", "Define score_prompt(prompt_text)."),
                StepCheck("defines_function", "coach_feedback", "Define coach_feedback(prompt_text)."),
                StepCheck("uses", "f-string", "Build the score line with an f-string."),
            ),
            tests=(
                'assert score_prompt("") == 0, "an empty prompt scores 0"\n'
                'assert score_prompt("task context constraints format verification") == 5, "covering all five criteria scores 5"\n'
                'message = coach_feedback("Task: write a haiku about autumn.")\n'
                'assert isinstance(message, str), "coach_feedback should return a string"\n'
                'assert "1/5" in message, "a task-only prompt should score 1/5"\n'
                'assert "audience" in message.lower(), "the first gap is context — the suggestion should mention the audience"\n'
                'assert "5/5" in coach_feedback("task context constraints format verification")'
            ),
            sample_solution=_PROMPT_STEP3_SOLUTION,
            hint="missing_criteria() already tells you everything: its length gives the score, and missing[0] is the key to look up in your SUGGESTIONS dict.",
        ),
        BuildStep(
            id="examples",
            title="Add examples",
            goal="Prove the rubric works: a weak prompt and a strong prompt, scored side by side.",
            instructions=(
                'Add a WEAK_PROMPT constant — one vague sentence like "Write something good about dogs." that hits at most one criterion. Real weak prompts look exactly like this.',
                'Add a STRONG_PROMPT constant that covers all five criteria. Easiest way: start each sentence with the criterion name — "Task: ... Context: ... Constraints: ... Format: ... Verification: ..." — since step 1 put each name in its own keyword list.',
                "Wrap STRONG_PROMPT in parentheses as several adjacent string literals, one per sentence, so it stays readable without backslashes.",
                'Define compare_examples() returning {"weak": score_prompt(WEAK_PROMPT), "strong": score_prompt(STRONG_PROMPT)}. Scoring known-good and known-bad examples is how you test a rubric — if the strong one doesn\'t win, the rubric (not the prompt) needs fixing.',
            ),
            lesson_ids=("07-debugging-tests", "10-ai-prompting"),
            checks=(
                StepCheck("defines_function", "compare_examples", "Define compare_examples()."),
                StepCheck("calls", "score_prompt", "compare_examples should reuse score_prompt(...)."),
            ),
            tests=(
                'assert isinstance(WEAK_PROMPT, str) and isinstance(STRONG_PROMPT, str), "both example prompts should be strings"\n'
                'assert missing_criteria(STRONG_PROMPT) == [], "the strong prompt must cover all five criteria"\n'
                'assert len(missing_criteria(WEAK_PROMPT)) >= 2, "the weak prompt should miss at least two criteria"\n'
                "scores = compare_examples()\n"
                'assert scores["strong"] == 5, "the strong prompt should score a perfect 5"\n'
                'assert scores["weak"] < scores["strong"], "the strong prompt must outscore the weak one"'
            ),
            sample_solution=_PROMPT_STEP4_SOLUTION,
            hint="If STRONG_PROMPT literally contains the words task, context, constraints, format, and verification, it is guaranteed to hit all five keyword lists.",
        ),
        BuildStep(
            id="ai",
            title="The safety rule + full report",
            goal="Add the AI safety rule and a coach_report() demo behind a main-guard.",
            instructions=(
                'Add an AI_RULE constant that contains the exact phrase "AI suggests, the learner decides" — the spirit is that this tool (and any AI) proposes changes, but a human reviews and chooses. Every report should repeat it.',
                'Define coach_report(prompt_text) that combines a header line, the coach_feedback(...) output, and a "Rule: ..." line with AI_RULE into one string (an f-string with \\n works well).',
                'Add an if __name__ == "__main__": block at the bottom that prints coach_report(WEAK_PROMPT), then coach_report(STRONG_PROMPT), then one line comparing the two scores from compare_examples().',
                "The main-guard matters: the demo runs when you execute the file directly, but stays quiet if someone imports your functions into another program.",
            ),
            lesson_ids=("10-ai-prompting", "23-directing-agents"),
            checks=(
                StepCheck("defines_function", "coach_report", "Define coach_report(prompt_text)."),
                StepCheck("uses", "main-guard", 'Put the demo behind if __name__ == "__main__":.'),
                StepCheck("calls", "print", "The demo should print the reports."),
            ),
            tests=(
                'assert "AI suggests" in AI_RULE and "decides" in AI_RULE, "keep the spirit: AI suggests, the learner decides"\n'
                "report = coach_report(WEAK_PROMPT)\n"
                'assert AI_RULE in report, "every report should repeat the safety rule"\n'
                'assert "/5" in report, "the report should include the score line"\n'
                'assert "uggestion" in report, "the report should include the suggestion"\n'
                'assert "5/5" in coach_report(STRONG_PROMPT), "the strong prompt\'s report should show a perfect score"'
            ),
            sample_solution=_PROMPT_STEP5_SOLUTION,
            hint="coach_report just glues three strings together — a header, coach_feedback(prompt_text), and f\"Rule: {AI_RULE}\" — joined with newlines.",
        ),
    ),
)


# --------------------------------------------------------------------------
# Text Analyzer (text_analyzer)
# --------------------------------------------------------------------------
_TEXT_SCAFFOLD = '''\
"""Text Analyzer — build a word-frequency report, one step at a time."""

# Step 1 (plan): add SAMPLE_TEXT and stub out the three core functions.
# SAMPLE_TEXT = "..."   a few hardcoded sentences with repeated words

# def clean_words(text): ...   lowercase + strip punctuation -> list of words
# def count_words(words): ...  list of words -> {word: count}
# def top_words(counts, n): .. best n (word, count) pairs, highest count first

# Later steps add format_report(text, n), run_checks(), and a main-guard demo.
'''

_TEXT_STEP1 = '''\
"""Text Analyzer — turn a paragraph of text into a word-frequency report."""

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "The dog barks, and the fox runs. "
    "Quick thinking keeps the quick fox ahead!"
)


def clean_words(text):
    """Lowercase the text and return its words with punctuation stripped."""
    return []


def count_words(words):
    """Return a dict mapping each word to how many times it appears."""
    return {}


def top_words(counts, n):
    """Return the n most common (word, count) pairs, highest count first."""
    return []
'''

_TEXT_STEP2 = '''\
"""Text Analyzer — turn a paragraph of text into a word-frequency report."""
import re

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "The dog barks, and the fox runs. "
    "Quick thinking keeps the quick fox ahead!"
)


def clean_words(text):
    """Lowercase the text and return its words with punctuation stripped."""
    if not text:
        return []
    return re.findall(r"[a-z']+", text.lower())


def count_words(words):
    """Return a dict mapping each word to how many times it appears."""
    return {}


def top_words(counts, n):
    """Return the n most common (word, count) pairs, highest count first."""
    return []
'''

_TEXT_STEP3 = '''\
"""Text Analyzer — turn a paragraph of text into a word-frequency report."""
import re

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "The dog barks, and the fox runs. "
    "Quick thinking keeps the quick fox ahead!"
)


def clean_words(text):
    """Lowercase the text and return its words with punctuation stripped."""
    if not text:
        return []
    return re.findall(r"[a-z']+", text.lower())


def count_words(words):
    """Return a dict mapping each word to how many times it appears."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts, n):
    """Return the n most common (word, count) pairs, highest count first."""
    return []
'''

_TEXT_STEP4 = '''\
"""Text Analyzer — turn a paragraph of text into a word-frequency report."""
import re

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "The dog barks, and the fox runs. "
    "Quick thinking keeps the quick fox ahead!"
)


def clean_words(text):
    """Lowercase the text and return its words with punctuation stripped."""
    if not text:
        return []
    return re.findall(r"[a-z']+", text.lower())


def count_words(words):
    """Return a dict mapping each word to how many times it appears."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts, n):
    """Return the n most common (word, count) pairs, highest count first."""
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:n]


def format_report(text, n):
    """Build a readable multi-line report of the top n words in text."""
    words = clean_words(text)
    counts = count_words(words)
    lines = [f"Top {n} words ({len(words)} total, {len(counts)} unique)"]
    for word, count in top_words(counts, n):
        bar = "#" * count
        lines.append(f"  {word:<10} {count:>2}  {bar}")
    return "\\n".join(lines)
'''

_TEXT_STEP5 = '''\
"""Text Analyzer — turn a paragraph of text into a word-frequency report."""
import re

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "The dog barks, and the fox runs. "
    "Quick thinking keeps the quick fox ahead!"
)


def clean_words(text):
    """Lowercase the text and return its words with punctuation stripped."""
    if not text:
        return []
    return re.findall(r"[a-z']+", text.lower())


def count_words(words):
    """Return a dict mapping each word to how many times it appears."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts, n):
    """Return the n most common (word, count) pairs, highest count first."""
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:n]


def format_report(text, n):
    """Build a readable multi-line report of the top n words in text."""
    words = clean_words(text)
    counts = count_words(words)
    lines = [f"Top {n} words ({len(words)} total, {len(counts)} unique)"]
    for word, count in top_words(counts, n):
        bar = "#" * count
        lines.append(f"  {word:<10} {count:>2}  {bar}")
    return "\\n".join(lines)


def run_checks():
    """My own mini test suite — run this before trusting any report."""
    assert clean_words("") == []
    assert clean_words(None) == []
    assert clean_words("Dog, dog!") == ["dog", "dog"]
    assert count_words(["a", "b", "a"]) == {"a": 2, "b": 1}
    assert top_words({"a": 2, "b": 2, "c": 1}, 2) == [("a", 2), ("b", 2)]
    print("All checks passed.")


if __name__ == "__main__":
    run_checks()
    print(format_report(SAMPLE_TEXT, 5))
'''

_TEXT_BUILD = ProjectBuild(
    project_id="text_analyzer",
    intro=(
        "The classic capstone: grow one script that takes a paragraph of text and "
        "prints a word-frequency report. You will plan with stubs, clean messy text "
        "with a regex, count words in a dict, sort and format a readable report, "
        "and finish with a self-testing demo."
    ),
    scaffold=_TEXT_SCAFFOLD,
    run_hint="Run it from a terminal with: python text_analyzer.py",
    filename="text_analyzer.py",
    steps=(
        BuildStep(
            id="plan",
            title="Plan the analyzer",
            goal="Hardcode some sample text and sketch the three core functions as stubs.",
            instructions=(
                "Near the top, create a constant SAMPLE_TEXT with a few sentences of "
                "your own — include repeated words and punctuation, because that is "
                "exactly what the analyzer must handle later.",
                "Define def clean_words(text): with a one-line docstring saying what it "
                "WILL do (lowercase + strip punctuation), and just return [] for now.",
                "Define def count_words(words): the same way — docstring, then return {} "
                "as a placeholder.",
                "Define def top_words(counts, n): with a docstring and return [].",
                "Why stubs? Naming the functions and writing their docstrings first is "
                "the plan — every later step fills in exactly one piece of it.",
            ),
            lesson_ids=("21-capstone-text-analyzer", "05-functions"),
            checks=(
                StepCheck("defines_function", "clean_words", "Define clean_words(text)."),
                StepCheck("defines_function", "count_words", "Define count_words(words)."),
                StepCheck("defines_function", "top_words", "Define top_words(counts, n)."),
            ),
            tests=(
                "assert isinstance(SAMPLE_TEXT, str), \"SAMPLE_TEXT should be a string\"\n"
                "assert len(SAMPLE_TEXT.split()) >= 10, \"Give SAMPLE_TEXT at least 10 words\"\n"
                "assert callable(clean_words) and clean_words.__doc__, \"clean_words needs a docstring\"\n"
                "assert callable(count_words) and count_words.__doc__, \"count_words needs a docstring\"\n"
                "assert callable(top_words) and top_words.__doc__, \"top_words needs a docstring\"\n"
            ),
            sample_solution=_TEXT_STEP1,
            hint=(
                "A stub is just def name(...): plus a docstring plus a placeholder "
                "return — three of those and one constant is the whole step."
            ),
        ),
        BuildStep(
            id="clean",
            title="Clean the text",
            goal="Implement clean_words so messy text becomes a tidy lowercase word list.",
            instructions=(
                "Add import re at the very top of the file — the regular-expression "
                "module does the punctuation-stripping for you.",
                "Inside clean_words, guard first: if not text: return [] — that one line "
                "means empty strings and None come back as an empty list instead of "
                "crashing everything downstream.",
                "Then return re.findall(r\"[a-z']+\", text.lower()) — lowercase FIRST so "
                "the pattern only needs lowercase letters, and keep the apostrophe so "
                "\"Don't.\" becomes \"don't\", not \"don\" and \"t\".",
                "Why clean here? Every later function trusts this word list, so bad "
                "input gets handled once, in one place.",
            ),
            lesson_ids=("17-regex", "13-error-handling"),
            checks=(
                StepCheck("uses", "import", "Import the re module at the top."),
                StepCheck("calls", "re.findall", "Use re.findall to pull out the words."),
                StepCheck("uses", "if", "Guard against empty or None text with an if."),
            ),
            tests=(
                "assert clean_words(\"Hello, World!\") == [\"hello\", \"world\"]\n"
                "assert clean_words(\"Don't stop.\") == [\"don't\", \"stop\"]\n"
                "assert clean_words(\"\") == [], \"Empty text should give an empty list\"\n"
                "assert clean_words(None) == [], \"None should give an empty list, not a crash\"\n"
            ),
            sample_solution=_TEXT_STEP2,
            hint=(
                "re.findall returns a list of every match, so lowercasing the text "
                "before matching means the pattern [a-z']+ catches everything."
            ),
        ),
        BuildStep(
            id="count",
            title="Count the words",
            goal="Implement count_words so a word list becomes a word-to-count dictionary.",
            instructions=(
                "Inside count_words, start with an empty dict: counts = {}.",
                "Loop over the list with for word in words: — one visit per word is all "
                "the counting needs.",
                "Each time around, write counts[word] = counts.get(word, 0) + 1 — the "
                ".get(word, 0) part returns 0 for a word you haven't seen yet, so the "
                "very first occurrence counts as 1 without any special case.",
                "Return counts at the end — a dict is the right shape here because "
                "looking up any word's count later is instant.",
            ),
            lesson_ids=("06-data-structures", "04-loops"),
            checks=(
                StepCheck("uses", "for", "Loop over the words with a for loop."),
                StepCheck("uses", "dict", "Build the tally in a dictionary."),
                StepCheck("calls", "get", "Use counts.get(word, 0) for unseen words."),
            ),
            tests=(
                "assert count_words([]) == {}\n"
                "assert count_words([\"dog\"]) == {\"dog\": 1}\n"
                "assert count_words([\"a\", \"b\", \"a\", \"a\"]) == {\"a\": 3, \"b\": 1}\n"
                "assert count_words(clean_words(\"Dog dog DOG!\")) == {\"dog\": 3}\n"
            ),
            sample_solution=_TEXT_STEP3,
            hint=(
                "dict.get(word, 0) hands you 0 when the word isn't a key yet, so "
                "adding 1 works for both new and repeated words."
            ),
        ),
        BuildStep(
            id="report",
            title="Format the report",
            goal="Implement top_words plus a format_report that reads like a tiny dashboard.",
            instructions=(
                "In top_words, sort the pairs: sorted(counts.items(), key=lambda pair: "
                "(-pair[1], pair[0])) — the minus sign puts big counts first, and the "
                "word itself breaks ties alphabetically so results are predictable.",
                "Slice the sorted list with [:n] and return it — asking for more words "
                "than exist just returns them all, no error needed.",
                "Add a new function format_report(text, n) that chains your pipeline: "
                "clean_words, then count_words, then loops over top_words.",
                "Start a lines list with an f-string header (total and unique word "
                "counts), then append one row per word like f\"  {word:<10} {count:>2}  "
                "\" plus \"#\" * count — the # bar makes big counts visible at a glance.",
                "Return \"\\n\".join(lines) so the caller gets one printable string "
                "instead of the function printing things itself.",
            ),
            lesson_ids=("06-data-structures", "18-clean-code"),
            checks=(
                StepCheck("defines_function", "format_report", "Add a format_report(text, n) function."),
                StepCheck("calls", "sorted", "Sort the (word, count) pairs with sorted()."),
                StepCheck("uses", "f-string", "Build the report lines with f-strings."),
            ),
            tests=(
                "counts_demo = {\"apple\": 3, \"pear\": 1, \"kiwi\": 3, \"plum\": 2}\n"
                "assert top_words(counts_demo, 2) == [(\"apple\", 3), (\"kiwi\", 3)], \"ties break alphabetically\"\n"
                "assert top_words(counts_demo, 10) == [(\"apple\", 3), (\"kiwi\", 3), (\"plum\", 2), (\"pear\", 1)]\n"
                "report_demo = format_report(\"Dog dog cat.\", 2)\n"
                "assert \"dog\" in report_demo and \"cat\" in report_demo\n"
                "assert len(report_demo.splitlines()) == 3, \"expected a header line plus one row per word\"\n"
            ),
            sample_solution=_TEXT_STEP4,
            hint=(
                "Sorting by the tuple (-count, word) gets both orders in a single "
                "sorted() call — no second pass needed."
            ),
        ),
        BuildStep(
            id="demo",
            title="Demo with proof",
            goal="Add run_checks() with your own asserts, then a main-guard demo that prints the report.",
            instructions=(
                "Write def run_checks(): containing assert lines that pin down behavior "
                "YOU care about — e.g. clean_words(\"\") == [], clean_words(None) == [], "
                "counts for a tiny known string, and a top_words tie-break.",
                "End run_checks with print(\"All checks passed.\") so a silent run still "
                "tells you the asserts actually executed.",
                "At the bottom, add if __name__ == \"__main__\": and inside it call "
                "run_checks() first, then print(format_report(SAMPLE_TEXT, 5)).",
                "Why the guard? It means importing text_analyzer from another file "
                "won't print anything — the demo only runs when this file IS the "
                "program.",
                "Run it: checks pass, then your word-frequency dashboard appears. That "
                "is the whole capstone, proven and demoed.",
            ),
            lesson_ids=("07-debugging-tests", "21-capstone-text-analyzer"),
            checks=(
                StepCheck("defines_function", "run_checks", "Add a run_checks() function."),
                StepCheck("uses", "assert", "Put your own assert lines inside run_checks."),
                StepCheck("uses", "main-guard", 'Finish with an if __name__ == "__main__": demo block.'),
            ),
            tests=(
                "assert callable(run_checks), \"Define a run_checks() function\"\n"
                "run_checks()\n"
                "final_report = format_report(SAMPLE_TEXT, 5)\n"
                "assert final_report.splitlines()[0].startswith(\"Top 5\")\n"
                "assert len(final_report.splitlines()) == 6, \"header plus five word rows\"\n"
                "assert \"the\" in final_report, \"'the' should top the sample text\"\n"
            ),
            sample_solution=_TEXT_STEP5,
            hint=(
                "assert condition, \"message\" does nothing when the condition is true "
                "and stops the program with your message when it isn't — perfect for "
                "a quick self-test suite."
            ),
        ),
    ),
)


PROJECT_BUILDS: dict[str, ProjectBuild] = {
    "quiz_scorekeeper": _QUIZ_BUILD,
    "habit_tracker_json": _HABIT_BUILD,
    "prompt_coach": _PROMPT_BUILD,
    "text_analyzer": _TEXT_BUILD,
}


def build_for_project(project_id: str) -> ProjectBuild | None:
    return PROJECT_BUILDS.get(project_id)


def _build_record(progress_data: Mapping[str, Any], project_id: str) -> Mapping[str, Any]:
    record = (progress_data.get("project_builds", {}) or {}).get(project_id, {})
    return record if isinstance(record, Mapping) else {}


def saved_build_code(progress_data: Mapping[str, Any], project_id: str) -> str:
    return str(_build_record(progress_data, project_id).get("code", "") or "")


def passed_build_steps(progress_data: Mapping[str, Any], project_id: str) -> set[str]:
    steps = _build_record(progress_data, project_id).get("steps", {})
    if not isinstance(steps, Mapping):
        return set()
    return {
        str(step_id)
        for step_id, item in steps.items()
        if isinstance(item, Mapping) and item.get("status") == "Passed"
    }


def build_completion_percent(progress_data: Mapping[str, Any], build: ProjectBuild) -> float:
    if not build.steps:
        return 0.0
    passed = passed_build_steps(progress_data, build.project_id)
    done = sum(1 for step in build.steps if step.id in passed)
    return round(done / len(build.steps), 3)


def next_build_step_index(progress_data: Mapping[str, Any], build: ProjectBuild) -> int:
    passed = passed_build_steps(progress_data, build.project_id)
    for index, step in enumerate(build.steps):
        if step.id not in passed:
            return index
    return len(build.steps) - 1


def editor_seed(progress_data: Mapping[str, Any], build: ProjectBuild) -> str:
    """What the code editor should show first: saved work, else the scaffold."""
    return saved_build_code(progress_data, build.project_id) or build.scaffold


def guide_code_before_step(build: ProjectBuild, step_index: int) -> str:
    """The guide's version of the program just before ``step_index`` starts."""
    if step_index <= 0:
        return build.scaffold
    return build.steps[step_index - 1].sample_solution
