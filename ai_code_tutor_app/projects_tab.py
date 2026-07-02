"""Projects tab — the Build Studio (guided builds) plus capstone checkpoints.

Buildable projects get a step-by-step studio: instructions, a persistent code
editor, static structure checks that work even where the code runner is off,
and a download of the finished program. Every project keeps the original
milestone checklist as a second mode. Imports come straight from the leaf
domain modules so there is no dependency back on ``app.py``, keeping the
per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from build_checks import all_checks_pass, run_static_checks
from code_runner import code_runner_enabled, run_python_with_tests
from curriculum import get_lesson_by_id
from progress import (
    record_build_step,
    record_project_milestone,
    save_build_code,
    save_progress,
)
from project_builds import (
    build_completion_percent,
    build_for_project,
    editor_seed,
    guide_code_before_step,
    next_build_step_index,
    passed_build_steps,
)
from projects import (
    PROJECTS,
    completed_project_milestones_count,
    next_project_milestone,
    project_completion_percent,
    project_progress,
    recommended_project_id,
)
from ui_components import render_card, select_pace_control
from ui_safety import h

MODE_BUILD = "🏗️ Build it"
MODE_CHECKLIST = "📋 Checkpoints"


def render_project_summary(project, progress_data: dict) -> None:
    completion = int(project_completion_percent(progress_data, project.id) * 100)
    milestone = next_project_milestone(progress_data, project.id)
    build_note = "Guided build available in the studio." if build_for_project(project.id) else "Checklist track — bring your own editor."
    st.markdown(
        f"""
<div class="project-card">
    <h3>{h(project.title)}</h3>
    <p><strong>{h(project.level)}</strong> · about {h(project.minutes)} min total · {h(completion)}% complete</p>
    <p>{h(project.description)}</p>
    <p><strong>Next milestone:</strong> {h(milestone.title)} · <em>{h(build_note)}</em></p>
    <p><strong>Skills:</strong> {h(', '.join(project.skills))}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )


def _lesson_titles(lesson_ids) -> str:
    titles = []
    for lesson_id in lesson_ids:
        try:
            titles.append(get_lesson_by_id(lesson_id).title)
        except (KeyError, StopIteration):
            titles.append(lesson_id)
    return ", ".join(titles)


def render_build_studio(build, project, progress_data: dict, progress_path) -> None:
    passed = passed_build_steps(progress_data, project.id)
    total_steps = len(build.steps)
    done_steps = sum(1 for step in build.steps if step.id in passed)

    st.write(build.intro)
    st.progress(build_completion_percent(progress_data, build))
    st.caption(f"{done_steps} of {total_steps} build steps passed. Your code saves with your profile, so you can stop anytime.")

    step_labels = [
        f"{index + 1}. {step.title}" + (" ✅" if step.id in passed else "")
        for index, step in enumerate(build.steps)
    ]
    default_index = next_build_step_index(progress_data, build)
    picked_label = select_pace_control(
        "Build steps",
        step_labels,
        index=default_index,
        key=f"build_step_{project.id}",
        help_text="One step at a time. Each step adds a little more real code to your program.",
    ) or step_labels[default_index]
    step_index = step_labels.index(picked_label)
    step = build.steps[step_index]

    instruction_items = "".join(f"<li>{h(item)}</li>" for item in step.instructions)
    st.markdown(
        f"""
<div class="milestone-card current">
    <h3>Step {step_index + 1} of {total_steps}: {h(step.title)}</h3>
    <p><strong>Goal:</strong> {h(step.goal)}</p>
    <ul>{instruction_items}</ul>
    <p class="small-muted"><strong>Uses what you learned in:</strong> {h(_lesson_titles(step.lesson_ids))}</p>
</div>
""".strip(),
        unsafe_allow_html=True,
    )
    if st.toggle("💡 Stuck? Show the hint", value=False, key=f"build_hint_{project.id}_{step.id}"):
        st.info(step.hint)

    editor_key = f"build_code_{project.id}"
    if editor_key not in st.session_state:
        st.session_state[editor_key] = editor_seed(progress_data, build)

    catch_up_cols = st.columns(2)
    if catch_up_cols[0].button(
        "↩️ Load the guide's code up to this step",
        key=f"build_catchup_{project.id}_{step.id}",
        help="Replaces the editor with the guide's version of the program just before this step — handy if you got lost.",
        use_container_width=True,
    ):
        st.session_state[editor_key] = guide_code_before_step(build, step_index)
        st.rerun()
    if catch_up_cols[1].button(
        "💾 Save my code",
        key=f"build_save_{project.id}_{step.id}",
        use_container_width=True,
    ):
        save_build_code(progress_data, project.id, st.session_state.get(editor_key, ""))
        save_progress(progress_data, progress_path)
        st.toast("Code saved to your profile.")

    user_code = st.text_area(
        "Your program (it grows every step)",
        height=340,
        key=editor_key,
    )

    if st.button("✅ Check this step", type="primary", key=f"build_check_{project.id}_{step.id}", use_container_width=True):
        save_build_code(progress_data, project.id, user_code)
        results = run_static_checks(user_code, step.checks)
        checks_ok = all_checks_pass(results)
        runner_result = None
        if code_runner_enabled():
            runner_result = run_python_with_tests(user_code, step.tests)
        step_passed = checks_ok and (runner_result is None or runner_result.ok)

        for result in results:
            icon = "✅" if result.passed else "❌"
            st.write(f"{icon} {result.check.message} — {result.detail}")
        if runner_result is not None:
            if runner_result.ok:
                st.write("✅ Local test run — every assert passed.")
            else:
                st.write("❌ Local test run failed:")
                st.code((runner_result.stderr or runner_result.stdout or "No output.").strip())

        if step_passed:
            record_build_step(progress_data, project.id, step.id, code=user_code)
            record_project_milestone(
                progress_data,
                project.id,
                step.id,
                "Completed",
                note=f"Build Studio: passed '{step.title}'.",
            )
            save_progress(progress_data, progress_path)
            if done_steps + 1 >= total_steps:
                st.balloons()
                st.success("That was the last step — you built the whole program! Download it below and run it yourself.")
            else:
                st.success("Step passed and saved! Pick the next step above when you're ready.")
        else:
            save_progress(progress_data, progress_path)
            st.warning("Not there yet — fix the ❌ items above and check again. Wrong turns are part of the workout.")

    st.subheader("Take it with you")
    st.caption(f"This is a real Python file you wrote. {build.run_hint}")
    st.download_button(
        f"⬇️ Download {build.filename}",
        data=st.session_state.get(editor_key, ""),
        file_name=build.filename,
        mime="text/x-python",
        key=f"build_download_{project.id}",
    )
    if not code_runner_enabled():
        st.caption(
            "Structure checks run right here. To also execute the step's tests in-app, run the app "
            "locally with `ALLOW_CODE_RUNNER=true` — or run your downloaded file with any Python."
        )

    if done_steps >= total_steps:
        render_card(
            "You shipped it 🎉",
            f"Every step of {project.title} passed. Next level: run it on your machine, change one thing "
            "on purpose (a new feedback tier, a new habit field), and watch your program respond.",
            "success-soft",
        )


def render_milestone_checklist(selected_project, progress_data: dict, progress_path) -> None:
    saved_milestones = project_progress(progress_data, selected_project.id)
    for milestone in selected_project.milestones:
        if st.toggle(f"{milestone.title} - {saved_milestones.get(milestone.id, {}).get('status', 'Not started')}", value=saved_milestones.get(milestone.id, {}).get("status") in {None, "Not started", "In progress"}, key=f"project_toggle_{selected_project.id}_{milestone.id}"):
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


def render_projects_tab(progress_data: dict, progress_path) -> None:
    st.header("🛠️ Projects & capstone checkpoints")
    st.write(
        "Projects make the lessons feel real. Buildable tracks open a guided studio where you write the "
        "actual program step by step; every track keeps tiny checkpoints so you can build without getting overwhelmed."
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
    recommended_index = next(index for index, project in enumerate(PROJECTS) if project.id == recommended.id)
    selected_project_label = select_pace_control(
        "Choose a project track",
        project_labels,
        index=recommended_index,
        key="project_track_choice",
        help_text="Tracks with a guided build open the Build Studio.",
    ) or project_labels[recommended_index]
    selected_project = PROJECTS[project_labels.index(selected_project_label)]
    render_project_summary(selected_project, progress_data)
    st.progress(project_completion_percent(progress_data, selected_project.id))

    build = build_for_project(selected_project.id)
    if build is not None:
        mode = select_pace_control(
            "How do you want to work?",
            [MODE_BUILD, MODE_CHECKLIST],
            index=0,
            key=f"project_mode_{selected_project.id}",
            help_text="Build it walks you through writing the real program. Checkpoints is the classic proof checklist.",
        ) or MODE_BUILD
        if mode == MODE_BUILD:
            render_build_studio(build, selected_project, progress_data, progress_path)
        else:
            st.subheader("Milestones")
            render_milestone_checklist(selected_project, progress_data, progress_path)
    else:
        st.subheader("Milestones")
        render_milestone_checklist(selected_project, progress_data, progress_path)

    st.subheader("All project tracks")
    for project in PROJECTS:
        render_project_summary(project, progress_data)
