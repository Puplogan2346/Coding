# V14 Stop/Resume + Time-Based Lesson QA Report

This pass tightened the exact daily-use behavior requested: saved preferred workout length, stopping mid-session, resuming later, and changing the day lesson based on how much time is available.

## UX improvements

- The Today tab now exposes the time choice as **Time I have today** for 10, 30, or 45 minutes.
- The selected time drives the lesson selector before the workout starts.
- A saved workout locks its time and lesson when resumed so the checklist, proof draft, and review note do not mismatch.
- **Save current draft** parks the workout as `In workout` and stores the checklist, proof draft, selected lesson, selected pace, and next-review note.
- **Stop & save for later** remains the clear close-the-app-safe action.
- A new resume banner summarizes what was saved: pace, lesson, block progress, proof draft, and next review.
- The app can recover older/bad saved pace labels by using the saved minute value.
- Starting a workout can also save the selected 10/30/45-minute length as the future default via the new checkbox.

## Focused QA result

```text
preferred default minutes: 10
resume active: True
resume locked: True
resume source: saved_pace
resume pace: 10 min rescue
resume lesson: 02-variables-types
resume status: In workout
resume step_state: {'open': True, 'proof': False, 'tiny_rep': True}
resume proof: I stopped after practicing variables and want to continue later.
resume next_review: string vs int
resume summary: 2/3 blocks; Resume where you stopped: 2/3 blocks done
10 min suggestion: 02-variables-types / 10 min rescue review
30 min suggestion: 03-conditionals / today’s plan
45 min suggestion: 03-conditionals / today’s full lesson
legacy pace recovered from minutes: 10 min rescue (saved_minutes)
```

## Automated tests

```text
python -m compileall -q .
completed successfully

python -m pytest -q
101 passed
```

## Covered behaviors

- Preferred workout length persists through `focus_preferences.default_minutes`.
- Invalid imported default minute values are normalized.
- Time can be changed before starting without creating a gym session.
- Start Today creates a resumable workout.
- Stop/save preserves pace, selected lesson, checked blocks, proof draft, and next-review note.
- Reloaded progress resumes with the same saved time and lesson.
- Saved workouts do not show as active resume sessions.
- Older progress with a bad saved pace label can still resume from the saved minutes.
- Time-based lesson options differ for 10, 30, and 45 minute sessions.
