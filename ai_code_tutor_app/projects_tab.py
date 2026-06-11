"""Projects tab — project tracks, milestones, and capstone checkpoints.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from progress import record_project_milestone, save_progress
from projects import (
    PROJECTS,
    completed_project_milestones_count,
    next_project_milestone,
    project_completion_percent,
    project_progress,
    recommended_project_id,
)
from ui_components import render_card
from ui_safety import h


def render_project_summary(project, progress_data: dict) -> None:
    completion = int(project_completion_percent(progress_data, project.id) * 100)
    milestone = next_project_milestone(progress_data, project.id)
    st.markdown(
        f"""
<div class="project-card">
    <h3>{h(project.title)}</h3>
    <p><strong>{h(project.level)}</strong> · about {h(project.minutes)} min total · {h(completion)}% complete</p>
    <p>{h(project.description)}</p>
    <p><strong>Next milestone:</strong> {h(milestone.title)}</p>
    <p><strong>Skills:</strong> {h(', '.join(project.skills))}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_projects_tab(progress_data: dict, progress_path) -> None:
    st.header("🛠️ Projects & capstone checkpoints")
    st.write(
        "Projects make the lessons feel real. Each track is broken into tiny checkpoints so you can build without getting overwhelmed."
    )

    project_metric_cols = st.columns(4)
    project_metric_cols[0].metric("Project tracks", len(PROJECTS))
    project_metric_cols[1].metric("Milestones done", completed_project_milestones_count(progress_data))
    project_metric_cols[2].metric("Recommended", next(project.title for project in PROJECTS if project.id == recommended_project_id(progress_data)))
    project_metric_cols[3].metric("Capstone", f"{int(project_completion_percent(progress_data, 'personal_ai_code_tutor') * 100)}%")

    recommended = next(project for project in PROJECTS if project.id == recommended_project_id(progress_data))
    render_card(
        "Recommended project",
        f"{recommended.title}: {recommended.description} Next checkpoint: {next_project_milestone(progress_data, recommended.id).title}.",
        "success-soft",
    )

    project_labels = [f"{project.title} ({project.level})" for project in PROJECTS]
    selected_project_label = st.radio("Choose a project track", project_labels, key="project_track_choice")
    selected_project = PROJECTS[project_labels.index(selected_project_label)]
    render_project_summary(selected_project, progress_data)
    st.progress(project_completion_percent(progress_data, selected_project.id))

    st.subheader("Milestones")
    saved_milestones = project_progress(progress_data, selected_project.id)
    for milestone in selected_project.milestones:
        if st.toggle(f"{milestone.title} - {saved_milestones.get(milestone.id, {}).get('status', 'Not started')}", value=saved_milestones.get(milestone.id, {}).get("status") in {None, "Not started", "In progress"}):
            st.write(milestone.proof)
            current = saved_milestones.get(milestone.id, {})
            status_options = ["Not started", "In progress", "Completed", "Skipped"]
            current_status = current.get("status", "Not started") if current.get("status", "Not started") in status_options else "Not started"
            new_status = st.radio(
                "Status",
                status_options,
                index=status_options.index(current_status),
                horizontal=True,
                key=f"project_status_{selected_project.id}_{milestone.id}",
            )
            new_note = st.text_area(
                "Proof note",
                value=current.get("note", ""),
                key=f"project_note_{selected_project.id}_{milestone.id}",
                height=80,
                placeholder="Example: I wrote the score function and tested 3/3 answers.",
            )
            if st.button("Save milestone", key=f"save_project_{selected_project.id}_{milestone.id}"):
                record_project_milestone(progress_data, selected_project.id, milestone.id, new_status, new_note)
                save_progress(progress_data, progress_path)
                st.success("Project milestone saved.")
                st.rerun()

    st.subheader("All project tracks")
    for project in PROJECTS:
        render_project_summary(project, progress_data)
