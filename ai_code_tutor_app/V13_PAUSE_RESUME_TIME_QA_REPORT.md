# V13 Pause/Resume + Time-Based Lesson QA Report

## Goal

This pass focused on the exact daily-use behavior requested:

1. The app remembers the learner's preferred workout length.
2. The learner can stop mid-workout, save progress, and continue later.
3. The Today tab can change the day's lesson based on how much time the learner has.
4. The final package is tested before delivery.

## UX changes

- Added a Today-tab **Remember 10/30/45 min** button when the selected workout differs from the saved default.
- Locked the workout pace and selected lesson after a workout has started, so resuming later does not mismatch a saved checklist with a different workout structure.
- Added **Stop & save for later** in the proof-card area. It saves:
  - workout status as `In workout`
  - pace label
  - minutes
  - selected lesson
  - checklist state
  - proof note typed so far
  - next-review note typed so far
- Added **Today's lesson based on time** selector:
  - 10 min rescue favors review/tiny next steps.
  - 30 min daily favors the planned lesson.
  - 45 min deep dive adds stretch/deeper work.
- Completing a changed daily lesson can mark the selected lesson complete; rescue sessions default to protecting the habit without pretending a full lesson is done.

## Automated verification

```bash
python -m compileall -q .
python -m pytest -q
```

Result:

```text
90 passed
```

## Focused simulation result

```text
preferred default minutes: 10
default pace label: 10 min rescue
10 min lesson: 02-variables-types / 10 min rescue review
30 min lesson: 04-loops / today’s plan
45 min lesson: 04-loops / today’s full lesson
stopped/resumable status: In workout
paused active: True
paused pace: 10 min rescue
paused lesson: 02-variables-types
paused proof: I reviewed variables and need to finish proof later.
paused next review: string vs int
paused steps: {'open': True, 'tiny_rep': False, 'proof': False}
paused completion: 0.333
```

## Remaining manual checks

- Real Streamlit browser-click test on the user's machine.
- Xcode/iOS Simulator preview on macOS.
- Live OpenAI API tutor call with a real key.
