# Onboarding & Handover — AI Code Tutor

Everything a new engineer (or a future AI session) needs to take over this app: what it is, how to run/test/deploy, the architecture, the data model, the one critical constraint, the design system, conventions, and where the bodies are buried. Pairs with the private playbook skill at `.claude/skills/improve-tutor/SKILL.md`.

---

## 1. What the app is & deployment context

**AI Code Tutor** is a single-user Streamlit study app — a daily "coding gym" plus a 24-lesson Python + AI-coding curriculum with quizzes, coding challenges, a glossary, spaced-repetition flashcards, project/capstone checkpoints, an optional AI tutor, and an external-AI-certifications tracker. It is ADHD-friendly by design (one obvious next action, minimal sidebar, low-stimulation theme toggle).

- **App root:** `ai_code_tutor_app/`. The **repo root is one level up** (`Coding/`) — this matters for git and for the theme config (see §6).
- **GitHub:** `Puplogan2346/Coding` (keep private). `origin` is **SSH** (`git@github.com:Puplogan2346/Coding.git`) — SSH key auth works; HTTPS has no cached token.
- **Hosting:** Streamlit Community Cloud, main file `ai_code_tutor_app/app.py`. **Pushing to `main` auto-redeploys** — there is no separate deploy step.
- `streamlit_app.py` is a thin wrapper (`runpy.run_path("app.py")`) for platforms expecting that filename. `Dockerfile`, `docker-compose.yml`, `render.yaml`, `run_app.sh` exist for alternate hosting; Streamlit Cloud is the live target.
- **Secrets:** supply `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`) via the Streamlit **Secrets** panel, never in code. `ai_tutor.get_secret()` reads env first, then `st.secrets`.

## 2. Run locally, test, and deploy

**Run locally** (use `python3`, not `python`):
```bash
cd ai_code_tutor_app
pip install -r requirements.txt        # streamlit==1.58.0 (needs Python 3.10+), openai>=2.38.0, pytest>=8.0
streamlit run app.py
```
The app works with **no** `OPENAI_API_KEY` (AI buttons just disable).

**Test:**
```bash
cd ai_code_tutor_app
python3 -m pytest -q                   # ~150 tests, must stay green
```
Real-runtime render check (catches Streamlit errors unit tests miss):
```python
from streamlit.testing.v1 import AppTest
at = AppTest.from_file('app.py', default_timeout=30)
at.session_state['active_profile']='guest'; at.session_state['profile_name']='guest'
at.run(); assert len(at.exception) == 0
```
> A full-app `AppTest` rerun can crash on an `st.pills` serialization quirk in `today_tab`. To test a button that triggers `st.rerun()`, write a throwaway probe that renders just one `render_X_tab(...)` with mock data, `AppTest.from_file` it, `.click().run()`, then delete the probe. Pass a real `pathlib.Path` (not a str) wherever `progress_path` is expected.

**Deploy** (run git from the **repo root** `Coding/`):
```bash
git add ai_code_tutor_app/<changed files>
git commit -m "<msg>"
git pull --rebase origin main          # a devcontainer/other session may have pushed
git push origin main                   # Streamlit Cloud auto-redeploys
```
Never commit secrets; `.gitignore` excludes `.env`, `.streamlit/secrets.toml`, `data/progress_*.json`, `data/*.sqlite3`, plus `*.zip` and `.DS_Store` at the root.

## 3. Architecture & file map

**`app.py` is a thin composition layer.** It defines `apply_theme()` (all inline CSS), handles the optional private-passcode gate, renders the sidebar + hero, then wires **9 flat top-level tabs** via `st.tabs([...])` + `with X_tab: render_X_tab(...)`: 🧭 Home, 🏠 Today, 📚 Lessons, ✏️ Practice, 🔁 Review, 🛠️ Projects, 🤖 AI Tutor, 📈 Progress, ⋯ More. Some tabs compose two renderers (Practice = quiz + code; Review = review + flashcards; Progress = path + dashboard); the More tab uses an `st.pills` tile switcher over Glossary / AI Certs / Prompt Lab / Notes / Deploy.

**Tab-module split:** each tab's UI lives in its own `*_tab.py` exposing `render_X_tab(...)` — `home_tab, today_tab, lesson_tab, quiz_tab, code_tab, projects_tab, prompt_tab, ai_tab, notes_tab, official_ai_tab, focus_tab, dashboard_tab, path_tab, deploy_tab, glossary_tab, review_tab, flashcards_tab`.

**Architecture rule (enforced by tests):** `*_tab.py` modules import only from leaf domain modules (`curriculum`, `glossary`, `progress`, `review`, `flashcards`, `learning_path`, `coding_gym`, `study_plan`, `ui_components`, `ui_safety`, …) — **never from `app.py`**. This keeps the split acyclic. Shared presentation renderers go in `ui_components.py`; tab-specific/state-touching renderers stay in the tab module. HTML-escape helpers (`h`, `safe_html_text`, `truncate_text`) live in `ui_safety.py` and must wrap any learner text rendered into raw HTML.

**Leaf logic modules (logic split from its renderer):** `review.py`, `flashcards.py` (Leitner spaced repetition), `home.py`, `learning_path.py` (skill outcomes, milestones, graduation), `coding_gym.py`/`smooth_workout.py` (workout blocks), `study_plan.py` (`DAILY_PLAN`, missions), `focus_coach.py`, `projects.py`, `gamification.py` (XP/levels), `daily_coach.py`, `experience.py`.

**Central data dicts/lists (edit these for content, not `app.py`):**
- `curriculum.LESSONS` — 24 `Lesson` dataclasses (`Lesson`, `QuizQuestion`, `CodingChallenge` at top of `curriculum.py`; helper `get_lesson_by_id`).
- `glossary.GLOSSARY` — term→definition dict, lowercase keys; `define()` (case-insensitive), `vocab_for_terms()`.
- `lesson_extras.WORKED_EXAMPLES` + `COMMON_MISTAKES` — keyed by lesson id.
- `learning_path.SKILL_OUTCOMES` / `MILESTONES`.
- `study_plan.DAILY_PLAN` — the 30-day mission plan.
- `official_ai_resources.py` — external AI courses/certs catalog.

Support modules: `private_access.py` (passcode gate), `product_export.py` (backup zip / transcript / certificate / import unwrap), `progress_store.py` (SQLite snapshot), `standalone_check.py` (deploy readiness).

## 4. Data model (progress schema & persistence)

The persisted schema is defined in **`progress.py`** by two functions that must stay in lockstep:
- `default_progress(lesson_ids, profile_name)` — the canonical empty schema.
- `normalize_progress_data(raw, lesson_ids, profile_name)` — merges saved/imported data over the defaults, coerces types, and drops lesson IDs no longer in the curriculum.

**Top-level keys:** `created_at`, `updated_at`, `profile_name`, `completed_lessons` (list), `quiz_scores` (dict: lesson id → {score,total,percent,taken_at}), `notes` (dict), `prompt_scores` (list), `official_ai_status`/`official_ai_notes` (dicts), `daily_missions`/`daily_checklists` (dicts), `daily_reflections` (list), `lesson_completed_at` (dict), `study_streak`/`longest_streak`/`last_session_date`, `focus_preferences` (dict), `learning_contract` (dict), `focus_checkins` (list), `parking_lot` (list), `project_milestones` (dict), `gym_sessions` (dict by day), `mistake_cards` (list), `flashcards` (dict: term → {box,due,seen,correct,…}), `review_history` (list).

**Persistence is dual-store.** `save_progress(data, path)` writes pretty JSON to `data/progress_<slug>.json` AND (unless `APP_DISABLE_SQLITE_BACKUP`) a SQLite snapshot via `progress_store`. `load_progress` reads the JSON first, falls back to the SQLite snapshot, then always runs `normalize_progress_data`. Each profile gets its own file via `progress_path_for_profile`. `DATA_DIR` defaults to `data/` (`APP_DATA_DIR`). Streaks/dates use `APP_TIMEZONE` (default `America/Los_Angeles`) via `local_today()`.

**Mutators** are the only sanctioned way to change progress: `mark_lesson_complete`, `record_quiz_score`, `record_review_result`, `save_note`, `record_prompt_score`, `record_official_ai_resource`, `update_study_streak`, `record_daily_mission`/`record_daily_checklist`, `record_gym_session`/`start_gym_session`/`pause_gym_session`, `add_mistake_card`/`close_mistake_card`, `save_focus_preferences`, `record_focus_checkin`, `add_parking_lot_item`/`close_parking_lot_item`, `record_project_milestone`.

> **To persist a NEW progress field, add the key in THREE places:** (1) `default_progress`, (2) the coercion in `normalize_progress_data`, (3) a `record_*` mutator. Missing (1) or (2) means it silently won't survive save/load or import-normalize.

## 5. THE constraint — the `-I -S` stdlib-only auto-grader

`code_runner.run_python_with_tests` runs learner/sample code with `subprocess.run([sys.executable, "-I", "-S", script])` — **isolated mode, no site-packages, 4s timeout, temp dir.** `tests/test_curriculum.py::test_all_sample_solutions_pass_their_lesson_tests` runs every lesson's `challenge.sample_solution` against its `challenge.tests` through that exact runner and asserts a clean exit.

**Therefore every `CodingChallenge` (`sample_solution` AND `tests`) must be solvable with the standard library only** — no `pandas`, `numpy`, `requests`, etc. If a lesson *teaches* a third-party library, teach it in the explanation/worked example, but make the auto-graded challenge pure-Python that mirrors the concept (e.g. group-and-average a list of dicts by hand instead of `df.groupby`). Always run the new `sample_solution` against its `tests` before shipping.

### How to add a lesson correctly
1. Append a `Lesson(...)` to `curriculum.LESSONS` with a new id like `25-topic` (numeric prefix orders lessons; keep sequential).
2. For every new `key_terms` entry, add a lowercase definition in `glossary.GLOSSARY` — `tests/test_glossary.py` fails otherwise.
3. Add `WORKED_EXAMPLES[id]` and `COMMON_MISTAKES[id]` in `lesson_extras.py` — `tests/test_lesson_extras.py` enforces both (worked example must contain a code block).
4. Each `QuizQuestion.answer` must be one of its `options` — `tests/test_curriculum.py` checks this.
5. Ensure `challenge.sample_solution` passes `challenge.tests` under `-I -S` (stdlib only).
6. Optionally map the lesson into `SKILL_OUTCOMES`/`MILESTONES` in `learning_path.py`.
7. Bump the count in `README.md`. Lesson count is data-driven everywhere (`len(LESSONS)`), so no other code change is needed.

## 6. Design system (warm "sunset" theme)

**Two layers:**
1. **Streamlit theme** in TWO `config.toml` files that must stay in sync: the **repo root** `Coding/.streamlit/config.toml` (Streamlit Cloud runs from the repo root and reads this) and `ai_code_tutor_app/.streamlit/config.toml` (local runs from the app dir). Both set `base="light"`, `primaryColor=#F97316`, `backgroundColor=#FAF5EF`, `secondaryBackgroundColor=#FFFDF9`, `textColor=#2D2A26`. **Change both files together.**
2. **All custom CSS** lives in `app.py` `apply_theme(low_stimulation=False)` — one large `st.markdown(<style>…)` block. It injects an extra low-stimulation override when the learner enables `low_stimulation_mode` (from `focus_preferences`).

**Tokens:** cream canvas `#FAF5EF`, warm-white surfaces `#FFFDF9`, espresso text `#2D2A26`, orange accent `#F97316` (hover `#EA580C`), amber→orange→pink gradient `linear-gradient(#F59E0B, #F97316, #EC4899)` on the hero headline, progress bars, and primary buttons. Font is Apple system fonts (`-apple-system, "SF Pro"…`).

**Interaction convention (important UX rule):** the app **deliberately uses no `st.selectbox` dropdowns and no `st.expander`.** Pickers are `st.pills` tile switchers (sidebar tools, More-tab section switcher, pace/energy/focus/status selectors, Code Lab tests/hints/solution); reveal/hide is `st.toggle` (e.g. "🧘 Focus coach", "Where is my progress saved?"). Top nav is a flat row of `st.tabs` styled as an iOS segmented control. Lesson selection is a clickable list in `lesson_tab.py`. Both `st.pills` usages keep a `st.radio` fallback guarded by `hasattr(st, "pills")`. **Don't reintroduce dropdowns or expanders.**

## 7. Conventions & guardrails

- **Acyclic imports:** `*_tab.py` import only leaf modules, never `app.py`. `tests/test_app_static_integrity.py` AST-walks app.py + ui_components.py + every `*_tab.py` to assert required imports exist, names aren't duplicated, every flat-nav block (`with home_tab:` … `with more_tab:`) is present, and every `render_X_tab(` call is wired. Rename a renderer and this test guides you.
- **AI is optional:** the app must work with no `OPENAI_API_KEY`. `ai_is_configured()` gates AI buttons (they disable, not error). The client uses the OpenAI **Responses API** (`client.responses.create`); default model from `OPENAI_MODEL` (verify it's a valid id for the account).
- **Code runner off in public deploys** (`ALLOW_CODE_RUNNER` unset → `code_runner_enabled()` False). Local-study only; not a secure sandbox.
- **Completeness/structure tests are the safety net (~150 total):** every key term defined (`test_glossary.py`), every lesson has a worked example + common mistake (`test_lesson_extras.py`), every sample_solution passes under `-I -S` and every quiz answer is valid (`test_curriculum.py`), flat-nav wiring + HTML escaping + import hygiene (`test_app_static_integrity.py`), plus runtime smoke and a new-user journey test.
- **HTML safety:** wrap learner-entered text in `h`/`safe_html_text(truncate_text(...))` before injecting into raw HTML.
- **Private mode:** `APP_PRIVATE_MODE=true` + `APP_PRIVATE_PASSCODE` puts an app-wide passcode gate in front (`private_access.py`); leave blank for local use.

## 8. Known limitations & suggested next steps

**Known limitations:**
- **No real auth; shared-filesystem storage.** "Profiles" are separate JSON files keyed by a free-text sidebar name. On Streamlit Cloud all visitors share one container filesystem and any visitor can switch profiles. The passcode gate is app-wide, not per-user.
- **Ephemeral persistence on Streamlit Cloud:** progress JSON/SQLite live on the container disk, wiped on redeploy/restart. The export/import + backup-zip flow (`product_export.py`, in the Progress tab) is the only durable path — back up periodically.
- **The in-app code runner is disabled in production** and is explicitly not a secure sandbox; hosted learners self-check challenges against the sample solution rather than executing them.
- **Repo layout oddity:** the app is a subdirectory of the larger `Coding` repo, so the Streamlit theme config is duplicated at the repo root and the app dir.

**Suggested next steps:**
1. If multi-user is ever a goal, replace file/SQLite-on-container storage with a hosted DB + per-user auth (load/save is centralized in `progress.py`, so the change is contained).
2. ~~Wire `.github/workflows/tests.yml` to run tests on PRs~~ — done: the workflow now lives at the **repo root** (GitHub only runs root workflows) with `working-directory: ai_code_tutor_app`, so `pytest -q` runs on every push/PR before auto-deploy.
3. Add a tiny test asserting the two `config.toml` `[theme]` blocks match, so the root/nested copies can't drift.
4. A lesson editor for adding curriculum items without code edits; custom quizzes from missed questions; completion analytics.
5. A true sandboxed code runner so hosted learners can actually execute lesson tests.
