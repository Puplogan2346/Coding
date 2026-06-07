# V8 fixed daily coach QA report

## Summary

This pass fixes the app into a cleaner private MVP for an ADHD-friendly, 30-minutes-a-day Python training experience. The Today tab now centers on one daily mission and one saved checklist, while the rest of the app keeps lessons, quizzes, code practice, Prompt Lab, projects, and official AI resource tracking.

## Fixes and improvements

- Consolidated the Today tab around the `daily_coach.py` checklist instead of competing checklist paths.
- Kept the daily coach ADHD-friendly:
  - 30-minute default session
  - 10-minute low-energy rescue mode
  - next tiny action nudges
  - shame-free streak repair messages
- Added checklist persistence helpers:
  - `record_daily_checklist`
  - `daily_checklist_steps`
  - `daily_checklist_completion`
- Preserved backward compatibility with older checklist data that stored `checked_step_ids`.
- Escaped learner-entered parking-lot text before rendering it inside custom HTML.
- Added `ui_safety.py` with reusable `safe_html_text` and `truncate_text` helpers.
- Normalized imported progress JSON before saving it, so old or malformed progress files are migrated to the current lesson schema.
- Added a type check so importing a non-object JSON file does not crash the app.
- Changed exported progress filenames to use the safe profile slug instead of raw profile text.
- Hooked low-stimulation preference into the app theme.
- Added a fake-Streamlit app import smoke test to catch missing imports/name errors even when Streamlit is not installed in the packaging container.

## Automated checks

```text
python -m compileall -q .
completed successfully

python -m pytest -q
64 passed in 2.13s
```

## Fresh new-user smoke test

```text
profile: New User V8 QA
initial mission day: 1
initial mission title: Start Python without fear
daily coach steps: 6 steps / 30 minutes
nudge after completed checklist: Session checklist complete. Save the mission reflection and stop while the win is visible.
lesson completion: 0.083
daily plan completion: 0.033
daily missions complete: 1
checklist completion: 1.0
quiz percent: 100.0
code sample passed: True
prompt score: 10/10
project milestones done: 1
recommended project: quiz_scorekeeper
ai stats: {'total': 21, 'started': 1, 'completed': 0, 'certificate_options': 9}
next official ai: gumloop_ai_fundamentals
xp: 150
level: Level 2 - Habit Builder
badges: first_step, quiz_starter, focus_reset, prompt_builder, project_starter, ai_track
review queue: 01-python-mindset, 02-variables-types, 03-conditionals
parking lot saved text: <script>alert(1)</script> research keyboard later
```

The parking-lot smoke test intentionally saves HTML-looking text. The app stores the text as a note, but the display path escapes it before raw HTML rendering.

## Browser/Xcode limitation

This environment cannot run Xcode and does not have Streamlit installed, so I could not perform a real browser-click or iOS Simulator test here. The fake-Streamlit runtime smoke test imports `app.py` and catches missing-name errors in the main app flow, while the remaining tests cover learning logic, progress storage, code challenges, official AI resources, projects, and prompt scoring.

## Next production upgrades

Before public launch, add login/auth, database-backed progress storage, and a secure sandbox for running user code.
