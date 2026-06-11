"""Prompt Lab tab — prompt rubric scoring and AI prompt improvement.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from ai_tutor import ai_is_configured, improve_prompt_with_ai
from progress import record_prompt_score, save_progress
from prompt_lab import improved_prompt_template, score_prompt


def render_prompt_tab(progress_data: dict, progress_path, lesson) -> None:
    st.header("💡 Prompt Lab")
    st.write("Practice writing better prompts for coding, learning, debugging, and AI app building.")

    prompt_text = st.text_area(
        "Write or paste a prompt",
        value=improved_prompt_template("Python functions"),
        height=240,
        key="prompt_lab_text",
    )

    score_col, ai_col = st.columns(2)
    with score_col:
        if st.button("Score prompt", type="primary"):
            result = score_prompt(prompt_text)
            record_prompt_score(progress_data, result.score, prompt_text)
            save_progress(progress_data, progress_path)
            st.metric("Prompt score", f"{result.score}/{result.max_score}")
            st.progress(result.score / result.max_score)
            st.write(result.summary)
            for criterion in result.criteria:
                if criterion.passed:
                    st.success(f"{criterion.name}: +{criterion.points} - {criterion.feedback}")
                else:
                    st.warning(f"{criterion.name}: {criterion.feedback}")
    with ai_col:
        ai_ready = ai_is_configured()
        if st.button(
            "Ask AI to improve this prompt",
            disabled=not ai_ready,
            help="Add OPENAI_API_KEY to enable this." if not ai_ready else None,
        ):
            improved = improve_prompt_with_ai(prompt_text, lesson_title=lesson.title)
            st.subheader("AI feedback")
            st.write(improved)
        if not ai_ready:
            st.caption("The built-in rubric works offline. AI rewriting turns on after you add OPENAI_API_KEY.")

    if st.toggle("Prompt formula"):
        st.markdown(
            """
Use this formula:

```text
Role: Who should the AI act as?
Task: What exact job should it do?
Context: What does it need to know about you, the code, or the situation?
Constraints: What should it avoid or follow?
Example/Input: What code, error, sample input, or desired output can you provide?
Output format: How should the answer be structured?
Verification: How can the answer be checked?
```
""".strip()
        )
