# AI Code Tutor

A private, deploy-ready Streamlit app that feels like a **daily coding gym**: open it, press **Start Today**, complete one 10/30/45-minute workout, save a proof card, and come back tomorrow. It teaches a full 24-lesson Python + AI-coding curriculum with quizzes, coding challenges, spaced-repetition flashcards, projects, and an optional AI tutor.

> New engineer or returning after a break? Read **[ONBOARDING.md](ONBOARDING.md)** for the architecture, data model, the one critical constraint, and how to add a lesson.

## Getting started (your first lesson)

1. Open the app and go to the **📚 Lessons** tab.
2. Press **▶ Start Lesson 1 — Python mindset: commands, output, and mistakes**.
3. Read the lesson, take the quiz in the **✏️ Practice** tab, and try the Code Lab challenge.
4. Come back tomorrow and press **Start Today** on the **🏠 Today** tab for your 30-minute session.

No API key is required — the AI tutor is optional. Add `OPENAI_API_KEY` (as a Streamlit secret or env var) only if you want live AI hints.

## Navigation

A single flat row of nine tabs (no nested menus, no dropdowns — every picker is a tap-able tile or toggle):

- **🧭 Home** — command-center dashboard: quick actions, an auto-built to-do list, current projects, open mistake cards ("bugs"), and your next learning resource.
- **🏠 Today** — the daily coding gym (Start Today → one rep at a time → save proof). Focus Coach is a toggle here.
- **📚 Lessons** — a clickable list of all 24 lessons with a "Start Lesson 1 / Continue" button; the open lesson's content (objectives, explanation, worked example, common mistake, vocabulary) shows beside it.
- **✏️ Practice** — the current lesson's quiz and Code Lab challenge.
- **🔁 Review** — progress-based recommendations, a mixed review quiz, and spaced-repetition flashcards over the glossary.
- **🛠️ Projects** — the Build Studio: guided step-by-step builds where you write a real Python program in-app (with structure checks and a downloadable `.py`), plus capstone checkpoints.
- **🤖 AI Tutor** — optional AI chat about the current lesson.
- **📈 Progress** — learning path, milestones, graduation checklist, and the dashboard.
- **⋯ More** — a tile switcher for Glossary, AI Certs, Prompt Lab, Notes, and Deploy tools.

## The 24 lessons

| # | Lesson | Level |
|---|--------|-------|
| 1 | Python mindset: commands, output, and mistakes | Beginner |
| 2 | Variables, strings, numbers, and booleans | Beginner |
| 3 | Decisions with if, elif, and else | Beginner |
| 4 | Loops: repeat work without repeating yourself | Beginner |
| 5 | Functions: reusable steps with inputs and outputs | Beginner |
| 6 | Lists and dictionaries: storing many things | Beginner |
| 7 | Debugging and tests: prove your code works | Intermediate |
| 8 | Files, JSON, and APIs: talking to the outside world | Intermediate |
| 9 | Object-oriented basics: classes and objects | Intermediate |
| 10 | Prompt engineering for coding and learning | Intermediate |
| 11 | Mini-project: build a quiz scorer | Project |
| 12 | AI app basics with Streamlit | Project |
| 13 | Error handling: try, except, and resilient code | Intermediate |
| 14 | List comprehensions: transform data in one clean line | Intermediate |
| 15 | Data analysis with pandas: summarize real data | Project |
| 16 | Working with dates and times | Intermediate |
| 17 | Pattern matching with regular expressions | Intermediate |
| 18 | Clean code: type hints, docstrings, and refactoring | Project |
| 19 | Automated testing with pytest | Intermediate |
| 20 | Calling web APIs: requests, status codes, and JSON | Intermediate |
| 21 | Capstone: build a word-frequency text analyzer | Project |
| 22 | AI coding agents: how they plan, act, and verify | Intermediate |
| 23 | Directing AI agents: context, prompt, and model | Intermediate |
| 24 | Agentic workflows: verify, review, and ship | Project |

Each lesson has objectives, an explanation, a worked example, a "common mistake to avoid", a vocabulary section (defined in the central glossary), a 3-question quiz, and a coding challenge with hints and a sample solution.

## What's included

- **Daily Coding Gym** (Today tab): Start Today → warm-up → lesson → coding reps → AI/prompt drill → proof card, in 10/30/45-minute modes, with persistent stop/resume.
- **Spaced-repetition flashcards** (Leitner system) over the 111-term glossary, plus a progress-based mixed review quiz — all in the Review tab.
- **Home dashboard** that auto-builds a to-do list, surfaces open mistake cards, and shows project + resource status from real progress.
- **Learning path**: six milestones, a skill map, graduation checklist, certificate/transcript exports, and learning outcomes.
- **Build Studio projects**: four guided builds (Quiz Scorekeeper, JSON Habit Tracker, Prompt Coach, Text Analyzer) where you grow one real program step by step in an in-app editor — each step has lesson-linked instructions, AST-based structure checks that work even with the code runner off, hints, catch-up code, and a download of your finished `.py`. Checkpoint tracks and **streaks, XP, levels, and badges** round it out.
- **Quizzes** with saved scores; **coding challenges** with starter code, hints, tests, and sample solutions.
- **Optional OpenAI-powered AI Tutor**, **Prompt Lab** with a scoring rubric, and an **Official AI lessons/certifications tracker** (Anthropic, Gumloop, OpenAI, Google, Microsoft, AWS, Hugging Face, NVIDIA, and the Agentic Engineer courses). See `OFFICIAL_AI_RESOURCES.md`.
- **Learner profiles**, progress export/import, JSON + SQLite progress storage, and an optional private-access passcode gate.
- An **Apple-inspired warm UI**: cream canvas, white cards, iOS segmented-control tabs, tile pickers, and toggle switches (no dropdowns anywhere).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
python3 -m pytest -q
```

## Enable the AI Tutor (optional)

The app works fully without AI; AI buttons stay disabled until a key is set.

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_MODEL="gpt-4o-mini"   # or any current model
streamlit run app.py
```

Or copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your key there. **Never commit `.env`, `.streamlit/secrets.toml`, or any API key.**

## Public sharing safety

The built-in code runner is for your own machine, not a secure public sandbox. Keep it off for shared deployments (the default): `ALLOW_CODE_RUNNER` unset. To run lesson tests locally only: `ALLOW_CODE_RUNNER=true streamlit run app.py`.

## Deploy (Streamlit Community Cloud)

Deployed from GitHub `Puplogan2346/Coding` with main file `ai_code_tutor_app/app.py`; **pushing to `main` auto-redeploys**. The theme config is mirrored at the repo root (`.streamlit/config.toml`) because Streamlit Cloud reads config from the repo root. See `README_DEPLOY.md` for Docker/Render options and `ONBOARDING.md` for the full deploy flow.

## Project structure

```text
app.py                  Thin composition layer: theme + 9 flat tabs wiring render_*_tab()
streamlit_app.py        Streamlit Community Cloud entrypoint wrapper
curriculum.py           LESSONS (24 Lesson dataclasses) + Lesson/QuizQuestion/CodingChallenge
glossary.py             GLOSSARY term->definition map (feeds vocab + Glossary + flashcards)
lesson_extras.py        WORKED_EXAMPLES + COMMON_MISTAKES per lesson id
home.py / home_tab.py           Dashboard selection logic / renderer
lesson_tab.py                   Clickable lesson list + open-lesson detail
quiz_tab.py / code_tab.py       Quiz form / Code Lab (tile-switched tests/hints/solution)
review.py / review_tab.py       Progress-based recommendations + mixed quiz
flashcards.py / flashcards_tab.py   Leitner spaced-repetition logic / study UI
projects_tab.py / projects.py   Build Studio UI + project tracks and milestones
project_builds.py / build_checks.py   Guided build steps content / AST structure checks
ai_tab.py / ai_tutor.py         AI chat tab / OpenAI helper (optional)
prompt_tab.py / prompt_lab.py   Prompt Lab + scoring rubric
notes_tab.py                    Per-lesson notes
official_ai_tab.py / official_ai_resources.py   AI certs tracker + catalog
focus_tab.py / focus_coach.py   ADHD-friendly focus sessions
dashboard_tab.py                Progress dashboard (under the Progress tab)
path_tab.py / learning_path.py  Milestones, skill map, graduation readiness
deploy_tab.py / standalone_check.py   Deploy guide + readiness checks
glossary_tab.py                 Searchable full glossary (in More)
today_tab.py / coding_gym.py / smooth_workout.py / experience.py / study_plan.py   Daily gym
progress.py / progress_store.py SQLite+JSON progress storage and schema
gamification.py                 XP, levels, badges
private_access.py               Optional private-access passcode gate
product_export.py               Transcript, certificate, and backup-pack exports
code_runner.py                  Optional local code runner (python -I -S)
ui_components.py / ui_safety.py Shared renderers / HTML-escape helpers
tests/                          pytest suite (~150 tests)
.streamlit/config.toml          Warm theme + server config (mirrored at repo root)
ios_wrapper/                    Optional SwiftUI WKWebView wrapper
.github/workflows/tests.yml     CI test workflow
```

## Suggested next upgrades

1. Real user accounts + a hosted database for multi-device sync (replaces local JSON/SQLite).
2. A true sandboxed code runner so learners can run tests in shared deployments.
3. A lesson editor for adding curriculum items without code edits.
4. Custom quizzes generated from missed questions, and completion analytics.

See **[ONBOARDING.md](ONBOARDING.md)** for architecture, conventions, the stdlib-only auto-grader constraint, and a step-by-step "how to add a lesson".
