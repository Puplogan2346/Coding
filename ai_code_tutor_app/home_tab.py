"""Home tab — the command-center dashboard (first screen of the app).

Structured like a bootcamp dashboard hub: Quick Actions, an auto-generated
to-do list, current projects, newest "bugs" (mistake cards), and the next
learning resource — every section built from real progress, each pointing at
the tab where the work happens. Imports stay on leaf modules (never app.py).
"""
from __future__ import annotations

import streamlit as st

from curriculum import LESSONS
from flashcards import stats as flashcard_stats
from gamification import calculate_xp, level_for_xp
from home import build_todo_items, lesson_title, open_mistakes, project_rows
from learning_path import current_milestone_status
from official_ai_resources import next_recommended_resource, official_resource_stats
from progress import completed_daily_missions_count
from review import lessons_to_review, next_lesson_to_study
from study_plan import DAILY_PLAN
from ui_safety import h, truncate_text


def _section(title: str) -> None:
    st.markdown(f"### {title}")


def render_home_tab(progress_data: dict) -> None:
    completed = set(progress_data.get("completed_lessons", []) or [])
    xp = calculate_xp(progress_data)

    # ---- Quick glance strip ----
    glance = st.columns(4)
    glance[0].metric("Lessons", f"{len(completed)}/{len(LESSONS)}")
    glance[1].metric("Daily missions", f"{completed_daily_missions_count(progress_data)}/{len(DAILY_PLAN)}")
    glance[2].metric("Flashcards due", flashcard_stats(progress_data)["due"])
    glance[3].metric("Level", level_for_xp(xp).split(" ")[0] if level_for_xp(xp) else f"{xp} XP")

    milestone = current_milestone_status(progress_data)
    st.progress(milestone.percent)
    st.caption(f"🎯 {milestone.milestone.title} — {milestone.next_action}")

    # ---- Quick Actions ----
    _section("⚡ Quick actions")
    actions = st.columns(3)
    next_lesson = next_lesson_to_study(progress_data)
    with actions[0]:
        if st.button(f"📚 Open: {truncate_text(next_lesson.title, 34)}", use_container_width=True, type="primary", key="home_open_lesson"):
            st.session_state.selected_lesson_id = next_lesson.id
            st.rerun()
        st.caption("Sets the active lesson — then tap **📚 Lessons**.")
    with actions[1]:
        st.button("🏠 Start today's workout", use_container_width=True, disabled=True, key="home_goto_today")
        st.caption("Tap the **🏠 Today** tab to begin.")
    with actions[2]:
        due_now = flashcard_stats(progress_data)["due"]
        st.button(f"🃏 {due_now} flashcards waiting", use_container_width=True, disabled=True, key="home_goto_cards")
        st.caption("Tap **🔁 Review** to drill them.")

    home_left, home_right = st.columns([1.25, 1], gap="large")

    with home_left:
        # ---- Tasks To-Do ----
        _section("✅ Tasks to-do")
        st.caption("Auto-built from your progress — finish these and the day is won.")
        for item in build_todo_items(progress_data):
            st.markdown(
                f"""
<div class="lesson-row">
    <strong>{h(item['icon'])} {h(item['label'])}</strong><br>
    <span class="small-muted">→ {h(item['where'])} tab</span>
</div>
""".strip(),
                unsafe_allow_html=True,
            )

        # ---- Current Projects ----
        _section("🛠️ Current projects")
        for row in project_rows(progress_data)[:4]:
            badge = " · ⭐ recommended" if row["recommended"] else ""
            st.markdown(
                f"""
<div class="lesson-row">
    <strong>{h(row['title'])} — {h(row['percent'])}%{h(badge)}</strong><br>
    <span class="small-muted">{h(row['level'])} · next: {h(row['next_milestone'])}</span>
</div>
""".strip(),
                unsafe_allow_html=True,
            )

    with home_right:
        # ---- Newest Bugs (mistake notebook) ----
        _section("🐛 Newest bugs")
        st.caption("Your open mistake cards — squash them in the Today tab's mistake notebook.")
        mistakes = open_mistakes(progress_data)
        if not mistakes:
            st.success("No open bugs. Mistakes you log in the Daily Gym show up here.")
        for card in mistakes:
            st.markdown(
                f"""
<div class="review-chip warning-soft">
    <strong>{h(truncate_text(str(card.get('concept', 'Review')), 48))}</strong>
    <span>{h(truncate_text(str(card.get('mistake', '')), 90))}<br><b>Fix:</b> {h(truncate_text(str(card.get('fix', '')), 90))} · {h(lesson_title(str(card.get('lesson_id', ''))))}</span>
</div>
""".strip(),
                unsafe_allow_html=True,
            )

        # ---- Worth reviewing ----
        weak = lessons_to_review(progress_data)
        if weak:
            _section("🔁 Worth reviewing")
            for lesson in weak[:3]:
                st.markdown(
                    f"""
<div class="review-chip">
    <strong>{h(lesson.title)}</strong>
    <span>Quiz not passed yet — retake it in ✏️ Practice.</span>
</div>
""".strip(),
                    unsafe_allow_html=True,
                )

        # ---- Learning Resources ----
        _section("🎓 Learning resources")
        stats = official_resource_stats(progress_data)
        nxt = next_recommended_resource(progress_data)
        if nxt:
            st.markdown(
                f"""
<div class="review-chip">
    <strong>Next up: {h(nxt.provider)} — {h(nxt.title)}</strong>
    <span>{h(stats['started'])} started · {h(stats['completed'])} completed of {h(stats['total'])} curated resources. Track them in ⋯ More.</span>
</div>
""".strip(),
                unsafe_allow_html=True,
            )
            st.markdown(f"[Open the official page]({nxt.url})")
        else:
            st.success("Official resource track complete.")
