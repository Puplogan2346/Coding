# V9 UX/UI optimization report

This pass focused on making the app feel less like a dashboard and more like a daily learning coach for a brand-new coder using it in short sessions.

## UX audit findings

The v8 app was stable, but the first screen still asked the learner to interpret several sections at once. For an ADHD-friendly learning app, the highest-impact improvement was to make the next action obvious and keep the plan visible without turning the page into a scoreboard.

## Improvements added

- Added a **30-day visual timeline** to the Today tab so the learner can see current, completed, skipped, and upcoming days at a glance.
- Added **10 / 30 / 45 minute pace choices**:
  - 10 min rescue keeps the streak/habit alive.
  - 30 min daily is the default training plan.
  - 45 min deep dive supports project or challenge days.
- Added a prominent **Do this now** action callout generated from the first unfinished checklist step.
- Added **Now / Then / Proof** micro-cards to reduce working-memory load.
- Added stronger **level progress** feedback with XP-to-next-level copy.
- Improved the hero area with today's mission, next lesson, streak, and XP.
- Added mobile-friendly CSS for smaller screens.
- Added clearer focus outlines and larger rounded buttons for accessibility and touch use.
- Extended low-stimulation mode to the new action callout, timeline dots, and mini-cards.
- Moved new UX logic into `experience.py` so the UI rules can be tested without Streamlit.

## New files

```text
experience.py
V9_UX_OPTIMIZATION_REPORT.md
tests/test_experience.py
tests/test_gamification_levels.py
```

## Tests run

```text
python -m compileall -q .
completed successfully

python -m pytest -q
70 passed in 1.69s
```

## Fresh new-user QA

```text
profile: V9 New User QA
initial lesson completion: 0.0
initial daily completion: 0.0
today mission: Day 1 - Start Python without fear
timeline first five: 1:current, 2:upcoming, 3:upcoming, 4:upcoming, 5:upcoming
pace: The normal read-practice-check-reflect session for steady progress.
next action: Do this now: Open and orient
stage cards: Now / Then / Proof
checklist: 0 of 6 steps 0%
recommended project: quiz_scorekeeper
after lesson completion: 0.083
after daily completion: 0.033
daily missions complete: 1
quiz percent: 100.0
code sample passed: True
prompt score: 10/10
xp: 150
level: Level 2 - Habit Builder
xp to next: 300
next project milestone: Write the score function
review queue: 01-python-mindset, 02-variables-types, 03-conditionals
```

## Manual testing limitation

This container still does not include Streamlit or Xcode, so I could not perform a live browser-click or iOS Simulator test here. The app was syntax-compiled, app-import smoke-tested with fake Streamlit, and the core new-user flow was tested directly through the app modules.

## Next UX upgrades

- Add a visible countdown/focus timer for each checklist block.
- Add real spaced-repetition cards from missed quiz questions.
- Add a mobile bottom navigation wrapper if the Streamlit version supports it well enough.
- Add a first-run walkthrough modal after authentication is added.
