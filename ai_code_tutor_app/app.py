from __future__ import annotations

import json
import os

import streamlit as st

from ai_tutor import (
    ai_is_configured,
    configured_model,
)
from code_runner import code_runner_enabled
from curriculum import LESSONS, get_lesson_by_id
from gamification import calculate_xp
from learning_path import first_incomplete_lesson_id
from private_access import configured_passcode, private_access_status, private_badge_text, verify_passcode
from product_export import (
    backup_zip_bytes,
    learning_transcript_markdown,
    unwrap_progress_import,
)
from progress import (
    completed_daily_missions_count,
    completion_percent,
    load_progress,
    normalize_progress_data,
    profile_slug,
    progress_path_for_profile,
    save_progress,
)
from study_plan import (
    DAILY_PLAN,
    next_mission,
    plan_completion_percent,
)
from ui_safety import h
from today_tab import render_today_tab
from focus_tab import render_focus_tab
from dashboard_tab import render_dashboard_tab
from path_tab import render_path_tab
from lesson_tab import render_lesson_tab
from quiz_tab import render_quiz_tab
from code_tab import render_code_tab
from projects_tab import render_projects_tab
from prompt_tab import render_prompt_tab
from official_ai_tab import render_official_ai_tab
from ai_tab import render_ai_tab
from notes_tab import render_notes_tab
from deploy_tab import render_deploy_tab
from glossary_tab import render_glossary_tab
from review_tab import render_review_tab


st.set_page_config(
    page_title="AI Code Tutor",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LESSON_IDS = [lesson.id for lesson in LESSONS]


def apply_theme(low_stimulation: bool = False) -> None:
    st.markdown(
        """
<style>
    .block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px;}
    [data-testid="stSidebar"] {border-right: 1px solid rgba(120, 120, 120, .16);}
    h1, h2, h3 {letter-spacing: -0.025em;}
    .hero {
        padding: 2.1rem 2.2rem;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(53, 111, 255, .18), rgba(106, 214, 185, .16));
        border: 1px solid rgba(120, 120, 120, .18);
        margin-bottom: 1.25rem;
    }
    .hero h1 {font-size: 3rem; margin: 0 0 .3rem 0;}
    .hero p {font-size: 1.08rem; margin: .2rem 0 0 0; color: rgba(49, 51, 63, .78); max-width: 760px;}
    .card {
        border: 1px solid rgba(120, 120, 120, .18);
        border-radius: 22px;
        padding: 1.05rem 1.15rem;
        background: rgba(255, 255, 255, .72);
        box-shadow: 0 14px 36px rgba(0, 0, 0, .045);
        min-height: 118px;
        margin-bottom: .75rem;
    }
    .card h3 {font-size: 1.05rem; margin: 0 0 .3rem 0;}
    .card p {margin: 0; color: rgba(49, 51, 63, .74);}
    .pill {
        display: inline-block;
        padding: .22rem .58rem;
        border-radius: 999px;
        background: rgba(53, 111, 255, .12);
        border: 1px solid rgba(53, 111, 255, .18);
        font-size: .8rem;
        margin-right: .35rem;
        margin-bottom: .35rem;
    }
    .lesson-row {
        padding: .75rem .85rem;
        border: 1px solid rgba(120, 120, 120, .15);
        border-radius: 16px;
        margin-bottom: .55rem;
        background: rgba(255, 255, 255, .58);
    }
    .small-muted {font-size: .88rem; color: rgba(49, 51, 63, .66);}
    .success-soft {background: rgba(52, 168, 83, .12); border-color: rgba(52, 168, 83, .25);}
    .warning-soft {background: rgba(251, 188, 5, .13); border-color: rgba(251, 188, 5, .28);}
    .danger-soft {background: rgba(234, 67, 53, .10); border-color: rgba(234, 67, 53, .22);}
    .step-card {
        padding: .95rem 1.05rem;
        border-radius: 18px;
        border: 1px solid rgba(120, 120, 120, .15);
        background: rgba(255, 255, 255, .68);
        margin-bottom: .7rem;
    }
    .step-card strong {font-size: 1rem;}
    .step-card span {display: block; color: rgba(49, 51, 63, .70); margin-top: .2rem;}

    .daily-action-card {
        position: sticky;
        top: .5rem;
        z-index: 6;
        border: 1px solid rgba(53, 111, 255, .22);
        border-radius: 24px;
        padding: 1rem 1.1rem;
        background: rgba(255, 255, 255, .96);
        box-shadow: 0 14px 36px rgba(0, 0, 0, .075);
        margin-bottom: .85rem;
    }
    .daily-action-card h2 {margin: 0 0 .25rem 0; font-size: 1.45rem;}
    .daily-action-card p {margin: .15rem 0; color: rgba(49, 51, 63, .72);}
    .compact-hero {
        padding: 1.15rem 1.35rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(53, 111, 255, .16), rgba(106, 214, 185, .14));
        border: 1px solid rgba(120, 120, 120, .16);
        margin-bottom: .65rem;
    }
    .compact-hero h1 {font-size: 2.15rem; margin: 0 0 .15rem 0;}
    .compact-hero p {margin: 0; color: rgba(49, 51, 63, .72);}
    .resource-card {
        border: 1px solid rgba(120, 120, 120, .16);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        background: rgba(255, 255, 255, .66);
        margin-bottom: .8rem;
    }
    .resource-card h3 {margin: 0 0 .25rem 0; font-size: 1.06rem;}
    .resource-card p {margin: .25rem 0; color: rgba(49, 51, 63, .74);}
    .resource-meta {font-size: .86rem; color: rgba(49, 51, 63, .68); margin-bottom: .45rem;}
    .track-card {
        padding: .85rem 1rem;
        border: 1px solid rgba(120, 120, 120, .15);
        border-radius: 16px;
        margin-bottom: .55rem;
        background: rgba(255, 255, 255, .54);
    }
    .mission-card {
        border: 1px solid rgba(53, 111, 255, .20);
        border-radius: 26px;
        padding: 1.2rem 1.25rem;
        background: linear-gradient(135deg, rgba(53, 111, 255, .11), rgba(106, 214, 185, .11));
        margin-bottom: 1rem;
    }
    .mission-card h2 {margin-top: 0;}
    .block-list {
        border-left: 3px solid rgba(53, 111, 255, .35);
        padding-left: .8rem;
        margin-bottom: .65rem;
    }
    .badge-card {
        border: 1px solid rgba(120, 120, 120, .16);
        border-radius: 16px;
        padding: .7rem .8rem;
        margin-bottom: .5rem;
        background: rgba(255, 255, 255, .64);
    }
    .badge-card strong {display: block; margin-bottom: .15rem;}
    .badge-card span {color: rgba(49, 51, 63, .70); font-size: .88rem;}

    .focus-card {
        border: 1px solid rgba(53, 111, 255, .18);
        border-radius: 18px;
        padding: .85rem 1rem;
        background: rgba(53, 111, 255, .065);
        margin-bottom: .55rem;
    }
    .focus-card strong {display: block; margin-bottom: .15rem;}
    .focus-card span {color: rgba(49, 51, 63, .72); font-size: .9rem;}
    .project-card {
        border: 1px solid rgba(120, 120, 120, .16);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        background: rgba(255, 255, 255, .68);
        margin-bottom: .8rem;
    }
    .project-card h3 {margin: 0 0 .25rem 0; font-size: 1.08rem;}
    .project-card p {margin: .25rem 0; color: rgba(49, 51, 63, .74);}
    .parking-item {
        padding: .55rem .7rem;
        border-radius: 14px;
        border: 1px dashed rgba(120, 120, 120, .28);
        margin-bottom: .4rem;
        background: rgba(255,255,255,.52);
    }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(120, 120, 120, .15);
        border-radius: 18px;
        padding: .8rem .95rem;
        background: rgba(255, 255, 255, .66);
    }
    .skip-link {
        position: absolute;
        left: -999px;
        top: .5rem;
        z-index: 9999;
        padding: .55rem .85rem;
        border-radius: 999px;
        background: #ffffff;
        border: 2px solid rgba(53, 111, 255, .60);
    }
    .skip-link:focus {left: .75rem;}
    .hero-meta {margin-top: .8rem; display: flex; gap: .5rem; flex-wrap: wrap;}
    .hero-stat {
        display: inline-flex;
        align-items: center;
        gap: .3rem;
        padding: .32rem .68rem;
        border-radius: 999px;
        border: 1px solid rgba(53, 111, 255, .16);
        background: rgba(255, 255, 255, .58);
        font-size: .86rem;
    }
    .action-callout {
        padding: 1.05rem 1.15rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(53, 111, 255, .13), rgba(106, 214, 185, .11));
        border: 1px solid rgba(53, 111, 255, .22);
        margin: .85rem 0 1rem 0;
    }
    .action-callout h3 {margin: 0 0 .25rem 0; font-size: 1.25rem;}
    .action-callout p {margin: .25rem 0; color: rgba(49, 51, 63, .74);}
    .mini-card {
        border: 1px solid rgba(120, 120, 120, .14);
        border-radius: 18px;
        padding: .85rem .95rem;
        background: rgba(255, 255, 255, .62);
        min-height: 106px;
        margin-bottom: .75rem;
    }
    .mini-card strong {display: block; margin-bottom: .2rem;}
    .mini-card span {color: rgba(49, 51, 63, .72); font-size: .92rem;}
    .timeline-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: .32rem;
        align-items: center;
        margin: .5rem 0 1rem 0;
    }
    .day-dot {
        width: 1.75rem;
        height: 1.75rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: .74rem;
        border: 1px solid rgba(120, 120, 120, .24);
        background: rgba(255,255,255,.64);
        color: rgba(49, 51, 63, .76);
    }
    .day-dot.complete {background: rgba(52, 168, 83, .16); border-color: rgba(52, 168, 83, .30);}
    .day-dot.current {background: rgba(53, 111, 255, .18); border-color: rgba(53, 111, 255, .42); font-weight: 700;}
    .day-dot.skipped, .day-dot.missed {background: rgba(251, 188, 5, .13); border-color: rgba(251, 188, 5, .32);}
    .coach-toolbar {
        border: 1px solid rgba(120, 120, 120, .15);
        border-radius: 22px;
        padding: .9rem 1rem;
        background: rgba(255, 255, 255, .60);
        margin-bottom: .85rem;
    }
    .progress-caption {font-size: .9rem; color: rgba(49, 51, 63, .70); margin-top: .15rem;}
    .coach-summary {
        border: 1px solid rgba(53, 111, 255, .22);
        border-radius: 28px;
        padding: 1.15rem 1.25rem;
        background: linear-gradient(135deg, rgba(53, 111, 255, .12), rgba(255, 255, 255, .70));
        margin: .85rem 0 1rem 0;
    }
    .coach-summary h2 {margin: 0 0 .35rem 0; font-size: 1.55rem;}
    .coach-summary p {margin: .25rem 0; color: rgba(49, 51, 63, .76);}
    .coach-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: .55rem;
        margin: .75rem 0 1rem 0;
    }
    .coach-strip-item {
        border: 1px solid rgba(120, 120, 120, .14);
        border-radius: 18px;
        padding: .75rem .8rem;
        background: rgba(255,255,255,.64);
    }
    .coach-strip-item strong {display: block; font-size: .92rem; margin-bottom: .16rem;}
    .coach-strip-item span {font-size: .88rem; color: rgba(49, 51, 63, .70);}
    .timeline-legend {display:flex; flex-wrap:wrap; gap:.4rem; margin: -.35rem 0 .85rem 0;}
    .legend-pill {
        display:inline-flex; align-items:center; gap:.32rem;
        padding:.22rem .52rem; border-radius:999px;
        border:1px solid rgba(120,120,120,.16); background:rgba(255,255,255,.58);
        font-size:.8rem; color:rgba(49,51,63,.72);
    }
    .legend-swatch {width:.68rem; height:.68rem; border-radius:999px; border:1px solid rgba(120,120,120,.24);}
    .legend-swatch.complete {background: rgba(52, 168, 83, .22);}
    .legend-swatch.current {background: rgba(53, 111, 255, .25);}
    .legend-swatch.upcoming {background: rgba(255,255,255,.75);}
    .legend-swatch.skipped, .legend-swatch.missed {background: rgba(251, 188, 5, .18);}
    .done-zone {
        border: 1px solid rgba(52, 168, 83, .24);
        border-radius: 20px;
        padding: .9rem 1rem;
        background: rgba(52, 168, 83, .09);
        margin: .8rem 0;
    }
    .done-zone strong {display:block; margin-bottom:.15rem;}
    .done-zone span {color: rgba(49,51,63,.72);}
    .gym-shell {
        border: 1px solid rgba(53, 111, 255, .22);
        border-radius: 30px;
        padding: 1.15rem 1.25rem;
        background: linear-gradient(135deg, rgba(53, 111, 255, .12), rgba(106, 214, 185, .10));
        margin: .85rem 0 1rem 0;
    }
    .gym-shell h2 {margin: 0 0 .3rem 0; font-size: 1.75rem;}
    .gym-shell p {margin: .22rem 0; color: rgba(49,51,63,.76);}
    .gym-start {
        border: 1px solid rgba(53, 111, 255, .20);
        border-radius: 24px;
        padding: 1rem 1.1rem;
        background: rgba(255,255,255,.68);
        margin: .75rem 0;
    }
    .focus-workout-card {
        border: 2px solid rgba(53, 111, 255, .28);
        border-radius: 30px;
        padding: 1.15rem 1.25rem;
        background: linear-gradient(135deg, rgba(53, 111, 255, .14), rgba(255,255,255,.82));
        margin: .85rem 0 1rem 0;
        box-shadow: 0 18px 40px rgba(0,0,0,.045);
    }
    .focus-workout-card h3 {margin: 0 0 .35rem 0; font-size: 1.45rem;}
    .focus-workout-card p {margin: .28rem 0; color: rgba(49,51,63,.76);}
    .focus-workout-card .next-rep {
        border-left: 4px solid rgba(53,111,255,.42);
        padding: .55rem .75rem;
        background: rgba(255,255,255,.64);
        border-radius: 0 16px 16px 0;
        margin: .8rem 0;
    }
    .smooth-check {
        border: 1px solid rgba(120,120,120,.14);
        border-radius: 16px;
        padding: .65rem .75rem;
        background: rgba(255,255,255,.62);
        margin-bottom: .45rem;
    }
    .smooth-check strong {display:block; margin-bottom:.12rem;}
    .smooth-check span {font-size:.88rem; color:rgba(49,51,63,.70);}
    .resume-box {
        border: 1px solid rgba(251, 188, 5, .30);
        border-radius: 24px;
        padding: 1rem 1.1rem;
        background: rgba(251, 188, 5, .10);
        margin: .75rem 0 1rem 0;
    }
    .resume-box strong {display:block; margin-bottom:.22rem; font-size:1.02rem;}
    .resume-box span {display:block; color:rgba(49,51,63,.72); font-size:.92rem;}
    .gym-block {
        border: 1px solid rgba(120, 120, 120, .15);
        border-radius: 18px;
        padding: .8rem .9rem;
        background: rgba(255,255,255,.64);
        margin-bottom: .55rem;
    }
    .gym-block strong {display:block; margin-bottom:.15rem;}
    .gym-block span {font-size:.9rem; color:rgba(49,51,63,.72);}
    .gym-block em {display:block; margin-top:.25rem; font-size:.84rem; color:rgba(49,51,63,.62);}
    .proof-card {
        border: 1px solid rgba(52, 168, 83, .25);
        border-radius: 20px;
        padding: .9rem 1rem;
        background: rgba(52,168,83,.08);
        margin: .7rem 0;
    }
    .proof-card strong {display:block; margin-bottom:.2rem;}
    .proof-card span {color:rgba(49,51,63,.72);}
    .lesson-choice-card {
        border: 1px solid rgba(53, 111, 255, .20);
        border-radius: 20px;
        padding: .9rem 1rem;
        background: rgba(53,111,255,.075);
        margin: .7rem 0;
    }
    .lesson-choice-card strong {display:block; margin-bottom:.18rem;}
    .lesson-choice-card span {font-size:.9rem; color:rgba(49,51,63,.72);}
    .review-chip {
        border: 1px solid rgba(120,120,120,.16);
        border-radius: 16px;
        padding: .65rem .75rem;
        margin-bottom:.45rem;
        background:rgba(255,255,255,.60);
    }
    .review-chip strong {display:block; margin-bottom:.12rem;}
    .review-chip span {font-size:.88rem; color:rgba(49,51,63,.70);}

    .milestone-card {
        border: 1px solid rgba(53, 111, 255, .18);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        background: rgba(255, 255, 255, .68);
        margin-bottom: .8rem;
    }
    .milestone-card.complete {border-color: rgba(52, 168, 83, .30); background: rgba(52, 168, 83, .08);}
    .milestone-card.current {border-color: rgba(53, 111, 255, .34); background: rgba(53, 111, 255, .08);}
    .milestone-card h3 {margin: 0 0 .25rem 0; font-size: 1.08rem;}
    .milestone-card p {margin: .25rem 0; color: rgba(49, 51, 63, .74);}
    .requirement-row {
        display: flex;
        justify-content: space-between;
        gap: .75rem;
        align-items: flex-start;
        border-bottom: 1px solid rgba(120, 120, 120, .12);
        padding: .55rem 0;
    }
    .requirement-row:last-child {border-bottom: 0;}
    .requirement-row span {color: rgba(49, 51, 63, .70); font-size: .9rem;}
    .check-row {
        border: 1px solid rgba(120,120,120,.15);
        border-radius: 16px;
        padding: .7rem .8rem;
        margin-bottom: .5rem;
        background: rgba(255,255,255,.62);
    }
    .check-row strong {display:block; margin-bottom:.1rem;}
    .check-row span {font-size:.88rem; color:rgba(49,51,63,.70);}
    .ux-note {
        border-left: 4px solid rgba(53, 111, 255, .36);
        padding: .65rem .85rem;
        background: rgba(53, 111, 255, .06);
        border-radius: 0 14px 14px 0;
        margin: .7rem 0;
    }
    .ux-note p {margin:0; color:rgba(49,51,63,.75);}
    .stButton > button, button[kind="primary"] {
        border-radius: 999px !important;
        min-height: 44px;
        font-weight: 650;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] {
        border-radius: 14px;
    }
    *:focus-visible {
        outline: 3px solid rgba(53, 111, 255, .55) !important;
        outline-offset: 2px !important;
    }
    @media (max-width: 760px) {
        .block-container {padding-left: .9rem; padding-right: .9rem; padding-top: 1rem;}
        .hero {padding: 1.25rem 1.1rem; border-radius: 22px;}
        .hero h1 {font-size: 2.15rem;}
        .hero p {font-size: 1rem;}
        .card, .mini-card, .mission-card, .action-callout, .coach-summary {min-height: 0; border-radius: 18px;}
        .coach-strip {grid-template-columns: 1fr;}
        .day-dot {width: 1.55rem; height: 1.55rem; font-size: .68rem;}
    }
</style>
""".strip(),
        unsafe_allow_html=True,
    )
    if low_stimulation:
        st.markdown(
            """
<style>
    .hero, .mission-card, .action-callout, .coach-summary {background: rgba(255, 255, 255, .88) !important;}
    .card, .step-card, .resource-card, .project-card, .focus-card, .mini-card, div[data-testid="stMetric"] {
        box-shadow: none !important;
    }
    .pill, .hero-stat, .day-dot {background: rgba(120, 120, 120, .08) !important;}
    .day-dot.current {border-width: 2px !important;}
</style>
""".strip(),
            unsafe_allow_html=True,
        )


def safe_json(data: dict) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def streamlit_secrets_mapping() -> dict:
    try:
        return dict(st.secrets)
    except Exception:
        return {}


_private_status = private_access_status(os.environ, streamlit_secrets_mapping())
_private_passcode, _private_passcode_source = configured_passcode(os.environ, streamlit_secrets_mapping())
if _private_status.required:
    if not _private_status.configured:
        st.error("Private mode is enabled, but no private passcode is configured.")
        st.info("Set APP_PRIVATE_PASSCODE as an environment variable or Streamlit secret, then restart the app.")
        st.stop()
    if not st.session_state.get("private_access_ok", False):
        st.markdown("# AI Code Tutor")
        st.caption("Private daily coding gym. Enter your access code to continue.")
        entered_passcode = st.text_input("Private access code", type="password")
        if st.button("Unlock private app", type="primary"):
            if verify_passcode(entered_passcode, _private_passcode):
                st.session_state.private_access_ok = True
                st.success("Unlocked.")
                st.rerun()
            else:
                st.error("That access code did not match.")
        st.stop()


with st.sidebar:
    # ADHD-friendly sidebar: keep visible-by-default to the essentials
    # (header, streak, single progress bar). Everything else — profile,
    # lesson picker, study mode, AI/runner status, downloads — moves into
    # a single Settings expander so Day 1 isn't overwhelmed.
    profile_name = (st.session_state.get("profile_name") or "guest").strip() or "guest"

    if st.session_state.get("active_profile") != profile_name:
        st.session_state.active_profile = profile_name
        st.session_state.profile_name = profile_name
        st.session_state.ai_messages = []
        st.session_state.selected_lesson_id = ""

    progress_path = progress_path_for_profile(profile_name)
    progress_data = load_progress(LESSON_IDS, progress_path, profile_name=profile_name)
    apply_theme(low_stimulation=bool(progress_data.get("focus_preferences", {}).get("low_stimulation_mode", False)))

    if (
        not st.session_state.get("selected_lesson_id")
        or st.session_state.selected_lesson_id not in LESSON_IDS
    ):
        st.session_state.selected_lesson_id = first_incomplete_lesson_id(progress_data)

    completed_count = len(progress_data.get("completed_lessons", []))
    completion = completion_percent(progress_data, len(LESSONS))
    daily_completion = plan_completion_percent(progress_data)
    daily_done = completed_daily_missions_count(progress_data)
    sidebar_streak = int(progress_data.get("study_streak", 0) or 0)

    # Day 1 minimal view: one header + streak + one progress bar.
    st.header("Your learning space")
    if sidebar_streak > 0:
        st.markdown(f"**🔥 {sidebar_streak}-day streak**")
    else:
        st.markdown("**Day 1 — let's bank your first session.**")
    st.progress(daily_completion)
    if daily_done == 0:
        st.caption(f"0 of {len(DAILY_PLAN)} days — press **Start Today** to begin.")
    else:
        st.caption(f"{daily_done} of {len(DAILY_PLAN)} daily missions complete")

    # Lesson selection moved out of the sidebar dropdown and into the Lessons
    # tab as a clickable list, so the sidebar stays calm and Day 1 isn't asked
    # to pick from a 12-item menu before doing anything.
    st.caption("📚 Open the **Lessons** tab to pick a lesson or start Lesson 1.")

    # Everything else lives behind one expander so the sidebar stays calm.
    with st.expander("Settings", expanded=False):
        new_profile_name = st.text_input(
            "Learner profile",
            value=profile_name,
            help="Use a name like your first name or study group name. It creates a separate progress file.",
        ).strip() or "guest"
        if new_profile_name != profile_name:
            st.session_state.profile_name = new_profile_name
            st.rerun()

        private_caption = private_badge_text(
            _private_status,
            unlocked=bool(st.session_state.get("private_access_ok", not _private_status.required)),
        )
        if private_caption:
            st.caption(private_caption)

        st.radio(
            "Study mode",
            ["Learn", "Practice", "Review", "Build"],
            horizontal=True,
            key="study_focus",
            help="This guides the dashboard and daily mission suggestions.",
        )

        st.progress(completion)
        st.caption(f"{completed_count} of {len(LESSONS)} lessons complete")

        if ai_is_configured():
            st.caption(f"AI: connected ({configured_model()})")
        else:
            st.caption("AI: not connected — set OPENAI_API_KEY to enable the tutor.")

        if code_runner_enabled():
            st.caption("Code runner: enabled (local use)")
        else:
            st.caption("Code runner: off (safe-sharing default)")

    with st.expander("Progress tools", expanded=False):
        st.download_button(
            "Download my progress JSON",
            data=safe_json(progress_data),
            file_name=f"ai_code_tutor_progress_{profile_slug(profile_name)}.json",
            mime="application/json",
        )
        st.download_button(
            "Download private backup pack",
            data=backup_zip_bytes(profile_name, profile_slug(profile_name), progress_data, LESSONS, DAILY_PLAN),
            file_name=f"ai_code_tutor_backup_{profile_slug(profile_name)}.zip",
            mime="application/zip",
        )
        st.download_button(
            "Download learning transcript",
            data=learning_transcript_markdown(profile_name, progress_data, LESSONS, DAILY_PLAN),
            file_name=f"learning_transcript_{profile_slug(profile_name)}.md",
            mime="text/markdown",
        )
        uploaded_progress = st.file_uploader("Import progress JSON or backup JSON", type=["json"])
        if uploaded_progress is not None and st.button("Import progress"):
            try:
                imported_payload = json.loads(uploaded_progress.getvalue().decode("utf-8"))
                imported = unwrap_progress_import(imported_payload)
                if not isinstance(imported, dict):
                    st.error("That file was valid JSON, but it was not a progress object or AI Code Tutor backup.")
                else:
                    imported = normalize_progress_data(imported, LESSON_IDS, profile_name=profile_name)
                    save_progress(imported, progress_path)
                    st.success("Progress imported and normalized for the current app version.")
                    st.rerun()
            except (UnicodeDecodeError, json.JSONDecodeError):
                st.error("That file was not valid JSON.")

        confirm_reset = st.checkbox("I understand this deletes this profile's progress")
        if confirm_reset and st.button("Reset this profile"):
            if progress_path.exists():
                progress_path.unlink()
            st.session_state.ai_messages = []
            st.rerun()

lesson = get_lesson_by_id(st.session_state.selected_lesson_id)
completed_lessons = set(progress_data.get("completed_lessons", []))
lesson_complete = lesson.id in completed_lessons
next_lesson = get_lesson_by_id(first_incomplete_lesson_id(progress_data))
hero_mission = next_mission(progress_data)
hero_xp = calculate_xp(progress_data)
hero_streak = int(progress_data.get("study_streak", 0) or 0)

st.markdown(
    f"""
<a class="skip-link" href="#today-30-minute-coding-session">Skip to today's session</a>
<div class="compact-hero">
    <h1>AI Code Tutor</h1>
    <p>Daily coding gym for Python basics. Start today, do one rep at a time, save proof, and stop.</p>
    <div class="hero-meta">
        <span class="hero-stat">Day {h(hero_mission.day)}: {h(hero_mission.title)}</span>
        <span class="hero-stat">Next: {h(next_lesson.title)}</span>
        <span class="hero-stat">Streak: {h(hero_streak)} day{'s' if hero_streak != 1 else ''}</span>
        <span class="hero-stat">XP: {h(hero_xp)}</span>
    </div>
</div>
""".strip(),
    unsafe_allow_html=True,
)

# First-run welcome: only for a brand-new profile (no lessons, no missions yet),
# point straight at Lesson 1 so day one has one obvious next step.
if completed_count == 0 and daily_done == 0:
    st.info(
        "👋 **New here?** Open the **📚 Lessons** tab and press "
        "**▶ Start Lesson 1 — Python mindset** to begin. Each session is about 30 minutes: "
        "read a little, try the quiz, and save one small win."
    )

# Flat, single-row navigation: seven scannable destinations instead of the old
# tabs-inside-tabs (3 groups -> 13 sub-tabs). Lower-traffic surfaces (Focus
# Coach, AI Certs, Prompt Lab, Notes, Deploy) move into expanders so every
# feature is still reachable without crowding the top bar.
(
    today_tab,
    lessons_tab,
    practice_tab,
    projects_tab,
    ai_tutor_tab,
    progress_tab,
    more_tab,
) = st.tabs(
    [
        "🏠 Today",
        "📚 Lessons",
        "✏️ Practice",
        "🛠️ Projects",
        "🤖 AI Tutor",
        "📈 Progress",
        "⋯ More",
    ]
)

with today_tab:
    render_today_tab(progress_data, progress_path)
    with st.expander("🧘 Focus coach", expanded=False):
        render_focus_tab(progress_data, progress_path, lesson)

with lessons_tab:
    render_lesson_tab(progress_data, progress_path, lesson, lesson_complete)

with practice_tab:
    render_review_tab(progress_data)
    st.divider()
    st.subheader("📝 Current lesson quiz")
    render_quiz_tab(progress_data, progress_path, lesson)
    st.divider()
    st.subheader("💻 Code Lab")
    render_code_tab(lesson)

with projects_tab:
    render_projects_tab(progress_data, progress_path)

with ai_tutor_tab:
    render_ai_tab(lesson)

with progress_tab:
    render_path_tab(progress_data, profile_name)
    st.divider()
    render_dashboard_tab(progress_data, lesson, next_lesson)

with more_tab:
    with st.expander("📖 Glossary (all key terms)", expanded=False):
        render_glossary_tab()
    with st.expander("🎓 AI certifications & official resources", expanded=False):
        render_official_ai_tab(progress_data, progress_path)
    with st.expander("💡 Prompt lab", expanded=False):
        render_prompt_tab(progress_data, progress_path, lesson)
    with st.expander("📝 Notes", expanded=False):
        render_notes_tab(progress_data, progress_path, lesson)
    with st.expander("🚀 Deploy & share", expanded=False):
        render_deploy_tab(progress_path)

st.divider()
# Hide dev-facing storage details behind an expander — the file path and
# multi-user warning are not useful to learners on the main surface.
with st.expander("Where is my progress saved?", expanded=False):
    st.caption(
        f"Progress for profile `{profile_name}` is saved at `{progress_path}`. "
        "For a serious multi-user app, replace file storage with a database and add authentication."
    )
