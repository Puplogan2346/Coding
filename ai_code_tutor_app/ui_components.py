"""Reusable leaf-level UI render helpers.

This module exists so the 2,600-line ``app.py`` can shrink over time. The
helpers here are *presentation* renderers — visual building blocks (cards,
pills, step rows, timelines, callouts) used across many tabs. They take plain
primitives or small dataclasses and render them with Streamlit.

Dependency rule: renderers may depend on Streamlit, the escape helpers in
``ui_safety``, and the pure *leaf domain* modules (``experience`` formatting,
``curriculum`` lookups, ``gamification`` math). They must **not** touch state,
read or mutate ``progress_data`` for business logic, or call ``save_progress``.
Renderers that need those (e.g. ``render_project_summary``,
``render_official_resource``) stay in ``app.py`` / per-tab modules.

Future per-tab module splits (``today_tab.py``, ``learn_tab.py``, …) can
import from here freely.
"""
from __future__ import annotations

import streamlit as st

from curriculum import LESSONS, get_lesson_by_id
from experience import percent_label, timeline_legend_counts
from gamification import earned_badges, level_progress_percent, xp_to_next_level
from ui_safety import h, safe_html_text


def render_card(title: str, body: str, tone: str = "") -> None:
    tone_class = f" {tone}" if tone else ""
    safe_title = safe_html_text(title)
    safe_body = safe_html_text(body)
    st.markdown(
        f"""
<div class="card{tone_class}">
    <h3>{safe_title}</h3>
    <p>{safe_body}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_status_pills(lesson_level: str, minutes: int, is_complete: bool) -> None:
    status = "Complete" if is_complete else "In progress"
    st.markdown(
        f"""
<span class="pill">{h(lesson_level)}</span>
<span class="pill">{h(minutes)} min</span>
<span class="pill">{h(status)}</span>
""".strip(),
        unsafe_allow_html=True,
    )


def render_step(number: int, title: str, body: str) -> None:
    safe_title = safe_html_text(title)
    safe_body = safe_html_text(body)
    st.markdown(
        f"""
<div class="step-card">
    <strong>{number}. {safe_title}</strong>
    <span>{safe_body}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_score_badge(score: int, total: int) -> None:
    percent = round((score / total) * 100) if total else 0
    if percent >= 80:
        st.success(f"Score: {score}/{total} ({percent}%). Strong work.")
    elif percent >= 60:
        st.warning(f"Score: {score}/{total} ({percent}%). Review the misses and try again.")
    else:
        st.error(f"Score: {score}/{total} ({percent}%). Revisit the lesson, then retake it.")


def render_daily_timeline(days) -> None:
    dots = []
    for day in days:
        dots.append(
            f'<span class="day-dot {h(day.status)}" title="{h(day.label)}" aria-label="{h(day.label)}">{h(day.day)}</span>'
        )
    st.markdown(f"<div class='timeline-wrap'>{''.join(dots)}</div>", unsafe_allow_html=True)


def render_level_progress(xp: int) -> None:
    st.progress(level_progress_percent(xp))
    remaining = xp_to_next_level(xp)
    if remaining:
        st.caption(f"{remaining} XP to the next level.")
    else:
        st.caption("Top starter level reached. Keep building projects and proof notes.")


def render_coach_summary(headline: str, subline: str, support: str) -> None:
    st.markdown(
        f"""
<div class="coach-summary">
    <h2>{h(headline)}</h2>
    <p><strong>{h(subline)}</strong></p>
    <p>{h(support)}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_timeline_legend(days) -> None:
    counts = timeline_legend_counts(days)
    labels = (
        ("complete", "Done"),
        ("current", "Today"),
        ("upcoming", "Later"),
        ("skipped", "Skipped"),
        ("missed", "Unfinished"),
    )
    rendered = []
    for status, label in labels:
        if counts.get(status, 0) or status in {"complete", "current", "upcoming"}:
            rendered.append(
                f"<span class='legend-pill'><span class='legend-swatch {h(status)}'></span>{h(label)}: {h(counts.get(status, 0))}</span>"
            )
    st.markdown(f"<div class='timeline-legend'>{''.join(rendered)}</div>", unsafe_allow_html=True)


def render_done_zone(checklist_completion: float, mission_complete_now: bool) -> None:
    if mission_complete_now:
        title = "Done zone: saved"
        body = "Today is already logged. A tiny review is optional; stopping is allowed."
    elif checklist_completion >= 1:
        title = "Done zone: lock it in"
        body = "Your checklist is complete. Save the mission reflection so the streak, XP, and proof note all update."
    else:
        title = "Done zone: not yet"
        body = "Only save the mission after you have one proof note. The checklist can be tiny on rescue days."
    st.markdown(
        f"""
<div class="done-zone">
    <strong>{h(title)}</strong>
    <span>{h(body)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_resume_banner(summary, lesson_title: str) -> None:
    st.markdown(
        f"""
<div class="resume-box">
    <strong>{h(summary.headline)}</strong>
    <span>{h(summary.body)}</span>
    <div class="hero-meta">
        <span class="hero-stat">Saved pace: {h(summary.pace)}</span>
        <span class="hero-stat">Lesson: {h(lesson_title)}</span>
        <span class="hero-stat">Saved progress: {h(summary.checked_blocks)}/{h(summary.total_blocks)} blocks</span>
        <span class="hero-stat">Status: {h(summary.status)}</span>
    </div>
    <span><b>Proof draft:</b> {h(summary.proof_preview)}<br><b>Next review:</b> {h(summary.next_review)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_gym_block(block, done: bool) -> None:
    status = "Done" if done else "Open"
    st.markdown(
        f"""
<div class="gym-block">
    <strong>{h(status)} · {h(block.label)} · {h(block.minutes)} min</strong>
    <span>{h(block.action)}<br><b>Proof:</b> {h(block.proof)}</span>
    <em>{h(block.why)}</em>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_focus_workout_card(card) -> None:
    st.markdown(
        f"""
<div class="focus-workout-card">
    <h3>{h(card.headline)}</h3>
    <p><strong>{h(card.nudge)}</strong></p>
    <div class="hero-meta">
        <span class="hero-stat">Step: {h(card.step_number)}/{h(card.total_steps)}</span>
        <span class="hero-stat">Time box: {h(card.minutes)} min</span>
        <span class="hero-stat">Workout: {h(percent_label(card.completion))}</span>
    </div>
    <div class="next-rep">
        <strong>Do this now:</strong> {h(card.action)}<br>
        <strong>Proof to save:</strong> {h(card.proof)}
    </div>
    <p>{h(card.why)}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_smoothness_check(check) -> None:
    status_class = "success-soft" if check.status == "Pass" else "warning-soft"
    st.markdown(
        f"""
<div class="smooth-check {h(status_class)}">
    <strong>{h(check.status)} · {h(check.name)}</strong>
    <span>{h(check.detail)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_review_item(item) -> None:
    try:
        lesson_title = get_lesson_by_id(item.lesson_id).title
    except Exception:
        lesson_title = item.lesson_id
    st.markdown(
        f"""
<div class="review-chip">
    <strong>{h(lesson_title)} · {h(item.intensity)}</strong>
    <span>{h(item.reason)} — {h(item.action)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_gym_history_item(item) -> None:
    st.markdown(
        f"""
<div class="review-chip">
    <strong>Day {h(item.day)} · {h(item.status)} · {h(item.pace)}</strong>
    <span>{h(item.minutes)} minutes · {h(item.proof_preview)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_milestone_status(status, is_current: bool = False) -> None:
    tone = "complete" if status.status == "Complete" else "current" if is_current else ""
    evidence = " · ".join(status.evidence)
    st.markdown(
        f"""
<div class="milestone-card {h(tone)}">
    <h3>{h(status.milestone.title)} · {h(percent_label(status.percent))}</h3>
    <p><strong>{h(status.status)}</strong> — {h(status.milestone.goal)}</p>
    <p><b>Proof goal:</b> {h(status.milestone.proof)}</p>
    <p><b>Evidence:</b> {h(evidence)}</p>
    <p><b>Next action:</b> {h(status.next_action)}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_graduation_requirement(req) -> None:
    label = "Done" if req.complete else "Open"
    st.markdown(
        f"""
<div class="requirement-row">
    <div><strong>{h(label)} · {h(req.title)}</strong><br><span>{h(req.proof)}</span></div>
    <div><strong>{h(req.current)}/{h(req.target)}</strong></div>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_skill_status(status) -> None:
    next_piece = "Complete" if status.next_lesson_id is None else f"Next lesson: {status.next_lesson_id}"
    st.markdown(
        f"""
<div class="review-chip">
    <strong>{h(status.skill.title)} · {h(percent_label(status.percent))}</strong>
    <span>{h(status.skill.description)}<br><b>Practice:</b> {h(status.skill.practice_goal)}<br><b>{h(next_piece)}</b></span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_standalone_check(check) -> None:
    tone = "success-soft" if check.status == "Pass" else "warning-soft" if check.status in {"Warning", "Optional"} else "danger-soft"
    st.markdown(
        f"""
<div class="check-row {h(tone)}">
    <strong>{h(check.status)} · {h(check.title)}</strong>
    <span>{h(check.detail)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_proof_preview(card) -> None:
    st.markdown(
        f"""
<div class="proof-card">
    <strong>{h(card.title)}</strong>
    <span>{h(card.summary)}<br><b>Next review:</b> {h(card.next_review)}</span>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_time_blocks(blocks) -> None:
    for block in blocks:
        st.markdown(
            f"""
<div class="block-list">
    <strong>{h(block.label)} - {h(block.minutes)} min</strong><br>
    <span class="small-muted">{h(block.instruction)}</span>
</div>
""".strip(),
            unsafe_allow_html=True,
        )


def render_focus_blocks(blocks) -> None:
    for block in blocks:
        st.markdown(
            f"""
<div class="focus-card">
    <strong>{h(block.label)} - {h(block.minutes)} min</strong>
    <span>{h(block.instruction)}<br><em>{h(block.why_it_helps)}</em></span>
</div>
""".strip(),
            unsafe_allow_html=True,
        )


def render_badge_shelf(progress_data: dict) -> None:
    badges = earned_badges(progress_data, len(LESSONS))
    if not badges:
        st.info("No badges yet. Complete your first mission or lesson to unlock one.")
        return
    for badge in badges:
        st.markdown(
            f"""
<div class="badge-card">
    <strong>{h(badge.title)}</strong>
    <span>{h(badge.description)}</span>
</div>
""".strip(),
            unsafe_allow_html=True,
        )


def render_daily_mission_card(mission) -> None:
    lesson_text = "Open practice" if mission.lesson_id is None else get_lesson_by_id(mission.lesson_id).title
    st.markdown(
        f"""
<div class="mission-card">
    <h2>Day {h(mission.day)}: {h(mission.title)}</h2>
    <p><strong>Focus:</strong> {h(mission.focus)} | <strong>Time:</strong> {h(mission.total_minutes)} minutes | <strong>Lesson:</strong> {h(lesson_text)}</p>
    <p><strong>Fun challenge:</strong> {h(mission.fun_challenge)}</p>
    <p><strong>Proof of understanding:</strong> {h(mission.proof)}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def render_official_resource_summary(resource) -> None:
    st.markdown(
        f"""
<div class="resource-card">
    <h3>{h(resource.provider)}: {h(resource.title)}</h3>
    <div class="resource-meta">{h(resource.resource_type)} | {h(resource.level)} | {h(resource.time_commitment)}</div>
    <p>{h(resource.summary)}</p>
    <p><strong>Credential:</strong> {h(resource.certificate)}</p>
    <p><strong>Use it when:</strong> {h(resource.recommended_when)}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def select_pace_control(label: str, options, index: int, key: str, help_text: str, disabled: bool = False):
    """iOS-style tile picker: Streamlit pills when available, radio fallback.

    Single-select pills can be tapped off (returning None), so callers should
    guard with ``or default``.
    """
    if hasattr(st, "pills"):
        return st.pills(
            label,
            options,
            default=options[index],
            key=key,
            help=help_text,
            selection_mode="single",
            width="stretch",
            disabled=disabled,
        )
    return st.radio(label, options, index=index, horizontal=True, key=key, help=help_text, disabled=disabled)
