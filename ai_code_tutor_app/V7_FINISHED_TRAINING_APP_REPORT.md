# v7 Finished Training App Report

Date: 2026-05-28

## Goal

Deliver a private, polished training app that a brand-new learner can use for fun in about 30 minutes a day, with ADHD-friendly structure and project/capstone momentum.

## Product upgrades

- Added `focus_coach.py` with ADHD-friendly session blocks, rescue mode, body-double scripts, design principles, and focus scoring.
- Added a **Focus Coach** tab to the Streamlit app.
- Added parking-lot capture for distracting thoughts.
- Added focus preferences: default session length, ADHD-friendly mode, low-stimulation mode, break reminders, and reward style.
- Added focus check-ins to progress storage.
- Added `projects.py` with five project tracks and capstone checkpoints.
- Added a **Projects** tab with project selection, milestone status, proof notes, progress bars, and a recommended project.
- Expanded XP and badges to include focus check-ins and project milestones.
- Added Xcode/iOS Simulator testing documentation and a simple SwiftUI `WKWebView` wrapper.
- Added documentation for ADHD-friendly design decisions.

## QA results

```text
python -m compileall -q .
completed successfully

python -m pytest -q
47 passed
```

## Manual testing note

This packaging container can run Python tests and compile checks, but it does not have a live Streamlit browser session. Use `XCODE_IOS_TESTING.md` or run `streamlit run app.py` locally for visual/mobile testing.

## Recommended next production upgrades

1. Add user authentication before public sharing.
2. Replace JSON progress files with SQLite, Supabase, Postgres, or Firebase.
3. Add Streamlit AppTest tests in a full dev environment with Streamlit installed.
4. Add a real sandbox before enabling code execution for anyone other than yourself.
5. Add optional calendar reminders or notification integrations for the 30-minute habit.
