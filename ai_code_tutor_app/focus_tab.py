"""Focus Coach tab — ADHD-friendly session design.

Part of the Today group. ``render_focus_tab`` is the entry point; ``app.py``
calls it from inside its ``with focus_tab:`` block. Imports come straight from
the leaf domain modules so there is no dependency back on ``app.py``.
"""
from __future__ import annotations

import streamlit as st

from focus_coach import (
    ADHD_DESIGN_PRINCIPLES,
    ENERGY_LEVELS,
    FOCUS_LEVELS,
    body_double_script,
    focus_blocks,
    focus_checkin_score,
    recommended_focus_mode,
    total_focus_minutes,
)
from progress import (
    add_parking_lot_item,
    close_parking_lot_item,
    record_focus_checkin,
    save_focus_preferences,
    save_progress,
)
from study_plan import next_mission
from ui_components import render_focus_blocks
from ui_safety import safe_html_text, truncate_text


def open_parking_lot_items(progress_data: dict) -> list[tuple[int, dict]]:
    return [
        (index, item)
        for index, item in enumerate(progress_data.get("parking_lot", []) or [])
        if item.get("status", "Open") == "Open"
    ]


def render_focus_tab(progress_data: dict, progress_path, lesson) -> None:
    st.header("Focus Coach: ADHD-friendly coding sessions")
    st.write(
        "This section turns coding into small, visible, low-pressure actions. "
        "It is not medical advice; it is a study-design layer for focus, memory, and momentum."
    )

    pref = progress_data.get("focus_preferences", {})
    pref_cols = st.columns(5)
    with pref_cols[0]:
        default_minutes = st.selectbox("Default session", [10, 30, 45], index=[10, 30, 45].index(int(pref.get("default_minutes", 30))), format_func=lambda x: f"{x} min")
    with pref_cols[1]:
        adhd_mode = st.checkbox("ADHD-friendly mode", value=bool(pref.get("adhd_friendly_mode", True)))
    with pref_cols[2]:
        low_stim = st.checkbox("Low-stimulation UI", value=bool(pref.get("low_stimulation_mode", False)))
    with pref_cols[3]:
        break_reminders = st.checkbox("Break reminders", value=bool(pref.get("break_reminders", True)))
    with pref_cols[4]:
        reward_style = st.selectbox("Reward style", ["Tiny wins", "Badges", "Quiet progress"], index=["Tiny wins", "Badges", "Quiet progress"].index(pref.get("reward_style", "Tiny wins") if pref.get("reward_style", "Tiny wins") in ["Tiny wins", "Badges", "Quiet progress"] else "Tiny wins"))

    if st.button("Save focus preferences"):
        save_focus_preferences(
            progress_data,
            {
                "default_minutes": default_minutes,
                "adhd_friendly_mode": adhd_mode,
                "low_stimulation_mode": low_stim,
                "break_reminders": break_reminders,
                "reward_style": reward_style,
            },
        )
        save_progress(progress_data, progress_path)
        st.success("Focus preferences saved.")
        st.rerun()

    coach_cols = st.columns([1.15, 1])
    with coach_cols[0]:
        st.subheader("Build your next session")
        energy = st.selectbox("Energy right now", ENERGY_LEVELS, index=1, key="focus_tab_energy")
        available_minutes = st.slider("Minutes available", 10, 45, int(pref.get("default_minutes", 30)), step=5)
        mode = recommended_focus_mode(energy, available_minutes)
        blocks = focus_blocks(mode.minutes, energy)
        st.info(f"Recommended: {mode.title} - {mode.summary}")
        st.caption(f"This plan totals {total_focus_minutes(blocks)} minutes.")
        render_focus_blocks(blocks)

        with st.expander("Body-double script"):
            for line in body_double_script(next_mission(progress_data).title):
                st.write(f"- {line}")

    with coach_cols[1]:
        st.subheader("Parking lot")
        st.caption("Put distracting ideas here so you do not have to chase them mid-session.")
        thought = st.text_input("Distracting thought or side quest", key="focus_parking_lot_input")
        if st.button("Park this thought"):
            if add_parking_lot_item(progress_data, thought, lesson_id=lesson.id, source="Focus Coach"):
                save_progress(progress_data, progress_path)
                st.success("Parked. Return to the next tiny action.")
                st.rerun()
            else:
                st.warning("Write a thought first, even a messy one.")

        open_items = open_parking_lot_items(progress_data)
        if not open_items:
            st.info("Parking lot is empty.")
        for index, item in open_items[-6:]:
            safe_thought = safe_html_text(truncate_text(item.get("thought", ""), 300))
            st.markdown(f"<div class='parking-item'>{safe_thought}</div>", unsafe_allow_html=True)
            if st.button("Close", key=f"close_parking_{index}"):
                close_parking_lot_item(progress_data, index)
                save_progress(progress_data, progress_path)
                st.rerun()

        st.subheader("Focus check-in")
        focus_level = st.selectbox("Focus level", FOCUS_LEVELS, index=1, key="focus_tab_level")
        blockers = st.text_area("What might pull you away?", height=80, key="focus_tab_blockers")
        win = st.text_area("What tiny win would count today?", height=80, key="focus_tab_win")
        if st.button("Save focus check-in"):
            record_focus_checkin(progress_data, energy, focus_level, blockers, win)
            save_progress(progress_data, progress_path)
            st.success(f"Check-in saved. Focus score: {focus_checkin_score(energy, focus_level)}/6.")

    st.subheader("Design rules used in this app")
    for principle in ADHD_DESIGN_PRINCIPLES:
        st.write(f"- {principle}")
