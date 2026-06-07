"""Official AI tab — curated provider resources, filters, and tracking.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from official_ai_resources import (
    OFFICIAL_AI_MILESTONES,
    OFFICIAL_AI_RESOURCES,
    OFFICIAL_AI_STARTER_PATH,
    PROVIDER_ORDER,
    RESOURCE_TYPES,
    STATUS_OPTIONS,
    next_recommended_resource,
    official_resource_stats,
    provider_counts,
    resource_has_certificate,
    resources_for_ids,
)
from progress import record_official_ai_resource, save_progress
from ui_components import render_card, render_official_resource_summary


def official_resource_status(progress_data: dict, resource_id: str) -> str:
    saved = progress_data.get("official_ai_status", {}).get(resource_id, "Not started")
    return saved if saved in STATUS_OPTIONS else "Not started"


def official_resource_note(progress_data: dict, resource_id: str) -> str:
    return progress_data.get("official_ai_notes", {}).get(resource_id, "")


def render_official_ai_tab(progress_data: dict, progress_path) -> None:
    st.header("Official AI Learning & Certifications")
    st.write(
        "Use this hub to track official provider lessons, docs, cohorts, and certifications while you learn Python. "
        "The app links out to official pages and saves your status here; it does not copy or republish their course content."
    )
    st.caption(
        "Verify prices, exam requirements, dates, and availability on the official provider page before enrolling or paying."
    )

    stats = official_resource_stats(progress_data)
    counts = provider_counts()
    stat_cols = st.columns(4)
    stat_cols[0].metric("Official resources", stats["total"])
    stat_cols[1].metric("Started", stats["started"])
    stat_cols[2].metric("Completed", stats["completed"])
    stat_cols[3].metric("Cert/certificate options", stats["certificate_options"])

    next_resource = next_recommended_resource(progress_data)
    if next_resource:
        render_card(
            "Recommended next AI step",
            f"{next_resource.provider}: {next_resource.title}. {next_resource.recommended_when}",
        )
        st.markdown(f"[Open recommended official page]({next_resource.url})")
    else:
        render_card(
            "Official AI track complete",
            "All curated official AI resources are marked Completed or Skipped. Add a new target or revisit your notes.",
            "success-soft",
        )

    st.subheader("Best starter path")
    starter_ids = OFFICIAL_AI_STARTER_PATH
    starter_cols = st.columns(3)
    for col, resource in zip(starter_cols, resources_for_ids(starter_ids)):
        with col:
            render_official_resource_summary(resource)
            st.markdown(f"[Open official page]({resource.url})")

    with st.expander("Suggested milestone tracks", expanded=True):
        for milestone in OFFICIAL_AI_MILESTONES:
            st.markdown(
                f"""
<div class="track-card">
    <strong>{milestone['title']}</strong><br>
    <span class="small-muted">{milestone['goal']}</span>
</div>
""".strip(),
                unsafe_allow_html=True,
            )
            for resource in resources_for_ids(milestone["resource_ids"]):
                status = official_resource_status(progress_data, resource.id)
                st.write(f"- **{resource.provider}: {resource.title}** - {status}")

    st.subheader("Browse and track official resources")
    filter_cols = st.columns([1, 1, 1])
    with filter_cols[0]:
        provider_filter = st.selectbox("Provider", ["All"] + list(PROVIDER_ORDER))
    with filter_cols[1]:
        type_filter = st.selectbox("Resource type", ["All"] + list(RESOURCE_TYPES))
    with filter_cols[2]:
        credential_only = st.checkbox("Show cert/certificate options only")

    filtered_resources = []
    for resource in OFFICIAL_AI_RESOURCES:
        if provider_filter != "All" and resource.provider != provider_filter:
            continue
        if type_filter != "All" and resource.resource_type != type_filter:
            continue
        if credential_only and not resource_has_certificate(resource):
            continue
        filtered_resources.append(resource)

    st.caption(f"Showing {len(filtered_resources)} resources. Provider counts: " + ", ".join(
        f"{provider}: {count}" for provider, count in counts.items()
    ))

    for resource in filtered_resources:
        status = official_resource_status(progress_data, resource.id)
        note = official_resource_note(progress_data, resource.id)
        expanded = resource.provider == "Gumloop" or status in {"Queued", "In progress"}
        with st.expander(f"{resource.provider}: {resource.title} ({status})", expanded=expanded):
            render_official_resource_summary(resource)
            st.markdown("**Skills:** " + ", ".join(f"`{tag}`" for tag in resource.tags))
            st.markdown(f"**Why it matters:** {resource.why_it_matters}")
            st.markdown(f"[Open official page]({resource.url})")

            status_index = STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0
            new_status = st.selectbox(
                "Status",
                STATUS_OPTIONS,
                index=status_index,
                key=f"official_status_{resource.id}",
            )
            new_note = st.text_area(
                "Private note for this resource",
                value=note,
                height=90,
                key=f"official_note_{resource.id}",
                placeholder="Example: Finish lessons 1-2 this week, then build one Gumloop workflow.",
            )
            if st.button("Save resource progress", key=f"save_official_{resource.id}"):
                record_official_ai_resource(progress_data, resource.id, new_status, new_note)
                save_progress(progress_data, progress_path)
                st.success("Official AI resource progress saved.")

    with st.expander("Prompt template for course or certificate prep"):
        st.code(
            """Role: You are my AI certification study coach.
Goal: Help me prepare for [provider/resource] while I learn Python.
Context: I am a beginner. I have completed lesson [number] in my Python app.
Official resource: [paste the official lesson/certification link]
Task: Create a 7-day study plan with daily tasks, practice questions, and one mini-project.
Constraints: Do not invent exam rules. Tell me what I must verify on the official page.
Output format: table with Day, Focus, Practice, Proof of Understanding.""",
            language="text",
        )
