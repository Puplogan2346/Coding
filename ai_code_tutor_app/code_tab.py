"""Code Lab tab — coding challenge, optional local test runner, AI hints.

No dropdown-style reveals: the tests, hints, and sample solution live behind an
iOS-style tile switcher (one panel at a time) instead of stacked expanders.
Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from ai_tutor import ai_is_configured, call_ai_tutor
from code_runner import code_runner_enabled, run_python_with_tests
from ui_components import select_pace_control

PANEL_TESTS = "🧪 Tests"
PANEL_HINTS = "💡 Hints"
PANEL_SOLUTION = "✅ Sample solution"


def render_code_tab(lesson) -> None:
    st.header(f"💻 Code Lab: {lesson.title}")
    challenge = lesson.challenge
    st.write(challenge.prompt)
    st.caption("Try for 8-10 focused minutes before opening hints. The goal is practice, not perfection.")

    user_code = st.text_area(
        "Your code",
        value=challenge.starter_code,
        height=280,
        key=f"code_{lesson.id}",
    )

    # Tile switcher instead of stacked expanders: tap to flip the panel.
    panel = select_pace_control(
        "Need a nudge?",
        [PANEL_TESTS, PANEL_HINTS, PANEL_SOLUTION],
        index=0,
        key=f"code_panel_{lesson.id}",
        help_text="Tests show what your code must do. Hints nudge. The solution is for after a real attempt.",
    ) or PANEL_TESTS

    if panel == PANEL_HINTS:
        for hint in challenge.hints:
            st.write(f"- {hint}")
        st.caption("Stuck after the hints? Flip to ✅ Sample solution and study it line by line.")
    elif panel == PANEL_SOLUTION:
        st.code(challenge.sample_solution, language="python")
        st.caption("Read it, then rewrite it from memory in the box above — that's the rep that sticks.")
    else:
        st.code(challenge.tests, language="python")
        st.caption("Your function passes when every assert is true.")

    runner_on = code_runner_enabled()
    if not runner_on:
        st.info(
            "✍️ Write your solution above, then check it against the ✅ sample. "
            "To run the tests right here, launch the app locally with `ALLOW_CODE_RUNNER=true` — "
            "or paste your code into any Python editor or a free online runner (e.g. replit.com). "
            "The in-app runner stays off so the shared app is safe for everyone."
        )
    else:
        st.warning(
            "Local runner is enabled. This is for your own machine only, not a secure public sandbox."
        )
        if st.button("Run lesson tests", type="primary"):
            result = run_python_with_tests(user_code, challenge.tests)
            if result.ok:
                st.success("Tests passed.")
            else:
                st.error("Tests failed.")
            if result.stdout:
                st.subheader("Output")
                st.code(result.stdout)
            if result.stderr:
                st.subheader("Errors")
                st.code(result.stderr)

    ai_ready = ai_is_configured()
    if st.button(
        "🤖 Ask AI for a hint on my code",
        disabled=not ai_ready,
        help="Add OPENAI_API_KEY to enable this." if not ai_ready else None,
        use_container_width=True,
    ):
        prompt = (
            "Give me one helpful hint for this coding challenge without giving the full solution.\n\n"
            f"Challenge: {challenge.prompt}\n\n"
            f"My code:\n```python\n{user_code}\n```"
        )
        response = call_ai_tutor(
            [{"role": "user", "content": prompt}],
            lesson_title=lesson.title,
            lesson_level=lesson.level,
        )
        st.write(response)
    if not ai_ready:
        st.caption("Connect the AI tutor to get code hints. Until then, use the built-in hints and sample solution.")
