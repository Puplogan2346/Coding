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
from ui_components import render_focus_blocks, select_pace_control
from ui_safety import safe_html_text, truncate_text


def open_parking_lot_items(progress_data: dict) -> list[tuple[int, dict]]:
    return [
        (index, item)
        for index, item in enumerate(progress_data.get("parking_lot", []) or [])
        if item.get("status", "Open") == "Open"
    ]


def render_focus_tab(progress_data: dict, progress_path, lesson) -> None:
    st.header("🧘 Focus Coach: ADHD-friendly coding sessions")
    st.write(
        "This section turns coding into small, visible, low-pressure actions. "
        "It is not medical advice; it is a study-design layer for focus, memory, and momentum."
    )

    pref = progress_data.get("focus_preferences", {})
    saved_minutes = int(pref.get("default_minutes", 30))
    minute_labels = ["10 min", "30 min", "45 min"]
    saved_minutes_label = f"{saved_minutes} min" if f"{saved_minutes} min" in minute_labels else "30 min"
    pref_cols = st.columns([1.2, 1.2, 1.6])
    with pref_cols[0]:
        default_minutes_label = select_pace_control(
            "Default session", minute_labels, index=minute_labels.index(saved_minutes_label),
            key="focus_default_minutes", help_text="Your usual workout length.",
        ) or saved_minutes_label
        default_minutes = int(default_minutes_label.split()[0])
    with pref_cols[1]:
        reward_options = ["Tiny wins", "Badges", "Quiet progress"]
        saved_reward = pref.get("reward_style", "Tiny wins")
        reward_style = select_pace_control(
            "Reward style", reward_options,
            index=reward_options.index(saved_reward if saved_reward in reward_options else "Tiny wins"),
            key="focus_reward_style", help_text="How the app should celebrate progress.",
        ) or "Tiny wins"
    with pref_cols[2]:
        adhd_mode = st.checkbox("ADHD-friendly mode", value=bool(pref.get("adhd_friendly_mode", True)))
        low_stim = st.checkbox("Low-stimulation UI", value=bool(pref.get("low_stimulation_mode", False)))
        break_reminders = st.checkbox("Break reminders", value=bool(pref.get("break_reminders", True)))

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
        energy = select_pace_control(
            "Energy right now", list(ENERGY_LEVELS), index=1, key="focus_tab_energy",
            help_text="Sessions adapt to your fuel level.",
        ) or ENERGY_LEVELS[1]
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
        focus_level = select_pace_control(
            "Focus level", list(FOCUS_LEVELS), index=1, key="focus_tab_level",
            help_text="Where your head is at right now.",
        ) or FOCUS_LEVELS[1]
        blockers = st.text_area("What might pull you away?", height=80, key="focus_tab_blockers")
        win = st.text_area("What tiny win would count today?", height=80, key="focus_tab_win")
        if st.button("Save focus check-in"):
            record_focus_checkin(progress_data, energy, focus_level, blockers, win)
            save_progress(progress_data, progress_path)
            st.success(f"Check-in saved. Focus score: {focus_checkin_score(energy, focus_level)}/6.")

    st.subheader("Design rules used in this app")
    for principle in ADHD_DESIGN_PRINCIPLES:
        st.write(f"- {principle}")
