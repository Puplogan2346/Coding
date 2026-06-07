import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"
# app.py is now a thin composition layer: each tab was extracted into its own
# ``*_tab.py`` module, with shared leaf renderers in ``ui_components.py``.
# Static-integrity checks for tab UI and dependency wiring search across the
# whole wired surface (app.py + ui_components + every per-tab module), so they
# stay meaningful no matter which module a given string or import lives in.
UI_COMPONENTS_PATH = ROOT / "ui_components.py"
_WIRED_MODULE_PATHS = (APP_PATH, UI_COMPONENTS_PATH, *sorted(ROOT.glob("*_tab.py")))


def _imported_names_from(module_name: str, path: Path = APP_PATH) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module_name:
            for alias in node.names:
                names.append(alias.asname or alias.name)
    return names


def _imported_names_anywhere(module_name: str) -> set[str]:
    """Names imported from ``module_name`` by app.py OR any wired module."""
    names: set[str] = set()
    for path in _WIRED_MODULE_PATHS:
        names.update(_imported_names_from(module_name, path))
    return names


def _assert_no_duplicate_imports(module_name: str) -> None:
    """Each wired module should import each name from ``module_name`` once."""
    for path in _WIRED_MODULE_PATHS:
        names = _imported_names_from(module_name, path)
        assert len(names) == len(set(names)), (
            f"Duplicate {module_name} imports in {path.name} create noisy "
            "maintenance risk."
        )


def _wired_source() -> str:
    """Combined source of app.py and the per-tab modules it composes."""
    return "\n".join(path.read_text(encoding="utf-8") for path in _WIRED_MODULE_PATHS)


def test_official_ai_app_dependencies_are_imported_once():
    names = _imported_names_anywhere("official_ai_resources")
    assert "provider_counts" in names
    assert "resource_has_certificate" in names
    assert "OFFICIAL_AI_STARTER_PATH" in names
    _assert_no_duplicate_imports("official_ai_resources")


def test_progress_imports_do_not_duplicate_names():
    _assert_no_duplicate_imports("progress")


def test_app_uses_shared_starter_path_constant():
    source = _wired_source()
    assert "starter_ids = OFFICIAL_AI_STARTER_PATH" in source
    assert '("gumloop_ai_fundamentals", "gumloop_getting_started", "anthropic_academy")' not in source


def test_app_exposes_today_tab_and_daily_training_imports():
    # Navigation is now a single flat row of seven tabs (no tabs-inside-tabs).
    # The destinations are delegated to per-tab modules, so dependency wiring is
    # checked across the whole wired surface.
    app_source = APP_PATH.read_text(encoding="utf-8")
    for block in (
        "with today_tab:",
        "with lessons_tab:",
        "with practice_tab:",
        "with projects_tab:",
        "with ai_tutor_tab:",
        "with progress_tab:",
        "with more_tab:",
    ):
        assert block in app_source, f"missing flat-nav block: {block}"
    # Every destination still calls its per-tab renderer from the flat layout.
    for call in (
        "render_today_tab(",
        "render_focus_tab(",
        "render_lesson_tab(",
        "render_quiz_tab(",
        "render_code_tab(",
        "render_projects_tab(",
        "render_ai_tab(",
        "render_path_tab(",
        "render_dashboard_tab(",
        "render_official_ai_tab(",
        "render_prompt_tab(",
        "render_notes_tab(",
        "render_deploy_tab(",
    ):
        assert call in app_source, f"missing per-tab render call: {call}"
    assert "record_daily_mission" in _imported_names_anywhere("progress")
    assert "completed_daily_missions_count" in _imported_names_anywhere("progress")
    source = _wired_source()
    assert "from study_plan import DAILY_PLAN" in source
    assert "render_daily_mission_card" in source
    assert "render_focus_blocks" in source


def test_app_mentions_30_minute_daily_habit():
    source = _wired_source()
    assert "30-minute coding session" in source
    assert "30-minute mission" in source
    assert "Badge shelf" in source
    assert "ADHD-friendly setup" in source
    assert "Projects & capstone checkpoints" in source
    assert "Learning Path: Python basics to capstone" in source
    assert "Graduation checklist" in source


def test_app_imports_focus_and_project_dependencies():
    focus_names = _imported_names_anywhere("focus_coach")
    project_names = _imported_names_anywhere("projects")
    progress_names = _imported_names_anywhere("progress")

    assert "focus_blocks" in focus_names
    assert "recommended_focus_mode" in focus_names
    assert "PROJECTS" in project_names
    assert "recommended_project_id" in project_names
    assert "record_focus_checkin" in progress_names
    assert "record_project_milestone" in progress_names
    assert "add_parking_lot_item" in progress_names


def test_app_escapes_learner_text_before_raw_html_rendering():
    # The escape helpers all come from the shared ui_safety module. After the
    # per-tab split, each module imports only the helpers it uses (app.py keeps
    # ``h``; the parking-lot escaping lives in focus_tab.py), so check that the
    # helpers are wired in across modules rather than pinning one import line.
    safety_names = _imported_names_anywhere("ui_safety")
    assert {"h", "safe_html_text", "truncate_text"} <= safety_names
    source = _wired_source()
    assert "safe_thought = safe_html_text(truncate_text(item.get" in source
    assert "{item.get('thought', '')}</div>" not in source


def test_app_has_low_stimulation_theme_hook_and_import_validation():
    source = APP_PATH.read_text(encoding="utf-8")
    assert "def apply_theme(low_stimulation: bool = False)" in source
    assert "apply_theme(low_stimulation=bool(progress_data.get" in source
    assert "if not isinstance(imported, dict):" in source


def test_progress_download_filename_uses_safe_slug():
    source = APP_PATH.read_text(encoding="utf-8")
    assert "profile_slug" in source
    assert 'file_name=f"ai_code_tutor_progress_{profile_slug(profile_name)}.json"' in source


def test_imported_progress_is_normalized_before_saving():
    source = APP_PATH.read_text(encoding="utf-8")
    assert "normalize_progress_data(imported, LESSON_IDS, profile_name=profile_name)" in source


def test_today_tab_uses_one_consolidated_checklist_without_legacy_helpers():
    # The Today tab's checklist and nudges are built from the gym-block system
    # (gym_blocks_for_choice / next_gym_action), which superseded the older
    # daily_coach.daily_session_checklist path. Assert the single consolidated
    # checklist exists and none of the legacy scattered helpers came back.
    source = _wired_source()
    legacy_names = {
        "today_session_steps",
        "session_readiness_message",
        "weekly_checkpoint_label",
        "checklist_completion_percent",
        "next_tiny_action",
        # Superseded by the gym-block checklist; must not be re-wired into a tab.
        "daily_session_checklist",
        "daily_session_nudge",
    }
    for name in legacy_names:
        assert name not in source
    assert "One-screen checklist" in source
    assert "gym_blocks_for_choice" in source
    assert source.count("Save current draft") == 1


def test_app_imports_progress_normalizer_used_by_import_flow():
    names = _imported_names_from("progress")
    assert "normalize_progress_data" in names
    source = APP_PATH.read_text(encoding="utf-8")
    assert "normalize_progress_data(imported, LESSON_IDS, profile_name=profile_name)" in source


def test_app_exposes_v11_daily_coding_gym_ui():
    source = _wired_source()
    assert "Today: Daily Coding Gym" in source
    assert "Start Today" in source
    assert "Time I have today" in source
    assert "One-screen checklist" in source
    assert "Proof card" in source
    assert "Mistake notebook" in source
    assert "Review queue" in source
    assert "render_gym_block" in source
    assert "gym_blocks_for_choice" in source
    assert "build_review_items" in source


def test_v11_keeps_accessible_controls_and_focus_preferences_polish():
    source = _wired_source()
    assert "render_timeline_legend" in source
    assert "select_pace_control" in source
    assert "st.pills" in source
    assert "Focus preferences saved." in source
    assert "st.rerun()" in source[source.index("Focus preferences saved."):]
    coding_gym_names = _imported_names_anywhere("coding_gym")
    assert "gym_blocks_for_choice" in coding_gym_names
    progress_names = _imported_names_anywhere("progress")
    assert "record_gym_session" in progress_names
    assert "add_mistake_card" in progress_names


def test_v13_stop_resume_and_time_based_lesson_ui_are_present():
    source = _wired_source()
    assert "Stop & save for later" in source
    assert "Stopped and saved. When you come back" in source
    assert "Today's lesson based on time" in source
    assert "workout_lesson_options" in source
    assert "Remember {selected_choice.label}" in source
    assert "Mark selected lesson complete when this workout is completed" in source
    assert source.count("record_daily_checklist(progress_data, mission.day, current_state)") == 1


def test_v15_learning_path_and_standalone_checks_are_wired():
    source = _wired_source()
    learning_names = _imported_names_anywhere("learning_path")
    standalone_names = _imported_names_anywhere("standalone_check")
    assert "current_milestone_status" in learning_names
    assert "graduation_readiness" in learning_names
    assert "standalone_checks" in standalone_names
    assert "standalone_summary" in standalone_names
    assert "render_milestone_status" in source
    assert "render_standalone_check" in source
    assert "Standalone readiness check" in source
