from __future__ import annotations

import os
from typing import Dict, List, Optional

DEFAULT_MODEL = "gpt-5.5"

SYSTEM_PROMPT = """
You are a patient Python, coding, and prompt-engineering tutor inside a self-study app.
Your teaching style:
- Explain in beginner-friendly language first.
- Prefer small examples over long lectures.
- Ask one check-in question when useful.
- Do not shame the learner for mistakes.
- When reviewing code, point out the exact line or idea that matters.
- When helping with prompts, improve clarity around task, context, constraints, examples, output format, and verification.
- Do not claim code is correct unless you can explain why or suggest a test.
""".strip()


def get_secret(name: str) -> Optional[str]:
    env_value = os.getenv(name)
    if env_value:
        return env_value

    try:
        import streamlit as st

        value = st.secrets.get(name)  # type: ignore[attr-defined]
        if value:
            return str(value)
    except Exception:
        return None

    return None


def ai_is_configured() -> bool:
    return bool(get_secret("OPENAI_API_KEY"))


def configured_model() -> str:
    return os.getenv("OPENAI_MODEL") or get_secret("OPENAI_MODEL") or DEFAULT_MODEL


def _sanitize_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    sanitized: List[Dict[str, str]] = []
    for message in messages[-12:]:
        role = message.get("role", "user")
        if role not in {"user", "assistant", "developer"}:
            role = "user"
        content = str(message.get("content", "")).strip()
        if content:
            sanitized.append({"role": role, "content": content})
    return sanitized


def call_ai_tutor(
    messages: List[Dict[str, str]],
    lesson_title: str,
    lesson_level: str,
    model: Optional[str] = None,
) -> str:
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        return (
            "AI tutor is not connected yet. Add OPENAI_API_KEY as an environment variable "
            "or in .streamlit/secrets.toml, then restart the app."
        )

    try:
        from openai import OpenAI
    except ImportError:
        return "The OpenAI Python package is not installed. Run: pip install -r requirements.txt"

    client = OpenAI(api_key=api_key)
    selected_model = model or configured_model()
    context = (
        f"Current lesson: {lesson_title}\n"
        f"Current level: {lesson_level}\n"
        "The learner is building skill from beginner toward intermediate Python and AI prompting."
    )
    input_messages = [{"role": "developer", "content": context}] + _sanitize_messages(messages)

    try:
        response = client.responses.create(
            model=selected_model,
            instructions=SYSTEM_PROMPT,
            input=input_messages,
        )
        return response.output_text
    except Exception as exc:
        return (
            "AI tutor request failed. Check your API key, model name, billing/access, and internet connection.\n\n"
            f"Error: {exc}"
        )


def improve_prompt_with_ai(prompt: str, lesson_title: str = "Prompt engineering") -> str:
    messages = [
        {
            "role": "user",
            "content": (
                "Review and improve this prompt for learning/coding. "
                "Return: 1) score out of 10, 2) what is missing, 3) improved prompt.\n\n"
                f"Prompt:\n{prompt}"
            ),
        }
    ]
    return call_ai_tutor(messages, lesson_title=lesson_title, lesson_level="Beginner to Intermediate")
