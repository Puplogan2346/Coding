# V14 Stop/Resume + Time-Fit QA Report

This pass focuses on the daily-use behavior requested by the learner:

1. Remember the preferred workout length.
2. Let the learner stop mid-workout and continue later.
3. Let the learner change the day's lesson based on whether they have 10, 30, or 45 minutes.
4. Test the behavior before packaging.

## UX changes

- The Today tab now makes the time choice more explicit with a saved default note.
- A learner can choose 10, 30, or 45 minutes before pressing Start Today.
- A preview expander shows how each time choice changes the recommended lesson.
- Once a workout is started, the app locks the saved pace and lesson so the checklist, proof draft, and resume state do not mismatch.
- The resume banner shows saved pace, selected lesson, checked blocks, workout status, proof draft, and next-review note.
- The draft-save flow preserves the same data as Stop & save for later.

## Reliability checks added

- `workout_resume_setup` locks a saved workout even if the learner changes the preferred default afterward.
- A saved 10-minute rescue workout still resumes as 10 minutes even if the profile default becomes 45 minutes.
- A saved lesson stays first in the lesson picker during resume.
- Old saved sessions with missing pace labels recover from saved minutes.
- New users with no started workout use the saved preferred default.

## Commands run

```bash
python -m compileall -q .
python -m pytest -q
```

## Results

```text
python -m compileall -q .
completed successfully

python -m pytest -q
101 passed
```

## Focused behavior result

```text
preferred default can be saved as 10, 30, or 45 minutes
no-start setup uses saved preferred minutes
started workout locks saved pace and lesson
paused workout status remains In workout
paused proof draft is preserved
paused next-review note is preserved
paused checklist state is preserved
changing default after pause does not override saved workout
saved lesson appears as the first resume option
old sessions with missing pace recover from saved minutes
```

## Remaining manual checks

The automated tests cover the logic and app import integrity. Manual checks still needed on a local machine:

- Click through the Streamlit UI in a browser.
- Close/reopen the browser after Stop & save for later.
- Try the Xcode/iOS Simulator WebView wrapper on macOS.
- Try the live AI Tutor with a real OpenAI API key.
