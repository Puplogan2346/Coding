"""Lesson tab — a clickable lesson list plus the open lesson's content.

Replaces the old sidebar ``selectbox`` dropdown: learners now see every lesson
as a tappable row with a clear ✅ / ▶ / ○ status and a "Start Lesson 1" entry
point. Imports come straight from the leaf domain modules so there is no
dependency back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from ai_tutor import ai_is_configured, call_ai_tutor
from curriculum import LESSONS
from learning_path import first_incomplete_lesson_id
from progress import mark_lesson_complete, save_progress
from ui_components import render_status_pills


def _select_lesson(lesson_id: str) -> None:
    """Set the active lesson and rerun so every lesson-bound tab follows it."""
    st.session_state.selected_lesson_id = lesson_id
    st.rerun()


def render_lesson_picker(progress_data: dict) -> None:
    """Clickable list of all lessons — replaces the old sidebar dropdown.

    Reads progress only to show status, and writes the navigation choice
    (``selected_lesson_id``) to session state. No progress is mutated and nothing
    is saved here, so it stays a thin per-tab control.
    """
    completed = set(progress_data.get("completed_lessons", []) or [])
    next_id = first_incomplete_lesson_id(progress_data)
    current_id = st.session_state.get("selected_lesson_id") or next_id

    # "Start here / Continue" call to action.
    if not completed:
        cta = LESSONS[0]
        st.success("New here? Start with **Lesson 1 — Python mindset**. It takes about 25 minutes.")
        cta_label = f"▶  Start Lesson 1 — {cta.title}"
    else:
        cta = next((les for les in LESSONS if les.id == next_id), LESSONS[-1])
        st.info(f"You've finished **{len(completed)} of {len(LESSONS)}** lessons. Pick up where you left off.")
        cta_label = f"▶  Continue — {cta.title}"
    if st.button(cta_label, type="primary", key="lesson_cta", use_container_width=True):
        _select_lesson(cta.id)

    st.markdown("**All lessons** — tap one to open it. Your Quiz and Code Lab follow the lesson you pick.")
    for index, lesson_item in enumerate(LESSONS):
        if lesson_item.id in completed:
            mark = "✅"
        elif lesson_item.id == current_id:
            mark = "▶"
        else:
            mark = "○"
        label = (
            f"{mark}   {index + 1}. {lesson_item.title}"
            f"   ·   {lesson_item.level} · ~{lesson_item.time_minutes} min"
        )
        if st.button(label, key=f"pick_{lesson_item.id}", use_container_width=True):
            _select_lesson(lesson_item.id)


def render_lesson_tab(progress_data: dict, progress_path, lesson, lesson_complete: bool) -> None:
    st.header("📚 Python Lessons")
    render_lesson_picker(progress_data)

    st.divider()
    st.subheader(f"📖 Now open: {lesson.title}")
    render_status_pills(lesson.level, lesson.time_minutes, lesson_complete)
    st.info("30-minute habit tip: read for 10 minutes, code for 10 minutes, quiz or review for 5 minutes, then write a 5-minute reflection.")

    st.subheader("Objectives")
    for objective in lesson.objectives:
        st.write(f"- {objective}")

    st.subheader("Lesson")
    st.markdown(lesson.explanation)

    st.subheader("Key terms")
    st.write(" ".join(f"`{term}`" for term in lesson.key_terms))

    st.info(f"Prompt skill: {lesson.prompt_skill}")

    action_cols = st.columns([1, 1.2])
    with action_cols[0]:
        if lesson_complete:
            st.success("You marked this lesson complete.")
        elif st.button("Mark lesson complete", type="primary"):
            mark_lesson_complete(progress_data, lesson.id)
            save_progress(progress_data, progress_path)
            st.success("Lesson marked complete.")
            st.rerun()
    with action_cols[1]:
        ai_ready = ai_is_configured()
        if st.button(
            "Ask AI to explain this lesson in simpler words",
            disabled=not ai_ready,
            help="Add OPENAI_API_KEY to enable this." if not ai_ready else None,
        ):
            prompt = (
                f"Explain the lesson '{lesson.title}' in beginner-friendly language. "
                "Use a tiny Python example and one check-in question."
            )
            st.write(call_ai_tutor([{"role": "user", "content": prompt}], lesson.title, lesson.level))
        if not ai_ready:
            st.caption("AI buttons are disabled until OPENAI_API_KEY is configured. The rest of the app works without AI.")
