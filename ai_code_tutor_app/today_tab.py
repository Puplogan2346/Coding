"""Today tab — the Daily Coding Gym.

This is the highest-traffic surface in the app, so it lives in its own module.
``render_today_tab`` is the single entry point; ``app.py`` calls it from inside
its ``with today_tab:`` block. The module imports its dependencies directly from
the leaf domain modules (no dependency back on ``app.py``), keeping the split
acyclic.
"""
from __future__ import annotations

import streamlit as st

from coding_gym import (
    build_review_items,
    gym_blocks_for_choice,
    gym_completion,
    gym_history_summary,
    gym_motivation_copy,
    gym_progress_label,
    gym_session_history,
    next_gym_action,
    proof_card_summary,
    total_gym_minutes,
    workout_finish_status,
    workout_lesson_options,
    workout_resume_setup,
    workout_resume_summary,
    workout_save_decision,
)
from curriculum import LESSONS, get_lesson_by_id
from experience import (
    SESSION_LABELS,
    daily_timeline,
    merge_step_state,
    percent_label,
    plan_progress_sentence,
    session_choice_by_label,
)
from focus_coach import ENERGY_LEVELS, FOCUS_LEVELS, focus_blocks, recommended_focus_mode
from gamification import calculate_xp, level_for_xp
from learning_path import current_milestone_status, first_incomplete_lesson_id
from official_ai_resources import resources_for_ids
from progress import (
    add_mistake_card,
    add_parking_lot_item,
    close_mistake_card,
    completed_daily_missions_count,
    daily_checklist_steps,
    gym_session_for_day,
    gym_session_is_active,
    gym_session_is_saved,
    mark_lesson_complete,
    pause_gym_session,
    record_daily_checklist,
    record_daily_mission,
    record_gym_session,
    save_focus_preferences,
    save_progress,
    start_gym_session,
)
from smooth_workout import (
    current_focus_card,
    daily_use_smoothness_checks,
    focus_completion_sentence,
    mark_focus_step_done,
    resume_safety_report,
)
from study_plan import DAILY_PLAN, next_mission, review_queue
from ui_components import (
    render_badge_shelf,
    render_card,
    render_daily_mission_card,
    render_daily_timeline,
    render_done_zone,
    render_focus_blocks,
    render_focus_workout_card,
    render_gym_block,
    render_gym_history_item,
    render_proof_preview,
    render_resume_banner,
    render_review_item,
    render_smoothness_check,
    render_time_blocks,
    render_timeline_legend,
    select_pace_control,
)
from ui_safety import h, truncate_text

# LESSON_IDS mirrors app.py's module-level constant; recomputed here so the tab
# module stays self-contained.
LESSON_IDS = [lesson.id for lesson in LESSONS]


def open_mistake_cards(progress_data: dict) -> list[tuple[int, dict]]:
    return [
        (index, card)
        for index, card in enumerate(progress_data.get("mistake_cards", []) or [])
        if card.get("status", "Open") == "Open"
    ]


def render_today_tab(progress_data: dict, progress_path) -> None:
    mission = next_mission(progress_data)
    st.markdown("<h1 id=\"today-30-minute-coding-session\">🏠 Today\'s Coding Gym</h1>", unsafe_allow_html=True)
    st.caption("A 30-minute coding session with one path: choose time, press Start or Resume, finish one rep, save proof, stop. Today: Daily Coding Gym.")

    with st.expander("Path and milestone details", expanded=False):
        timeline_days = daily_timeline(progress_data, len(DAILY_PLAN))
        st.caption(plan_progress_sentence(progress_data))
        render_daily_timeline(timeline_days)
        render_timeline_legend(timeline_days)
        today_milestone = current_milestone_status(progress_data)
        render_card(
            f"Current learning milestone: {today_milestone.milestone.title}",
            f"{percent_label(today_milestone.percent)} done. Goal: {today_milestone.milestone.goal} Next: {today_milestone.next_action}",
            "success-soft" if today_milestone.status == "Complete" else "",
        )

    existing_gym_session = gym_session_for_day(progress_data, mission.day)
    gym_saved = gym_session_is_saved(progress_data, mission.day)
    gym_active = gym_session_is_active(progress_data, mission.day)
    preferred_minutes = (progress_data.get("focus_preferences", {}) or {}).get("default_minutes", 30)
    resume_setup = workout_resume_setup(existing_gym_session, preferred_minutes, LESSON_IDS)
    saved_pace = resume_setup.pace_label if resume_setup.locked else None
    saved_lesson_id = resume_setup.lesson_id
    default_pace_index = SESSION_LABELS.index(resume_setup.pace_label)
    setup_locked = bool(resume_setup.locked and (gym_active or gym_saved))

    toolbar_cols = st.columns([1.25, 0.8, 0.8])
    with toolbar_cols[0]:
        if setup_locked:
            session_pace = saved_pace or SESSION_LABELS[default_pace_index]
            st.selectbox(
                "Time I have today",
                SESSION_LABELS,
                index=SESSION_LABELS.index(session_pace),
                key=f"today_session_pace_locked_{mission.day}",
                disabled=True,
                help="This workout was already started, so the app keeps the saved pace for a clean resume.",
            )
            st.caption("Resume mode: pace is locked so your saved checklist still matches the workout.")
        else:
            session_pace = select_pace_control(
                "Time I have today",
                SESSION_LABELS,
                index=default_pace_index,
                key=f"today_session_pace_{mission.day}",
                help_text="Choose rescue when starting feels hard. Rescue mode still counts.",
            ) or SESSION_LABELS[default_pace_index]
            saved_default_label = SESSION_LABELS[default_pace_index]
            st.caption(f"Time I have today: 10, 30, or 45 minutes · saved default: {saved_default_label}.")
    with toolbar_cols[1]:
        today_energy = select_pace_control(
            "Energy", list(ENERGY_LEVELS), index=1, key=f"today_energy_{mission.day}",
            help_text="How much fuel you have right now.",
        ) or ENERGY_LEVELS[1]
    with toolbar_cols[2]:
        today_focus = select_pace_control(
            "Focus", list(FOCUS_LEVELS), index=1, key=f"today_focus_{mission.day}",
            help_text="How locked-in you feel right now.",
        ) or FOCUS_LEVELS[1]

    selected_choice = session_choice_by_label(session_pace)
    if setup_locked:
        st.caption(f"Resuming saved workout: {selected_choice.label}. The lesson and checklist stay locked until you save or skip this session.")
    remember_on_start = False
    if not setup_locked:
        remember_on_start = st.checkbox(
            "Make this workout length my default for future days",
            value=False,
            key=f"remember_pace_on_start_{mission.day}",
            help="This saves your selected 10/30/45 minute length as the default for future sessions when you start today's workout.",
        )
    if not setup_locked and selected_choice.minutes != int(preferred_minutes or 30):
        preference_cols = st.columns([0.7, 1.4])
        with preference_cols[0]:
            if st.button(f"Remember {selected_choice.label}", key=f"remember_pace_{mission.day}"):
                save_focus_preferences(progress_data, {"default_minutes": selected_choice.minutes})
                save_progress(progress_data, progress_path)
                st.success(f"Default workout saved as {selected_choice.label}.")
                st.rerun()
        with preference_cols[1]:
            st.caption(
                "This only changes your default for future days. Today's started workouts keep their saved pace so you can resume cleanly."
            )

    review_lesson_ids_for_time = [item.lesson_id for item in build_review_items(progress_data, LESSON_IDS, max_items=5)]
    lesson_options = workout_lesson_options(
        progress_data,
        LESSONS,
        mission,
        selected_choice.minutes,
        review_lesson_ids=review_lesson_ids_for_time or review_queue(progress_data, LESSON_IDS),
        current_lesson_id=saved_lesson_id if setup_locked else None,
    )
    if not lesson_options:
        active_lesson_id = mission.lesson_id or first_incomplete_lesson_id(progress_data)
        active_lesson_reason = "safe fallback"
    else:
        option_labels = [option.label for option in lesson_options]
        option_by_label = {option.label: option for option in lesson_options}
        default_lesson_label = option_labels[0]
        if saved_lesson_id:
            for option in lesson_options:
                if option.lesson_id == saved_lesson_id:
                    default_lesson_label = option.label
                    break
        lesson_choice_key = f"today_lesson_choice_{mission.day}_{selected_choice.minutes}"
        if setup_locked:
            selected_lesson_label = select_pace_control(
                "Today's lesson based on time",
                option_labels,
                index=option_labels.index(default_lesson_label),
                key=f"{lesson_choice_key}_locked",
                help_text="This workout already has a saved lesson so you can continue where you stopped.",
                disabled=True,
            ) or default_lesson_label
            st.caption("Resume mode: lesson is locked to the one saved with this workout.")
        else:
            selected_lesson_label = select_pace_control(
                "Today's lesson based on time",
                option_labels,
                index=option_labels.index(default_lesson_label),
                key=lesson_choice_key,
                help_text="Short sessions suggest review or a tiny next step. Longer sessions suggest the full lesson or stretch work.",
            ) or default_lesson_label
        active_option = option_by_label[selected_lesson_label]
        active_lesson_id = active_option.lesson_id
        active_lesson_reason = active_option.reason
    active_lesson = get_lesson_by_id(active_lesson_id)
    st.caption(f"Lesson for the time you have today: {active_lesson.title} · {active_lesson_reason} · fits {selected_choice.minutes} min.")

    if not setup_locked:
        with st.expander("Preview how time changes the lesson", expanded=False):
            st.caption("This lets you change today's lesson before you start, based on whether you have 10, 30, or 45 minutes.")
            preview_cols = st.columns(3)
            for col, minutes, pace_label in zip(preview_cols, (10, 30, 45), SESSION_LABELS):
                preview_options = workout_lesson_options(
                    progress_data,
                    LESSONS,
                    mission,
                    minutes,
                    review_lesson_ids=review_lesson_ids_for_time or review_queue(progress_data, LESSON_IDS),
                )
                preview_option = preview_options[0] if preview_options else None
                if preview_option:
                    preview_lesson = get_lesson_by_id(preview_option.lesson_id)
                    preview_body = f"{preview_lesson.title}. Reason: {preview_option.reason}."
                else:
                    preview_body = "Use the current daily mission as a safe fallback."
                with col:
                    render_card(pace_label, preview_body)
            st.caption("After you press Start Today, the app locks the selected time and lesson so Stop & save for later can resume cleanly.")

    resume_summary = workout_resume_summary(progress_data, mission.day)
    if resume_summary and not gym_saved:
        render_resume_banner(resume_summary, active_lesson.title)

    proof_key = f"gym_proof_{mission.day}"
    review_key = f"gym_next_review_{mission.day}"
    gym_blocks = gym_blocks_for_choice(selected_choice)

    if setup_locked and gym_active and not gym_saved:
        with st.expander("Time changed since you paused?", expanded=False):
            st.caption("Use this only when you truly need to resize the saved workout. The app will keep your proof draft and compatible checked reps.")
            convert_pace = st.selectbox(
                "Change this saved workout to",
                SESSION_LABELS,
                index=SESSION_LABELS.index(selected_choice.label),
                key=f"convert_pace_{mission.day}",
            )
            convert_choice = session_choice_by_label(convert_pace)
            convert_options = workout_lesson_options(
                progress_data,
                LESSONS,
                mission,
                convert_choice.minutes,
                review_lesson_ids=review_lesson_ids_for_time or review_queue(progress_data, LESSON_IDS),
                current_lesson_id=active_lesson_id,
            )
            convert_labels = [option.label for option in convert_options]
            if convert_labels:
                convert_label = st.selectbox("Lesson for the new time", convert_labels, key=f"convert_lesson_{mission.day}_{convert_choice.minutes}")
                convert_option = {option.label: option for option in convert_options}[convert_label]
                if st.button("Convert saved workout", key=f"convert_workout_{mission.day}"):
                    converted_blocks = gym_blocks_for_choice(convert_choice)
                    old_state = existing_gym_session.get("step_state", {}) or {}
                    converted_state = {block.id: bool(old_state.get(block.id, False)) for block in converted_blocks}
                    pause_gym_session(
                        progress_data,
                        mission.day,
                        pace=convert_choice.label,
                        minutes=total_gym_minutes(converted_blocks),
                        lesson_id=convert_option.lesson_id,
                        step_state=converted_state,
                        proof_note=str(st.session_state.get(proof_key, existing_gym_session.get("proof_note", ""))),
                        next_review=str(st.session_state.get(review_key, existing_gym_session.get("next_review", ""))),
                    )
                    save_progress(progress_data, progress_path)
                    st.success("Saved workout resized. It will resume with the new time and lesson.")
                    st.rerun()
            else:
                st.info("No lesson option found for that time. Keep the current saved workout.")

    saved_steps = daily_checklist_steps(progress_data, mission.day)
    saved_steps.update({str(key): bool(value) for key, value in (existing_gym_session.get("step_state", {}) or {}).items()})
    visible_steps = merge_step_state(saved_steps, st.session_state, mission.day, gym_blocks)
    gym_percent = gym_completion(visible_steps, gym_blocks)
    gym_action = next_gym_action(mission.title, visible_steps, gym_blocks, gym_saved)
    if proof_key not in st.session_state and existing_gym_session.get("proof_note"):
        st.session_state[proof_key] = existing_gym_session.get("proof_note", "")
    if review_key not in st.session_state and existing_gym_session.get("next_review"):
        st.session_state[review_key] = existing_gym_session.get("next_review", "")
    proof_note = st.session_state.get(proof_key, "")

    st.markdown(
        f"""
<div class="daily-action-card">
    <h2>Day {h(mission.day)}: {h(mission.title)}</h2>
    <p><strong>Do this now:</strong> {h(gym_action.body)}</p>
    <div class="hero-meta">
        <span class="hero-stat">{h(selected_choice.label)}</span>
        <span class="hero-stat">{h(total_gym_minutes(gym_blocks))} min</span>
        <span class="hero-stat">{h(percent_label(gym_percent))} done</span>
        <span class="hero-stat">{h('Saved' if gym_saved else 'In progress' if gym_active or gym_percent > 0 else 'Not started')}</span>
    </div>
</div>
""".strip(),
        unsafe_allow_html=True,
    )
    st.progress(gym_percent)
    st.caption(gym_motivation_copy(gym_percent, selected_choice.label, gym_saved))

    start_key = f"gym_started_{mission.day}"
    workout_started = bool(st.session_state.get(start_key, False) or gym_percent > 0 or gym_saved or gym_active)
    if gym_active and not gym_saved:
        st.info("Resuming a workout you already started. Continue with the next open block, or save it as in progress.")
    if not workout_started:
        st.markdown(
            """
<div class="gym-start">
    <strong>Open app → press Start Today → follow one block at a time → save proof → done.</strong><br>
    <span class="small-muted">No browsing required. The rest of the app is available only when you need it.</span>
</div>
""".strip(),
            unsafe_allow_html=True,
        )
        if st.button("Start Today", type="primary", key=f"start_today_{mission.day}"):
            st.session_state[start_key] = True
            if remember_on_start:
                save_focus_preferences(progress_data, {"default_minutes": selected_choice.minutes})
            start_gym_session(
                progress_data,
                mission.day,
                pace=selected_choice.label,
                minutes=total_gym_minutes(gym_blocks),
                lesson_id=active_lesson_id,
                step_state=visible_steps,
            )
            save_progress(progress_data, progress_path)
            st.rerun()
        with st.expander("Preview today's workout", expanded=False):
            for block in gym_blocks:
                render_gym_block(block, False)
    else:
        left_today, right_today = st.columns([1.12, 1])
        with left_today:
            st.subheader("Focus Mode: one rep at a time")
            st.caption("The smooth path is one visible rep, one action button, then save. The full One-screen checklist is still below if you want manual control.")
            focus_card = current_focus_card(visible_steps, gym_blocks, session_saved=gym_saved)
            render_focus_workout_card(focus_card)
            st.caption(focus_completion_sentence(focus_card))

            # ADHD-friendly: a one-click parking lot right under the focus card,
            # so distracting thoughts get captured without leaving the rep.
            if hasattr(st, "popover"):
                with st.popover("📝 Park a thought", use_container_width=False):
                    quick_thought_focus = st.text_input(
                        "Quick thought to come back to later",
                        key=f"focus_parking_input_{mission.day}_{focus_card.block_id}",
                        placeholder="Example: look up list comprehensions tomorrow",
                    )
                    if st.button("Park it", key=f"focus_park_btn_{mission.day}_{focus_card.block_id}"):
                        if add_parking_lot_item(progress_data, quick_thought_focus, lesson_id=active_lesson_id, source="Focus card"):
                            save_progress(progress_data, progress_path)
                            st.success("Parked. Back to the rep.")
                            st.rerun()
                        else:
                            st.warning("Write a thought first.")

            focus_cols = st.columns([1.2, 1.15, 0.85])
            with focus_cols[0]:
                if not gym_saved and not focus_card.is_complete and st.button("Mark this rep done & save", type="primary", key=f"focus_done_{mission.day}_{focus_card.block_id}"):
                    current_state = {block.id: bool(st.session_state.get(f"coach_step_{mission.day}_{block.id}", visible_steps.get(block.id, False))) for block in gym_blocks}
                    current_state = mark_focus_step_done(current_state, gym_blocks)
                    pause_gym_session(
                        progress_data,
                        mission.day,
                        pace=selected_choice.label,
                        minutes=total_gym_minutes(gym_blocks),
                        lesson_id=active_lesson_id,
                        step_state=current_state,
                        proof_note=str(st.session_state.get(proof_key, "")),
                        next_review=str(st.session_state.get(review_key, "")),
                    )
                    save_progress(progress_data, progress_path)
                    st.success("Rep saved. Continue when you are ready, or stop here and come back later.")
                    st.rerun()
            with focus_cols[1]:
                if st.button("Stop & save for later", key=f"pause_gym_top_{mission.day}"):
                    current_state = {block.id: bool(st.session_state.get(f"coach_step_{mission.day}_{block.id}", visible_steps.get(block.id, False))) for block in gym_blocks}
                    pause_gym_session(
                        progress_data,
                        mission.day,
                        pace=selected_choice.label,
                        minutes=total_gym_minutes(gym_blocks),
                        lesson_id=active_lesson_id,
                        step_state=current_state,
                        proof_note=str(st.session_state.get(proof_key, "")),
                        next_review=str(st.session_state.get(review_key, "")),
                    )
                    save_progress(progress_data, progress_path)
                    st.success("Stopped and saved. You can close the app and continue later.")
                    st.rerun()
            with focus_cols[2]:
                if st.button("Save current draft", key=f"save_coach_steps_{mission.day}"):
                    current_state = {block.id: bool(st.session_state.get(f"coach_step_{mission.day}_{block.id}", visible_steps.get(block.id, False))) for block in gym_blocks}
                    pause_gym_session(
                        progress_data,
                        mission.day,
                        pace=selected_choice.label,
                        minutes=total_gym_minutes(gym_blocks),
                        lesson_id=active_lesson_id,
                        step_state=current_state,
                        proof_note=str(st.session_state.get(proof_key, "")),
                        next_review=str(st.session_state.get(review_key, "")),
                    )
                    save_progress(progress_data, progress_path)
                    st.success("Draft saved. You can close the app and continue later from this exact workout.")
                    st.rerun()

            with st.expander("Full One-screen checklist", expanded=False):
                st.caption("Manual backup view. Use this when you want to check multiple blocks at once.")
                for block in gym_blocks:
                    current_value = bool(visible_steps.get(block.id, False))
                    st.checkbox(
                        f"{block.minutes}m - {block.label}",
                        value=current_value,
                        key=f"coach_step_{mission.day}_{block.id}",
                        help=f"{block.action} Proof: {block.proof}",
                    )
                    render_gym_block(block, current_value)

            st.subheader("Today's lesson link")
            render_card(
                active_lesson.title,
                f"Matched to your {selected_choice.minutes}-minute workout: {active_lesson_reason}. Do not over-study; one clear idea is enough.",
            )
            if st.button("Open selected lesson", type="primary"):
                st.session_state.selected_lesson_id = active_lesson_id
                st.rerun()

            with st.expander("Full mission recipe", expanded=False):
                render_daily_mission_card(mission)
                render_time_blocks(mission.blocks)

        with right_today:
            st.subheader("Proof card")
            st.caption("Close the workout with one small artifact so tomorrow knows where to start.")
            proof_note = st.text_area(
                "Today I learned, fixed, or noticed...",
                key=proof_key,
                height=95,
                placeholder="Example: I learned that return gives a value back, while print only displays it.",
            )
            next_review_text = st.text_input(
                "Tomorrow, review this tiny thing",
                key=review_key,
                placeholder="Example: function return values",
            )
            finish_status, finish_message = workout_finish_status(gym_percent, proof_note, gym_saved)
            st.metric("Finish status", finish_status)
            st.caption(finish_message)
            render_proof_preview(proof_card_summary(mission.day, mission.title, proof_note, next_review_text))

            if st.button("Stop & save for later", key=f"pause_gym_{mission.day}"):
                current_state = {block.id: bool(st.session_state.get(f"coach_step_{mission.day}_{block.id}", False)) for block in gym_blocks}
                pause_gym_session(
                    progress_data,
                    mission.day,
                    pace=selected_choice.label,
                    minutes=total_gym_minutes(gym_blocks),
                    lesson_id=active_lesson_id,
                    step_state=current_state,
                    proof_note=proof_note,
                    next_review=next_review_text,
                )
                save_progress(progress_data, progress_path)
                st.success("Stopped and saved. When you come back, Today will resume this exact time, lesson, checklist, proof draft, and review note.")
                st.rerun()

            with st.form(f"save_gym_session_{mission.day}"):
                mood = select_pace_control(
                    "How did the workout feel?", ["Easy", "Good", "Stuck but learning", "Hard", "Fun"],
                    index=1, key=f"gym_mood_{mission.day}", help_text="Pick the closest vibe.",
                ) or "Good"
                mission_status = select_pace_control(
                    "Mission status", ["Completed", "In progress", "Skipped"],
                    index=0, key=f"gym_status_{mission.day}", help_text="Completed still counts on rescue days.",
                ) or "Completed"
                mark_selected_lesson = st.checkbox(
                    "Mark selected lesson complete when this workout is completed",
                    value=selected_choice.minutes >= 30,
                    key=f"mark_workout_lesson_complete_{mission.day}",
                    help="Rescue sessions can save the habit without pretending a full lesson is done.",
                )
                save_gym = st.form_submit_button("Save proof card")
            if save_gym:
                current_state = {block.id: bool(st.session_state.get(f"coach_step_{mission.day}_{block.id}", False)) for block in gym_blocks}
                current_completion = gym_completion(current_state, gym_blocks)
                save_decision = workout_save_decision(current_completion, proof_note, mission_status)
                if not save_decision.ok:
                    st.warning(save_decision.message)
                else:
                    record_daily_checklist(progress_data, mission.day, current_state)
                    record_gym_session(
                        progress_data,
                        mission.day,
                        pace=selected_choice.label,
                        status=save_decision.gym_status,
                        proof_note=proof_note,
                        next_review=next_review_text,
                        minutes=total_gym_minutes(gym_blocks),
                        lesson_id=active_lesson_id,
                        step_state=current_state,
                    )
                    record_daily_mission(progress_data, mission.day, status=save_decision.mission_status, mood=mood, reflection=proof_note)
                    if save_decision.mission_status == "Completed" and mark_selected_lesson and active_lesson_id:
                        mark_lesson_complete(progress_data, active_lesson_id)
                    save_progress(progress_data, progress_path)
                    st.success(save_decision.message)
                    st.rerun()

            st.subheader("Review queue")
            review_items = build_review_items(progress_data, LESSON_IDS)
            if review_items:
                for item in review_items[:3]:
                    render_review_item(item)
                st.caption("Full review, mixed quiz, and flashcards → **🔁 Review** tab.")
            else:
                st.info("No weak spots logged yet. After a quiz miss or bug, add one mistake card.")

            with st.expander("Mistake notebook", expanded=False):
                st.caption("Turn errors into tomorrow's warm-up instead of forgetting them.")
                concept = st.text_input("Concept", key=f"mistake_concept_{mission.day}", placeholder="Example: if statements")
                mistake = st.text_area("Mistake or confusion", key=f"mistake_text_{mission.day}", height=70, placeholder="Example: I forgot the colon after if.")
                fix = st.text_area("Correct pattern or reminder", key=f"mistake_fix_{mission.day}", height=70, placeholder="Example: if condition: then indent the next line.")
                if st.button("Add mistake card", key=f"add_mistake_{mission.day}"):
                    if add_mistake_card(progress_data, concept, mistake, fix, lesson_id=active_lesson_id):
                        save_progress(progress_data, progress_path)
                        st.success("Mistake card saved for review.")
                        st.rerun()
                    else:
                        st.warning("Write either a mistake or a fix first.")

                for index, card in open_mistake_cards(progress_data)[-3:]:
                    st.markdown(
                        f"""
<div class="review-chip">
    <strong>{h(card.get('concept', 'Review'))}</strong>
    <span>{h(truncate_text(card.get('mistake', ''), 120))}<br><b>Fix:</b> {h(truncate_text(card.get('fix', ''), 120))}</span>
</div>
""".strip(),
                        unsafe_allow_html=True,
                    )
                    if st.button("Close mistake card", key=f"close_mistake_{index}"):
                        close_mistake_card(progress_data, index)
                        save_progress(progress_data, progress_path)
                        st.rerun()

            st.subheader("ADHD-friendly setup")
            render_done_zone(gym_percent, gym_saved)
            mode = recommended_focus_mode(today_energy, selected_choice.minutes)
            st.caption(f"Recommended focus mode: {mode.title}")
            with st.expander("Show focus blocks", expanded=False):
                render_focus_blocks(focus_blocks(mode.minutes, today_energy))

            quick_thought = st.text_input("Parking lot thought", key=f"today_parking_{mission.day}", placeholder="Example: research laptops later")
            if st.button("Park thought", key=f"park_today_{mission.day}"):
                if add_parking_lot_item(progress_data, quick_thought, lesson_id=active_lesson_id, source="Today"):
                    save_progress(progress_data, progress_path)
                    st.success("Parked. Back to the next rep.")
                    st.rerun()
                else:
                    st.warning("Write a thought first.")

    gym_metrics = st.columns(4)
    xp = calculate_xp(progress_data)
    gym_metrics[0].metric("Workout", gym_progress_label(visible_steps, gym_blocks), percent_label(gym_percent))
    gym_metrics[1].metric("Daily missions", f"{completed_daily_missions_count(progress_data)}/{len(DAILY_PLAN)}")
    gym_metrics[2].metric("Streak", f"{progress_data.get('study_streak', 0)} days")
    gym_metrics[3].metric("XP", xp, level_for_xp(xp).split(" - ")[-1])

    # Extras live in a compact two-column grid (was five stacked full-width
    # rows) so the tab ends right after the workout instead of scrolling on.
    st.caption("More: 🏡 Home has today's overview · 🔁 Review has quizzes & flashcards · 📈 Progress has your level and milestones.")
    extras_left, extras_right = st.columns(2)
    with extras_left:
        with st.expander("Recent gym history", expanded=False):
            st.caption(gym_history_summary(progress_data))
            history_items = gym_session_history(progress_data, limit=5)
            if history_items:
                for history_item in history_items:
                    render_gym_history_item(history_item)
            else:
                st.info("No history yet. Save your first proof card to start the log.")

        with st.expander("Daily-use smoothness check", expanded=False):
            st.caption("Private QA for the daily habit loop: default time, stop/resume, one-rep focus mode, and proof habit.")
            for check in daily_use_smoothness_checks(progress_data, mission.day, gym_blocks, preferred_minutes):
                render_smoothness_check(check)
            resume_report = resume_safety_report(existing_gym_session, gym_blocks)
            if resume_report.can_resume:
                st.caption(f"Resume check: {resume_report.saved_blocks} block(s) saved for {resume_report.saved_pace}; lesson {resume_report.saved_lesson_id or 'not locked'}.")

    with extras_right:
        with st.expander("Badge shelf", expanded=False):
            render_badge_shelf(progress_data)
            st.caption("Levels, milestones, and the full dashboard → **📈 Progress** tab.")

        if mission.official_resource_ids:
            with st.expander("Official AI side quest", expanded=False):
                for resource in resources_for_ids(mission.official_resource_ids):
                    st.markdown(f"- [{resource.provider}: {resource.title}]({resource.url})")
