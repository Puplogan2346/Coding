# AI Code Tutor

A private, deploy-ready Streamlit training app that feels like a **daily coding gym**: open the app, press **Start Today**, complete one 10/30/45-minute workout, save a proof card, and come back tomorrow.

## Getting started (your first lesson)

1. Open the app and go to the **📚 Lessons** tab.
2. Press **▶ Start Lesson 1 — Python mindset: commands, output, and mistakes**.
3. Read the lesson, take the quiz in the **✏️ Practice** tab, and try the Code Lab challenge.
4. Come back tomorrow and press **Start Today** on the **🏠 Today** tab for your 30-minute session.

No API key is required — the AI tutor is optional. Add `OPENAI_API_KEY` (as a Streamlit secret or env var) only if you want live AI hints.

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

## Navigation

A single, flat row of nine tabs (no nested menus, no lesson dropdown):

- **🏡 Home** — the command-center dashboard: quick actions, an auto-built to-do list, current projects, open mistake cards ("bugs"), and your next learning resource.
- **🏠 Today** — the daily coding gym (Start Today → one rep at a time → save proof). Focus Coach lives here in an expander.
- **📚 Lessons** — a clickable list of all 24 lessons with a "Start Lesson 1 / Continue" button; the open lesson's content shows below.
- **✏️ Practice** — the current lesson's quiz and Code Lab challenge.
- **🔁 Review** — progress-based recommendations, a mixed review quiz, and spaced-repetition flashcards over the glossary.
- **🛠️ Projects** — project tracks and capstone checkpoints.
- **🤖 AI Tutor** — optional AI chat about the current lesson.
- **📈 Progress** — learning path, milestones, graduation checklist, and your dashboard.
- **⋯ More** — AI certifications, Prompt Lab, Notes, and Deploy tools.

### Official AI Lessons & Certifications

The app now includes an **AI Certs** tab that tracks official learning resources from Anthropic/Claude, Gumloop, OpenAI, Google Cloud/Gemini, Microsoft/Azure AI, AWS, Hugging Face, and NVIDIA. It links to the official provider pages, lets each learner save status and private notes, and separates course/certification tracking from the core Python curriculum. See `OFFICIAL_AI_RESOURCES.md` for the curated list and maintenance notes.



## V17: Smooth Daily Gym Focus Mode

This build makes the daily habit loop feel less like a dashboard and more like a guided coding gym. The Today tab now shows a single **Focus Mode** card with the current rep, one clear action, and a save button. The full checklist is still available, but hidden as a backup.

New in v17:

- **Focus Mode: one rep at a time** for the Today tab.
- **Mark this rep done & save** so progress persists after each block.
- **Daily-use smoothness check** inside the Today tab.
- **Time changed since you paused?** converter for resizing a saved in-progress workout.
- Focus-mode tests for next-rep logic, resume safety, and daily-use smoothness checks.

## V16: Complete Private Learning Product Layer

This build turns the app into a clearer end-to-end learning product instead of only a daily workout dashboard. The main goal is now visible in the app: finish the 30-day daily coding gym, complete the Python basics lessons, save proof cards, pass quizzes, build project checkpoints, and finish a capstone proof note.

New in v16:

- **Private access gate** for hosted personal use with `APP_PRIVATE_PASSCODE`.
- **SQLite progress snapshot backup** alongside the readable JSON progress file.
- **Private backup pack** with progress JSON, transcript, certificate preview, and README.
- **Certificate and transcript downloads** from the Path tab.
- **Path tab** with milestone map from Python starting line to capstone graduation.
- **Graduation checklist** showing exactly what counts as learning proof.
- **Skill map** for Python mindset, variables/types, control flow, loops, functions, data structures, debugging/tests, JSON/API thinking, objects, AI prompting, and project building.
- **Current milestone card** inside Today so each workout connects to a bigger learning goal.
- **Standalone readiness check** in Deploy so the app can live outside ChatGPT more safely.
- New automated tests for private access, SQLite backup storage, export artifacts, daily loop resume, milestone progress, graduation readiness, and standalone deployment checks.

The intended daily habit is still simple: open the app, press **Start Today**, finish one block at a time, save proof, and stop.

## What is included

- New **Daily Coding Gym** Today tab with a single default path: Start Today → warm-up → lesson → coding reps → AI/prompt drill → proof card
- **Path** tab with six milestones, a skill map, graduation checklist, and end-of-app learning outcomes
- 10/30/45 minute workout modes: rescue mode for low-energy days, daily mode for the normal habit, and deep-dive mode for project energy
- Focus Mode current-rep card, one-screen checklist backup, next-rep coach card, proof-card closeout, mistake notebook, adaptive review queue, and recent gym history
- Persistent Start Today/resume behavior, so a refresh does not erase an in-progress workout
- Explicit **Stop & save for later** and **Save current draft** controls that saves pace, selected lesson, checklist, proof note, and next-review note
- Today-tab **Remember this pace** control so your preferred 10/30/45-minute workout length is saved without visiting settings
- Time-based lesson switching: 10-minute sessions suggest review/tiny steps, 30-minute sessions suggest the normal plan, and 45-minute sessions add deeper/stretched options
- Safer proof-card completion: completed workouts require all visible blocks plus one proof sentence
- New **Focus Coach** tab with ADHD-friendly rescue mode, parking lot, body-double scripts, and focus check-ins
- New **Projects** tab with tiny project tracks and capstone milestones
- Daily missions with warm-up, learning, practice, reflection, review queue, and fun challenge
- Streaks, XP levels, badge shelf, daily-gym badges, mistake-card XP, focus check-ins, project XP, and end-of-session reflections
- 12 beginner-to-intermediate Python lessons
- Quizzes with saved scores
- Coding challenges with starter code, hints, tests, and sample solutions
- Prompt Lab with a scoring rubric
- Optional OpenAI-powered AI Tutor
- Learner profiles so multiple people can use separate progress files
- Progress export/import
- New-user habit loop designed for short daily sessions instead of cramming
- Xcode/iPhone Simulator testing guide plus a simple SwiftUI WebView wrapper
- Streamlit Community Cloud entrypoint
- Dockerfile and docker-compose setup
- Render-style deployment blueprint
- GitHub Actions test workflow
- Private GitHub setup guide
- New-user journey smoke test and report
- Official AI lessons/certifications tracker with private notes
- Recommended next AI-resource card for Gumloop, Claude/Anthropic, OpenAI, and later credential paths
- Pytest coverage for curriculum, progress, prompt scoring, code runner behavior, app static checks, and official AI resource tracking
- Bug-fix and QA report in `BUG_FIXES_AND_IMPROVEMENTS.md`
- V8 finished daily-coach QA report in `V8_FINISHED_DAILY_COACH_QA_REPORT.md`
- V9 UX/UI optimization report in `V9_UX_OPTIMIZATION_REPORT.md`
- V10 coach-flow optimization report in `V10_UX_EXPERIENCE_OPTIMIZATION_REPORT.md`
- V11 daily-coding-gym optimization report in `V11_DAILY_CODING_GYM_REPORT.md`
- V12 reliability and daily-use optimization report in `V12_DAILY_USE_QA_REPORT.md`
- V13 pause/resume, preferred-time, and time-based lesson switching report in `V13_PAUSE_RESUME_TIME_QA_REPORT.md`
- V14 stop/resume and time-fit QA report in `V14_STOP_RESUME_TIME_FIT_QA_REPORT.md`
- V15 learning app and standalone QA report in `V15_LEARNING_APP_QA_REPORT.md`
- V16 complete private product report in `V16_PRIVATE_PRODUCT_COMPLETION_REPORT.md`
- V17 smooth daily-gym QA report in `V17_SMOOTH_DAILY_GYM_QA_REPORT.md`

## Keep private while building

Use a private GitHub repository while building. See `PRIVATE_GITHUB_SETUP.md` and `PRIVATE_PRODUCT_GUIDE.md` for the exact setup commands. The important rule: never commit `.env`, `.streamlit/secrets.toml`, API keys, passcodes, or learner progress files. For any hosted link, set `APP_PRIVATE_MODE=true` and `APP_PRIVATE_PASSCODE` as a platform secret.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Enable the AI Tutor

The app works without AI. To enable live AI help, set an API key.

Environment variable option:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_MODEL="gpt-5.5"
streamlit run app.py
```

Streamlit secrets option:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml` and add your real key.

Never commit `.streamlit/secrets.toml`, `.env`, or any API key.

## Public sharing safety

The included code runner is useful for your own computer, but it is not a secure sandbox for public users.

For public deployment, keep this setting:

```bash
ALLOW_CODE_RUNNER=false
```

To enable local lesson tests only on your own machine:

```bash
ALLOW_CODE_RUNNER=true streamlit run app.py
```

## Test in Xcode / iPhone Simulator

This is a Streamlit web app, so Xcode is optional. To preview the mobile experience, run the app locally and open it in iOS Simulator Safari. The package also includes a simple SwiftUI WebView wrapper in `ios_wrapper/`. See `XCODE_IOS_TESTING.md`.

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then open `http://localhost:8501` in iOS Simulator Safari.

## Run tests

```bash
pytest -q
```

## Run with Docker

```bash
cp .env.example .env
# edit .env if you want AI features

docker build -t ai-code-tutor .
docker run -p 8501:8501 --env-file .env ai-code-tutor
```

Or use Docker Compose:

```bash
docker compose up --build
```

Then open `http://localhost:8501`.

## Project structure

```text
app.py                         Main Streamlit app
streamlit_app.py               Streamlit Community Cloud wrapper
curriculum.py                  Lessons, quizzes, coding challenges
ai_tutor.py                    OpenAI API helper functions
prompt_lab.py                  Prompt scoring rubric
study_plan.py                  30-day daily mission plan and review queue
focus_coach.py                 ADHD-friendly focus sessions and rescue mode
daily_coach.py                 One-screen daily coach checklist and rescue-mode nudges
coding_gym.py                  Daily coding-gym blocks, proof cards, review queue, and mistake-card helpers
learning_path.py                Milestones, skill map, graduation readiness, and learning outcomes
standalone_check.py             Standalone readiness checks for local/private deployment
projects.py                    Project tracks and capstone checkpoints
gamification.py                XP, levels, badges, level-progress helpers
experience.py                  UX helper logic for session pace, next action cards, timeline, and coaching copy
ui_safety.py                   HTML escaping and safe text previews for raw HTML cards
official_ai_resources.py       Official AI lessons/certifications catalog
progress.py                    Learner profile, streak, mission, and progress storage
progress_store.py              SQLite backup snapshot store
private_access.py              Optional private access gate helpers
product_export.py              Transcript, certificate, and backup-pack exports
code_runner.py                 Optional local code runner
requirements.txt               Runtime and test dependencies
run_app.sh                     One-command local launcher for macOS/Linux
run_app_windows.ps1            One-command local launcher for Windows PowerShell
pyproject.toml                 Project metadata and pytest config
Dockerfile                     Container deployment
render.yaml                    Render-style deployment blueprint
docker-compose.yml             Local container workflow
README_DEPLOY.md               Step-by-step sharing/deployment guide
PRIVATE_GITHUB_SETUP.md        Private repo setup and safety checklist
NEW_USER_TEST_REPORT.md        Fresh learner smoke-test notes
OFFICIAL_AI_RESOURCES.md       Official AI resource tracker notes
NEW_USER_OFFICIAL_AI_TEST_REPORT.md Official AI tracker smoke test
BUG_FIXES_AND_IMPROVEMENTS.md v5 bug-fix and QA notes
V6_OPTIMIZATION_REPORT.md      Finished-app optimization and QA notes
V7_FINISHED_TRAINING_APP_REPORT.md Finished app, focus, project, and Xcode QA notes
V8_FINISHED_DAILY_COACH_QA_REPORT.md Final daily-coach hardening and QA notes
V9_UX_OPTIMIZATION_REPORT.md   UX/UI polish, new-user flow, and QA notes
V11_DAILY_CODING_GYM_REPORT.md Daily gym conversion, efficiency notes, and QA results
V13_PAUSE_RESUME_TIME_QA_REPORT.md Pause/resume, preferred workout length, time-based lesson selector, and QA notes
THIRTY_DAY_TRAINING_PLAN.md    Human-readable daily learning plan
ADHD_FRIENDLY_DESIGN.md        ADHD-friendly UX/design notes
XCODE_IOS_TESTING.md           iPhone Simulator and SwiftUI wrapper guide
LEARNING_OUTCOMES.md            Course outcomes, milestones, and graduation evidence
STANDALONE_APP_CHECKLIST.md     Local/private deployment readiness checklist
ios_wrapper/                   Optional SwiftUI WKWebView wrapper files
.github/workflows/tests.yml    CI tests for GitHub
.streamlit/config.toml         Streamlit runtime config
.streamlit/secrets.toml.example Example secrets file
```

## Suggested next upgrades

1. Add real user accounts if anyone besides you will use it.
2. Move from local JSON/SQLite snapshots to a hosted database for multi-device sync.
3. Replace the simple review queue with real spaced-repetition cards.
4. Generate custom quizzes from missed questions.
5. Add a lesson editor for creating new curriculum items.
6. Add a true sandboxed code runner for public deployments.
7. Add analytics for lesson completion and quiz improvement.

## V14 daily-use persistence

The Today tab is designed around a daily coding-gym loop. Before pressing **Start Today**, choose how much time you have: **10 min rescue**, **30 min daily**, or **45 min deep dive**. The app changes the suggested lesson based on that time window.

Use **Save current draft** or **Stop & save for later** to pause. The app saves the selected time, selected lesson, checked blocks, proof draft, and next-review note so you can resume later from the same spot.

See `V14_STOP_RESUME_TIME_QA_REPORT.md` for the focused QA notes.