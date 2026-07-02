---
name: improve-tutor
description: >
  Project playbook for the AI Code Tutor Streamlit app in ai_code_tutor_app. Use
  this skill whenever working on that app — building features, fixing bugs,
  improving layout/UX, or adding lessons, quizzes, vocabulary, flashcards, or
  review modes. It front-loads the codebase map, conventions, the locked-down
  auto-grader constraint, and the verify-and-ship workflow so you do NOT need to
  re-explore the repo (re-exploration is the main thing that wastes credits).
  Trigger on "improve the tutor", "add a lesson", "fix the app", "work on the
  code tutor", "ai_code_tutor_app", or any edit to files under that directory.
---

# AI Code Tutor — project playbook

A Streamlit study app: a daily "coding gym" plus 24 Python lessons, quizzes,
coding challenges, an AI tutor, a glossary, and a spaced-repetition review tab.
Root: `/Users/collin.brown/Documents/GitHub/Coding/ai_code_tutor_app`.
Deployed on Streamlit Cloud from GitHub `Puplogan2346/Coding` (main file
`ai_code_tutor_app/app.py`); pushing to `main` auto-redeploys.

## Spend credits wisely (read this first)

The point of this playbook is that **this file is the map — trust it instead of
re-scanning the repo.** Re-discovering structure from scratch is what burns
tokens. So:

- **Don't broadly explore.** Use the file map below to jump straight to the one
  or two files a task touches, and read only those.
- **Prefer central data files over editing `app.py` or `curriculum.py`.** Most
  content changes are a single dict/list entry (see "Common tasks").
- **Make targeted `Edit`s,** not rewrites. Don't re-read a file right after
  editing it.
- **Verify once at the end** (see "Verify"), not after every micro-edit.
- **One commit per task.** Don't commit half-steps.
- If something here looks stale (a function/file was renamed), fix the playbook
  in the same change so it stays trustworthy.

## File map

| File | What it holds |
|------|---------------|
| `app.py` | Thin composition layer. Sidebar + 9 flat top-level `st.tabs` (Home, Today, Lessons, Practice, Review, Projects, AI Tutor, Progress, More), each wiring `with X_tab: render_X_tab(...)`. Edit only for navigation/layout/wiring. |
| `curriculum.py` | `LESSONS` (the 24 `Lesson` dataclasses: objectives, explanation, `key_terms`, `quiz`, `challenge`, `prompt_skill`) + `Lesson`, `QuizQuestion`, `CodingChallenge`, `get_lesson_by_id`. |
| `glossary.py` | `GLOSSARY` dict (term→definition, lowercase keys) + `define()`, `vocab_for_terms()`. One definition per term, reused everywhere. |
| `lesson_extras.py` | `WORKED_EXAMPLES` + `COMMON_MISTAKES` dicts keyed by lesson id, + `worked_example()`, `common_mistake()`. |
| `learning_path.py` | `first_incomplete_lesson_id`, `SKILL_OUTCOMES` (skill map), `MILESTONES`, graduation logic, `learning_outcomes()`. |
| `progress.py` | Progress schema: `default_progress`, `normalize_progress_data` (merges saved data over defaults — new keys persist if added to BOTH), `save_progress`, `load_progress`, and `record_*` mutators (incl. `record_build_step`, `save_build_code`). SQLite + JSON backup. |
| `projects.py` / `project_builds.py` / `build_checks.py` | Project tracks + milestones / guided Build Studio content (`PROJECT_BUILDS`: 5-step cumulative builds, step ids == milestone ids; plus the `design_your_own` free-build track with `DIY_INGREDIENTS`) / AST-based `StepCheck` structure checks (no execution — safe on public deploys). New builds must pass `tests/test_project_builds.py` (cumulative sample solutions vs. checks + tests). |
| `review.py` / `review_tab.py` | Progress-based recommendations + mixed quiz (logic / UI). |
| `flashcards.py` / `flashcards_tab.py` | Leitner spaced-repetition over glossary terms (logic / UI). |
| `*_tab.py` | One per tab: `today, lesson, quiz, code, projects, prompt, ai, notes, official_ai, focus, dashboard, path, deploy, glossary, review, flashcards`. Each exposes `render_X_tab(...)`. |
| `ui_components.py` | Shared presentation renderers. `ui_safety.py` | HTML escape helpers (`h`, `safe_html_text`). |
| `code_runner.py` | Runs challenge tests in a subprocess with `python -I -S` (see constraint below). |
| `tests/` | pytest suite (currently ~150 tests). |

**Architecture rule:** `*_tab.py` modules import only from leaf domain modules
(`curriculum`, `glossary`, `progress`, `review`, …), never from `app.py`. This
keeps the split acyclic. Shared renderers go in `ui_components.py`; tab-specific
or state-touching renderers stay in the tab module.

## The auto-grader constraint (most common footgun)

`code_runner.run_python_with_tests` executes learner code with
`python -I -S` — **isolated mode with no site-packages.** A test in
`tests/test_curriculum.py` runs every lesson's `challenge.sample_solution`
against its `challenge.tests` and asserts it passes.

Therefore: **every `CodingChallenge` must be solvable with the standard library
only.** No `pandas`, `requests`, `numpy`, etc. in `sample_solution` or `tests`.
If a lesson teaches a third-party library (e.g. pandas, requests), teach it in
the `explanation`/worked example, but make the auto-graded challenge pure-Python
that mirrors the concept (e.g. group-and-average a list of dicts by hand instead
of `df.groupby`). Always confirm a new `sample_solution` actually passes its
`tests` before shipping.

## Common tasks (recipes)

**Add a lesson** — append a `Lesson(...)` to `LESSONS` in `curriculum.py`
(id like `22-topic`). Then, keyed by that id, add: a definition in `GLOSSARY` for
each new `key_terms` entry, a `WORKED_EXAMPLES` + `COMMON_MISTAKES` entry, and
optionally a `SKILL_OUTCOMES` entry in `learning_path.py`. Tests enforce that
every term is defined and every lesson has a worked example + mistake. Quiz
answers must be one of their `options`; the sample_solution must pass its tests
(stdlib only). Bump the README lesson table count.

**Add/fix vocabulary** — edit `GLOSSARY` only (lowercase key). It feeds both the
per-lesson Vocabulary section and the searchable Glossary page automatically.

**Improve layout / navigation** — edit `app.py` (tab list + `with X_tab:`
blocks) and/or the specific `render_X_tab` in its module. Keep the flat
single-row tab structure; don't reintroduce dropdowns for navigation (the lesson
picker is a clickable list in `lesson_tab.py`).

**Persist new progress data** — add the key to BOTH `default_progress` and the
normalization in `normalize_progress_data` (`progress.py`), then a `record_*`
mutator. This is what makes it survive save/load.

**Add a new tab** — create `X_tab.py` with `render_X_tab(...)`, add it to the
`st.tabs([...])` list and a `with X_tab:` block in `app.py`, importing only leaf
modules.

## Verify (before shipping)

1. `./.venv/bin/python -m pytest -q` — full suite must stay green. The project
   venv at `ai_code_tutor_app/.venv` runs Python 3.12 + the pinned streamlit
   (system `python3` is 3.9 with an old streamlit — don't test with it; the
   3.12 interpreter lives at `~/.local/python/cpython-3.12.13`). For a quick
   check while iterating, run just the relevant file, e.g.
   `./.venv/bin/python -m pytest tests/test_curriculum.py -q`, then the full suite once.
2. Real-runtime render check — catches Streamlit errors the unit tests miss:
   ```python
   from streamlit.testing.v1 import AppTest
   at = AppTest.from_file('app.py', default_timeout=30)
   at.session_state['active_profile']='guest'; at.session_state['profile_name']='guest'
   at.run()
   assert len(at.exception) == 0
   ```
   Seed `selected_lesson_id` to test a specific lesson.
3. **Click/interaction tests:** a full-app rerun in `AppTest` crashes on an
   unrelated `st.pills` serialization quirk (in `today_tab`). To test a button
   that triggers `st.rerun()`, write a tiny throwaway probe script that renders
   just the one `render_X_tab(...)` with mock data, `AppTest.from_file` it, and
   `.click().run()`. Pass a real `pathlib.Path` (not a str) anywhere a
   `progress_path` is expected. Delete the probe after.

## Ship

Run all git from the repo root (`/Users/collin.brown/Documents/GitHub/Coding`).
`origin` is SSH (`git@github.com:Puplogan2346/Coding.git`) — SSH key auth works;
HTTPS has no cached token.

```bash
git add ai_code_tutor_app/<changed files>
git commit -m "<concise message>

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git pull --rebase origin main   # someone may have pushed (e.g. devcontainer)
git push origin main            # Streamlit Cloud auto-redeploys
```

Never commit secrets: `.gitignore` already excludes `.env`,
`.streamlit/secrets.toml`, progress JSON, and `*.sqlite3`. The root `.gitignore`
excludes `*.zip` and `.DS_Store`. Keep the GitHub repo private; supply
`OPENAI_API_KEY` via the Streamlit Secrets panel, never in code.

## Guardrails

- The AI tutor is optional — the app must keep working with no `OPENAI_API_KEY`
  (AI buttons just disable). Don't make features hard-depend on it.
- The code runner is off in public deploys (`ALLOW_CODE_RUNNER` unset) — never
  rely on it for core flows.
- Some tests assert completeness (every term defined, every lesson has extras)
  and structure (flat-nav wiring in `tests/test_app_static_integrity.py`). If
  you add lessons/terms/tabs, expect those tests to guide you.
