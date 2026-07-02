# Roadmap — ready-to-execute improvement specs

Each spec below is written so a fresh Claude Code session can implement it
**without exploring the repo**. Rules for keeping credits low:

1. **Read the playbook first**: `.claude/skills/improve-tutor/SKILL.md` (file
   map, conventions, the stdlib-only auto-grader constraint, verify commands).
   Trust it — do not re-scan the repo.
2. Open **only the files named in the spec**. Make targeted edits, not rewrites.
3. Verify **once** at the end: `./.venv/bin/python -m pytest -q` (160+ tests
   must stay green) plus the AppTest render snippet from the playbook.
4. One commit per spec; push to `main` (auto-deploys). CI now runs the suite
   on every push (`.github/workflows/tests.yml` at the repo root).

Current state (2026-07-02): 24 lessons, quizzes, daily gym, review/flashcards,
Build Studio with 4 guided builds + a Design Your Own track, milestones and
graduation tracking, optional AI tutor. streamlit==1.58.0, Python 3.10+.

---

## Tier 1 — quick wins (each ≈ one short session)

### 1.1 Home tab: surface the Build Studio next step
**Why:** Home's to-do list points at the recommended project's next *milestone*
but not the Build Studio step, so "go build" isn't one click from Home.
**Files:** `home.py` (logic), `tests/test_home.py`.
**How:** In `build_todo_items` (home.py, ~line 43) the recommended project item
already exists. Enhance it: if `project_builds.build_for_project(project.id)`
returns a build, label it with the next unpassed build step instead
(`next_build_step_index` + `steps[i].title`), e.g.
`"Quiz Scorekeeper — Build step 2: Write the score function"`. Same for
`project_rows` (~line 60): add a `build_percent` field via
`build_completion_percent` when a build exists. Import only from
`project_builds` (leaf module — keeps the acyclic rule).
**Tests:** extend `tests/test_home.py`: with empty progress, the recommended
item mentions the first build step; after `record_build_step(...)` it advances.

### 1.2 Build Studio badges
**Why:** XP already flows (build steps auto-complete milestones and
`calculate_xp` counts `30 * completed_project_milestones_count`), but no badge
celebrates building.
**Files:** `gamification.py` (the `Badge(...)` list, ~line 38, and the function
that evaluates earned badges), `tests/test_gamification_levels.py`.
**How:** Add two badges following the existing dataclass pattern:
`Badge("first_build_step", "First Brick", ...)` — any passed step in
`progress_data["project_builds"]`; `Badge("shipped_program", "Shipped It", ...)`
— any project with **all** its build steps passed (compare against
`project_builds.PROJECT_BUILDS[pid].steps`). Wire the two conditions where the
other badges are computed.
**Tests:** empty progress earns neither; `record_build_step` for one step earns
the first; recording all steps of `quiz_scorekeeper` earns both.

### 1.3 Theme-config drift test
**Why:** `.streamlit/config.toml` is duplicated at the repo root for Streamlit
Cloud; the copies can silently drift (ONBOARDING known-limitation #4).
**Files:** new `tests/test_theme_config.py`.
**How:** Parse both files with `tomllib` and assert the `[theme]` tables are
equal. Repo root is `Path(__file__).resolve().parents[2]`.

---

## Tier 2 — one solid session each

### 2.1 New guided build: “Contact Book” (files & JSON practice)
**Why:** Only 4 guided builds; lessons 08 (files/JSON) deserve a dedicated one.
**Files:** `projects.py` (new `ProjectTrack`, id `contact_book`, exactly 5
milestones, minutes ≤ 180), `project_builds.py` (new `ProjectBuild`, step ids
**must equal** the milestone ids in order), `learning_path.py` (add id to the
`graduation_requirements` project tuple), `tests/test_project_builds.py` (add
the id to `EXPECTED_BUILD_IDS`), `README.md` (mention it).
**Constraints (enforced by tests — read them in test_project_builds.py):**
stdlib only, no `input()`, each step's `sample_solution` is the FULL cumulative
program and must pass its own `StepCheck`s and its own + all earlier steps'
assert-based `tests`; final program runs standalone. Copy the shape of
`_QUIZ_BUILD` in `project_builds.py`. Suggested steps: shape → add/find →
update/delete → save/load via `json.dumps`/`loads` with try/except → main-guard
demo + learner asserts.
**Cost tip:** author the five cumulative `sample_solution`s in one scratch file
first and run them; the pytest suite is the validator.

### 2.2 Review quiz built from missed questions
**Why:** README "next upgrades" #4; the Review tab currently mixes generic
questions; targeting actual misses closes the loop.
**Files:** `quiz_tab.py` (capture), `progress.py` (schema + mutator),
`review.py` + `review_tab.py` (consume), `tests/test_review.py`,
`tests/test_progress.py`.
**How:** (a) In `quiz_tab.py`, where answers are graded, record each missed
question as `{"lesson_id", "question", "answer", "missed_at"}` via a new
`record_missed_question` mutator. (b) Schema recipe (playbook): add
`"missed_questions": []` to BOTH `default_progress` and the list-normalizing
section of `normalize_progress_data`, cap the list (e.g. last 50). (c) In
`review.py`, prefer missed questions (looked up from `curriculum.LESSONS` by
question text) when building the mixed quiz; fall back to current behavior.
Remove a question from the list once re-answered correctly.

---

## Tier 3 — bigger bets (plan first, then implement across sessions)

### 3.1 Durable progress: hosted DB
All load/save is centralized in `progress.py` (`load_progress`/`save_progress`
+ `progress_store.py` SQLite snapshots). Swap the SQLite snapshot layer for a
hosted Postgres (e.g. Supabase/Neon) behind an env var, keeping JSON files as
the local fallback. Do NOT start by picking a vendor in-code; write the
adapter interface in `progress_store.py` first.

### 3.2 Sandboxed code runner for the public deploy
`code_runner.py` is the only entry point. A safe path: a tiny FastAPI runner
service in a locked-down container (no network, rlimits, seccomp) called over
HTTP when `CODE_RUNNER_URL` is set; keep `python -I -S` subprocess mode for
local. The Build Studio's AST checks already cover the no-runner case, so this
is additive, not blocking.

### 3.3 Lesson editor (content without code edits)
A More-tab panel that renders a form matching the `Lesson` dataclass and
emits a ready-to-paste `Lesson(...)` snippet + glossary/extras stubs (do NOT
write to curriculum.py at runtime — the file is the source of truth in git).

---

## Authoring recipes (already enforced by tests — follow, don't rediscover)

- **New lesson:** append `Lesson(...)` in `curriculum.py`; add every new
  `key_terms` entry to `GLOSSARY`; add `WORKED_EXAMPLES` + `COMMON_MISTAKES`
  entries; optionally a `SKILL_OUTCOMES` entry; bump the README lesson table.
  `sample_solution` must pass `tests` under `python -I -S` (stdlib only).
- **New progress key:** add to BOTH `default_progress` AND
  `normalize_progress_data`, plus a `record_*` mutator — else it won't survive
  save/load.
- **New tab:** `X_tab.py` exposing `render_X_tab(...)`, wired in `app.py`
  tabs list; import only leaf modules.
