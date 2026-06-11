"""Notes tab — per-lesson private notes.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from progress import save_note, save_progress


def render_notes_tab(progress_data: dict, progress_path, lesson) -> None:
    st.header(f"📝 Notes: {lesson.title}")
    current_note = progress_data.get("notes", {}).get(lesson.id, "")
    note_text = st.text_area(
        "Write your own notes, questions, and reflections",
        value=current_note,
        height=320,
        key=f"notes_{lesson.id}",
    )
    if st.button("Save notes"):
        save_note(progress_data, lesson.id, note_text)
        save_progress(progress_data, progress_path)
        st.success("Notes saved.")
