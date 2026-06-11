"""Learning Path tab — milestones, graduation checklist, proof downloads.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from curriculum import LESSONS
from experience import percent_label
from learning_path import (
    GRADUATION_PROMISE,
    completed_milestones_count,
    current_milestone_status,
    graduation_readiness,
    learning_outcomes,
    milestone_statuses,
    overall_learning_percent,
    skill_statuses,
)
from product_export import backup_zip_bytes, certificate_markdown, learning_transcript_markdown
from progress import profile_slug
from study_plan import DAILY_PLAN
from ui_components import (
    render_coach_summary,
    render_graduation_requirement,
    render_milestone_status,
    render_skill_status,
)


def render_path_tab(progress_data: dict, profile_name: str) -> None:
    st.header("📈 Learning Path: Python basics to capstone")
    st.caption("This is the finish line: milestones, proof, and graduation requirements for learning Python and general coding basics.")

    path_metrics = st.columns(4)
    ready = graduation_readiness(progress_data, total_lessons=len(LESSONS))
    current_status = current_milestone_status(progress_data)
    path_metrics[0].metric("Learning progress", percent_label(overall_learning_percent(progress_data)))
    path_metrics[1].metric("Milestones", f"{completed_milestones_count(progress_data)}/{len(milestone_statuses(progress_data))}")
    path_metrics[2].metric("Graduation", ready.status, percent_label(ready.percent))
    path_metrics[3].metric("Current milestone", current_status.milestone.title.split(" - ")[-1])

    render_coach_summary(
        "Goal: learn the Python basics by building proof",
        "A lesson only counts when you can explain it, practice it, and save evidence.",
        GRADUATION_PROMISE,
    )
    st.progress(ready.percent)
    st.caption(ready.summary)

    left_path, right_path = st.columns([1.25, 1])
    with left_path:
        st.subheader("Milestone map")
        statuses = milestone_statuses(progress_data)
        for status in statuses:
            render_milestone_status(status, is_current=status.milestone.id == current_status.milestone.id)

    with right_path:
        st.subheader("Graduation checklist")
        st.caption("These requirements make the app feel like a complete course instead of random practice.")
        for req in ready.requirements:
            render_graduation_requirement(req)
        st.info(f"Next graduation action: {ready.next_action}")

        if st.toggle("What you should know by the end", value=True):
            for outcome in learning_outcomes():
                st.write(f"- {outcome}")

        if st.toggle("Skill map", value=True):
            st.caption("Each skill unlocks when the related lesson is complete. Use this when you want to see what the daily gym is actually teaching.")
            for skill_status in skill_statuses(progress_data):
                render_skill_status(skill_status)

        if st.toggle("Graduation proof downloads", value=True):
            st.caption("These exports make the app feel complete: a private transcript, certificate preview, and backup pack you can keep outside the app.")
            st.download_button(
                "Download certificate preview",
                data=certificate_markdown(profile_name, progress_data, LESSONS),
                file_name=f"ai_code_tutor_certificate_{profile_slug(profile_name)}.md",
                mime="text/markdown",
                key="download_certificate_path",
            )
            st.download_button(
                "Download full transcript",
                data=learning_transcript_markdown(profile_name, progress_data, LESSONS, DAILY_PLAN),
                file_name=f"ai_code_tutor_transcript_{profile_slug(profile_name)}.md",
                mime="text/markdown",
                key="download_transcript_path",
            )
            st.download_button(
                "Download backup pack",
                data=backup_zip_bytes(profile_name, profile_slug(profile_name), progress_data, LESSONS, DAILY_PLAN),
                file_name=f"ai_code_tutor_backup_{profile_slug(profile_name)}.zip",
                mime="application/zip",
                key="download_backup_path",
            )

        if st.toggle("Capstone proof idea", value=False):
            st.write(
                "A good final proof is a tiny app or script you can explain in 60 seconds: what problem it solves, "
                "what inputs it uses, what output it gives, one bug you fixed, and one test or checklist that proves it works."
            )
            st.code(
                """Capstone demo script
1. This app/script helps with: ______
2. User input: ______
3. Python concepts used: variables, functions, conditionals, lists/dicts, tests
4. Bug I fixed: ______
5. Next improvement: ______""",
                language="text",
            )
