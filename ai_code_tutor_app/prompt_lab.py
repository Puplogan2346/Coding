from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PromptCriterion:
    name: str
    points: int
    passed: bool
    feedback: str


@dataclass(frozen=True)
class PromptScore:
    score: int
    max_score: int
    criteria: List[PromptCriterion]
    summary: str


def _contains_any(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in words)


def score_prompt(prompt: str) -> PromptScore:
    text = prompt.strip()
    criteria: List[PromptCriterion] = []

    checks = [
        (
            "Clear task",
            2,
            len(text) >= 25 and _contains_any(text, ["help", "create", "explain", "write", "review", "debug", "build", "teach"]),
            "State the exact job you want the AI to do.",
        ),
        (
            "Context",
            2,
            _contains_any(text, ["context", "i know", "i am", "beginner", "project", "goal", "background"]),
            "Add background: your skill level, project situation, or what you already tried.",
        ),
        (
            "Constraints",
            2,
            _contains_any(text, ["do not", "avoid", "must", "only", "limit", "constraint", "requirements"]),
            "Add rules or limits, such as beginner-friendly language or no final answer yet.",
        ),
        (
            "Output format",
            2,
            _contains_any(text, ["format", "table", "bullets", "json", "steps", "checklist", "example"]),
            "Tell the AI how to structure the answer: steps, bullets, table, code block, etc.",
        ),
        (
            "Example or input",
            1,
            _contains_any(text, ["example", "input", "code", "error", "sample", "```"]),
            "Include a small example, code snippet, input, output, or error message.",
        ),
        (
            "Verification request",
            1,
            _contains_any(text, ["test", "verify", "check", "edge case", "explain why", "rubric"]),
            "Ask for tests, edge cases, or a reasoned explanation so you can verify the answer.",
        ),
    ]

    total = 0
    max_score = 0
    for name, points, passed, feedback in checks:
        max_score += points
        if passed:
            total += points
            criteria.append(PromptCriterion(name, points, True, "Looks good."))
        else:
            criteria.append(PromptCriterion(name, points, False, feedback))

    if total >= 9:
        summary = "Strong prompt. It gives the model enough direction to be useful and testable."
    elif total >= 6:
        summary = "Decent prompt. Add more context, constraints, or output format to improve it."
    else:
        summary = "Early draft. Make the task more specific and include context plus desired output format."

    return PromptScore(score=total, max_score=max_score, criteria=criteria, summary=summary)


def improved_prompt_template(topic: str = "Python loops") -> str:
    return f"""Role: Act as a patient Python tutor.
Task: Teach me {topic} from a beginner perspective.
Context: I know variables and if statements, but I get confused when code repeats.
Constraints: Do not skip steps. Use simple language. Do not give me a huge project yet.
Output format: Use 5 short sections: concept, tiny example, common mistake, practice task, check-in question.
Verification: Include one quick question that proves I understood the concept.
""".strip()
