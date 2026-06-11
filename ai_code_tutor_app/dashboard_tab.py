"""Dashboard tab — progress overview and curriculum map.

Part of the Today group. ``render_dashboard_tab`` is the entry point; ``app.py``
calls it from inside its ``with dashboard_tab:`` block. This tab is read-only
(no saves), so it does not take a ``progress_path``. Imports come straight from
the leaf domain modules so there is no dependency back on ``app.py``.
"""
from __future__ import annotations

from statistics import mean

import streamlit as st

from curriculum import LESSONS
from experience import streak_microcopy
from gamification import calculate_xp, level_for_xp
from official_ai_resources import official_resource_stats
from progress import completed_daily_missions_count
from study_plan import DAILY_PLAN, next_mission
from ui_components import render_badge_shelf, render_card, render_level_progress, render_step


def get_quiz_average(progress_data: dict) -> float:
    scores = progress_data.get("quiz_scores", {}).values()
    percentages = [item.get("percent", 0) for item in scores]
    return round(mean(percentages), 1) if percentages else 0.0


def get_best_prompt_score(progress_data: dict) -> int:
    scores = [item.get("score", 0) for item in progress_data.get("prompt_scores", [])]
    return max(scores) if scores else 0


def render_dashboard_tab(progress_data: dict, lesson, next_lesson) -> None:
    completed_lessons = set(progress_data.get("completed_lessons", []))
    completed_count = len(completed_lessons)
    if completed_count == 0:
        st.success("Welcome. This profile is brand new, so start with Lesson 1 and use the checklist below.")

    with st.expander("Start here: your first 10 minutes", expanded=completed_count == 0):
        intro_cols = st.columns(4)
        with intro_cols[0]:
            render_step(1, "Read", "Open the Lessons tab and read the current lesson once without memorizing.")
        with intro_cols[1]:
            render_step(2, "Check", "Take the quiz in the Practice tab. Misses are useful because they tell you what to review.")
        with intro_cols[2]:
            render_step(3, "Practice", "Try Code Lab (Practice tab) from the starter code before viewing the sample solution.")
        with intro_cols[3]:
            render_step(4, "Prompt", "Use Prompt Lab (More tab) to ask for help with context, constraints, and verification.")

    official_stats = official_resource_stats(progress_data)
    metric_cols = st.columns(6)
    metric_cols[0].metric("Lessons complete", f"{completed_count}/{len(LESSONS)}")
    metric_cols[1].metric("Daily missions", f"{completed_daily_missions_count(progress_data)}/{len(DAILY_PLAN)}")
    metric_cols[2].metric("Study streak", f"{progress_data.get('study_streak', 0)} days")
    metric_cols[3].metric("Quiz average", f"{get_quiz_average(progress_data)}%")
    metric_cols[4].metric("Best prompt score", f"{get_best_prompt_score(progress_data)}/10")
    metric_cols[5].metric("AI resources done", f"{official_stats['completed']}/{official_stats['total']}")

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Recommended next step")
        current_mission = next_mission(progress_data)
        render_card(
            f"Day {current_mission.day}: {current_mission.title}",
            f"30-minute mission. Focus: {current_mission.focus}. Proof: {current_mission.proof}",
            "success-soft" if current_mission.lesson_id == lesson.id else "",
        )
        render_card(
            next_lesson.title,
            f"Next incomplete lesson. Estimated lesson time: {next_lesson.time_minutes} minutes. Focus: {st.session_state.get('study_focus', 'Learn')}.",
        )
        if st.button("Select recommended lesson", type="primary"):
            st.session_state.selected_lesson_id = next_lesson.id
            st.rerun()
        st.caption("Sets the active lesson — then open the 📚 Lessons tab to study it.")

        st.subheader("Curriculum map")
        for index, item in enumerate(LESSONS, start=1):
            status = "✅ Complete" if item.id in completed_lessons else "⬜ Not complete"
            score = progress_data.get("quiz_scores", {}).get(item.id)
            score_text = f"Quiz: {score['percent']}%" if score else "Quiz: not taken"
            st.markdown(
                f"""
<div class="lesson-row">
    <strong>{index}. {item.title}</strong><br>
    <span class="small-muted">{item.level} · {item.time_minutes} min · {status} · {score_text}</span>
</div>
""".strip(),
                unsafe_allow_html=True,
            )

    with right:
        st.subheader("How to use this app")
        st.markdown(
            """
1. Start in the Today tab and follow the 30-minute mission.
2. Read, quiz, code, then reflect before moving on.
3. Use review days to revisit older lessons from memory.
4. Use the Review tab's mixed quiz and flashcards to keep old lessons fresh.
5. Save a tiny win each day so the app becomes your learning journal.
""".strip()
        )
        st.subheader("Current level")
        xp = calculate_xp(progress_data)
        render_card(level_for_xp(xp), f"{xp} XP earned from lessons, quizzes, prompts, daily missions, and AI resources.")
        render_level_progress(xp)
        st.caption(streak_microcopy(int(progress_data.get("study_streak", 0) or 0), int(progress_data.get("longest_streak", 0) or 0)))
        with st.expander("Unlocked badges", expanded=False):
            render_badge_shelf(progress_data)

        ai_stats = official_resource_stats(progress_data)
        st.subheader("Official AI track")
        render_card(
            "External learning progress",
            (
                f"{ai_stats['started']} started, {ai_stats['completed']} completed, "
                f"{ai_stats['certificate_options']} certificate/credential options across "
                f"{ai_stats['total']} curated official resources."
            ),
        )
        st.info("Keep API keys out of code files — use environment variables or your platform's secrets panel.")
