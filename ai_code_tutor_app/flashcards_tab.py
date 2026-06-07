"""Flashcards tab — spaced-repetition study over the glossary terms.

Shows one card at a time (term on the front, definition on the back). Answering
updates the card's Leitner box and next-due date and saves immediately, so review
results persist across sessions.
"""
from __future__ import annotations

import streamlit as st

from flashcards import ahead_terms, due_terms, next_due_date, record_result, stats
from glossary import GLOSSARY
from progress import save_progress


def _reset_card() -> None:
    st.session_state.flash_current = None
    st.session_state.flash_revealed = False


def _answer(progress_data: dict, progress_path, term: str, correct: bool) -> None:
    record_result(progress_data, term, correct)
    save_progress(progress_data, progress_path)
    _reset_card()
    st.rerun()


def render_flashcards_tab(progress_data: dict, progress_path) -> None:
    st.subheader("🃏 Flashcards — spaced repetition")
    st.caption("Review key terms. Cards you know come back later; cards you miss come back sooner.")

    card_stats = stats(progress_data)
    cols = st.columns(4)
    cols[0].metric("Total terms", card_stats["total"])
    cols[1].metric("Studied", card_stats["studied"])
    cols[2].metric("Mastered", card_stats["mastered"])
    cols[3].metric("Due now", card_stats["due"])

    ahead = bool(st.session_state.get("flash_ahead", False))
    queue = due_terms(progress_data) if not ahead else ahead_terms(progress_data)

    if not queue:
        if ahead:
            st.success("🏆 Every term is mastered. Incredible — come back when cards fall due.")
        else:
            st.success("✅ All caught up! No cards are due right now.")
            upcoming = next_due_date(progress_data)
            if upcoming:
                st.caption(f"Next cards are due on {upcoming}.")
            if ahead_terms(progress_data) and st.button("Study ahead anyway", key="flash_study_ahead"):
                st.session_state.flash_ahead = True
                _reset_card()
                st.rerun()
        return

    if ahead:
        st.caption("Studying ahead of schedule. Progress still counts.")

    current = st.session_state.get("flash_current")
    if current not in queue:
        current = queue[0]
        st.session_state.flash_current = current
        st.session_state.flash_revealed = False

    position = "Studying ahead" if ahead else f"{len(queue)} card(s) due"
    st.caption(position)

    st.markdown(
        f"""
<div class="card" style="text-align:center; min-height:120px; display:flex; align-items:center; justify-content:center;">
    <h2 style="margin:0;">{current}</h2>
</div>
""".strip(),
        unsafe_allow_html=True,
    )

    if not st.session_state.get("flash_revealed", False):
        if st.button("Show definition", type="primary", use_container_width=True, key="flash_show"):
            st.session_state.flash_revealed = True
            st.rerun()
        return

    st.info(GLOSSARY.get(current, "Definition unavailable."))
    got_col, missed_col = st.columns(2)
    with got_col:
        if st.button("✅ Got it", use_container_width=True, key="flash_got"):
            _answer(progress_data, progress_path, current, True)
    with missed_col:
        if st.button("❌ Missed it", use_container_width=True, key="flash_missed"):
            _answer(progress_data, progress_path, current, False)
