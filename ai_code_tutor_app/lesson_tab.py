"""Lesson tab — a list-and-detail layout.

The lesson list lives in a compact, scrollable column on the left; the open
lesson's content shows on the right and is always visible. This replaces the old
single-column design where you had to scroll past every lesson button to reach
the content. Imports come straight from the leaf domain modules so there is no
dependency back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from ai_tutor import ai_is_configured, call_ai_tutor
from curriculum import LESSONS
from glossary import vocab_for_terms
from learning_path import first_incomplete_lesson_id
from lesson_extras import common_mistake, worked_example
from progress import mark_lesson_complete, save_progress
from ui_components import render_status_pills


def _select_lesson(lesson_id: str) -> None:
    """Set the active lesson and rerun so every lesson-bound tab follows it."""
    st.session_state.selected_lesson_id = lesson_id
    st.rerun()


def render_lesson_list(progress_data: dict, current_id: str) -> None:
    """Left column: Start/Continue CTA + a scrollable, clickable lesson list."""
    # Marker for the mobile CSS in app.py: on narrow screens the columns stack,
    # and this lets the open lesson's content render above the list.
    st.markdown('<div class="lesson-list-marker"></div>', unsafe_allow_html=True)
    completed = set(progress_data.get("completed_lessons", []) or [])

    if not completed:
        cta_label, cta_target = "▶ Start Lesson 1", LESSONS[0].id
    else:
        cta_label, cta_target = "▶ Continue where you left off", first_incomplete_lesson_id(progress_data)
    if st.button(cta_label, type="primary", use_container_width=True, key="lesson_cta"):
        _select_lesson(cta_target)

    st.caption("Tap a lesson to open it →")
    # Fixed-height scroll box keeps the list compact so the lesson content on the
    # right is never pushed off-screen.
    with st.container(height=440):
        for index, item in enumerate(LESSONS):
            is_current = item.id == current_id
            mark = "✅" if item.id in completed else ("📖" if is_current else "○")
            label = f"{mark}  {index + 1}. {item.title}"
            if st.button(
                label,
                key=f"pick_{item.id}",
                use_container_width=True,
                type="primary" if is_current else "secondary",
            ):
                _select_lesson(item.id)


def render_lesson_tab(progress_data: dict, progress_path, lesson, lesson_complete: bool) -> None:
    st.header("📚 Python Lessons")

    completed = set(progress_data.get("completed_lessons", []) or [])
    total = len(LESSONS)
    st.progress(len(completed) / total if total else 0.0)
    st.caption(f"{len(completed)} of {total} lessons complete")

    list_col, content_col = st.columns([1, 2.2], gap="large")

    with list_col:
        render_lesson_list(progress_data, lesson.id)

    with content_col:
        current_index = next((i for i, item in enumerate(LESSONS) if item.id == lesson.id), 0)
        ai_ready = ai_is_configured()

        # Previous / Next navigation (page scrolls to top on rerun, so this stays
        # visible right after each jump).
        nav_prev, nav_next = st.columns(2)
        with nav_prev:
            if st.button("← Previous", use_container_width=True, disabled=current_index == 0, key="lesson_prev"):
                _select_lesson(LESSONS[current_index - 1].id)
        with nav_next:
            if st.button("Next →", use_container_width=True, disabled=current_index >= total - 1, key="lesson_next"):
                _select_lesson(LESSONS[current_index + 1].id)

        st.subheader(f"{current_index + 1}. {lesson.title}")
        render_status_pills(lesson.level, lesson.time_minutes, lesson_complete)
        if lesson_complete:
            st.success("✅ You completed this lesson.")

        st.markdown("**What you'll learn**")
        for objective in lesson.objectives:
            st.write(f"- {objective}")

        st.markdown("### Lesson")
        st.markdown(lesson.explanation)

        example = worked_example(lesson.id)
        if example:
            st.markdown("### 🔎 Worked example")
            st.markdown(example)

        mistake = common_mistake(lesson.id)
        if mistake:
            st.warning(f"⚠️ **Common mistake:** {mistake}")

        st.markdown("### 📖 Vocabulary")
        st.caption("Plain-English definitions for the key terms in this lesson.")
        for term, definition in vocab_for_terms(lesson.key_terms):
            st.markdown(f"- **{term}** — {definition}")

        st.info(f"💡 Prompt skill: {lesson.prompt_skill}")

        st.markdown("---")
        action_cols = st.columns(2)
        with action_cols[0]:
            if lesson_complete:
                st.button("✅ Completed", disabled=True, use_container_width=True, key="lesson_done")
            elif st.button("Mark lesson complete", type="primary", use_container_width=True, key="lesson_complete_btn"):
                mark_lesson_complete(progress_data, lesson.id)
                save_progress(progress_data, progress_path)
                st.success("Lesson marked complete.")
                st.rerun()
        with action_cols[1]:
            if st.button(
                "🤖 Explain this simpler",
                use_container_width=True,
                disabled=not ai_ready,
                help="Add OPENAI_API_KEY to enable this." if not ai_ready else None,
                key="lesson_ai_explain",
            ):
                prompt = (
                    f"Explain the lesson '{lesson.title}' in beginner-friendly language. "
                    "Use a tiny Python example and one check-in question."
                )
                st.write(call_ai_tutor([{"role": "user", "content": prompt}], lesson.title, lesson.level))

        st.caption("Tip: read for ~10 min, do the quiz & Code Lab in the Practice tab, then write a 5-min reflection.")
        if not ai_ready:
            st.caption("AI buttons turn on once OPENAI_API_KEY is set — everything else works without it.")
