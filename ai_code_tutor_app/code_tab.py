"""Code Lab tab — coding challenge, optional local test runner, AI hints.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from ai_tutor import ai_is_configured, call_ai_tutor
from code_runner import code_runner_enabled, run_python_with_tests


def render_code_tab(lesson) -> None:
    st.header(f"Code Lab: {lesson.title}")
    challenge = lesson.challenge
    st.write(challenge.prompt)
    st.caption("Try for 8-10 focused minutes before opening hints. The goal is practice, not perfection.")

    with st.expander("Hints"):
        for hint in challenge.hints:
            st.write(f"- {hint}")

    user_code = st.text_area(
        "Your code",
        value=challenge.starter_code,
        height=280,
        key=f"code_{lesson.id}",
    )

    with st.expander("View tests"):
        st.code(challenge.tests, language="python")

    runner_on = code_runner_enabled()
    if not runner_on:
        st.info(
            "The code runner is off. To run tests locally, start the app with "
            "ALLOW_CODE_RUNNER=true. Keep it off for public deployments."
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

    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("Show sample solution"):
            st.code(challenge.sample_solution, language="python")
    with col_b:
        ai_ready = ai_is_configured()
        if st.button(
            "Ask AI for a hint on my code",
            disabled=not ai_ready,
            help="Add OPENAI_API_KEY to enable this." if not ai_ready else None,
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
