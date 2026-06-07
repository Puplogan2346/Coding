# V12 Daily Use QA and Reliability Report

## Goal

Make the app easier to use every day by reducing lost progress, accidental completion, and dashboard-style decision fatigue. The app should behave more like a daily coding gym: start, resume, finish one workout, save proof, and stop.

## Improvements made

1. **Persistent Start Today**
   - Pressing **Start Today** now writes an `In workout` gym session to progress.
   - If the browser refreshes or the app reruns, the Today tab can resume the started workout.

2. **Safer completion flow**
   - A workout can be parked as **In progress** without a proof note.
   - A workout cannot be marked **Completed** unless all visible blocks are complete and a proof sentence exists.
   - This prevents empty streak/XP wins while still allowing low-energy rescue days.

3. **Default pace uses focus preferences**
   - The Today tab now defaults to the learner's saved default session length: 10, 30, or 45 minutes.
   - If a day already has a saved gym pace, the app resumes that pace.

4. **Recent gym history**
   - Added a small recent-history panel so the learner can see saved, parked, and skipped gym sessions.
   - This makes the habit feel visible without adding a dashboard-heavy experience.

5. **Proof-card review queue**
   - Saved `next_review` text from proof cards now feeds into the review queue.
   - Mistake cards, weak quiz scores, proof-card reviews, and recent lessons all contribute to review recommendations.

6. **Linked lesson progress**
   - When a completed daily mission has a linked lesson, that lesson is marked complete.
   - This keeps the Daily Coding Gym and the Learn tab from drifting out of sync.

7. **Progress hardening**
   - Gym sessions preserve their original `created_at` timestamp when updated.
   - Bad minute values are safely normalized.
   - Parking-lot inputs now safely handle non-string values.

## Automated checks

```text
python -m compileall -q .
completed successfully

python -m pytest -q
85 passed in 3.19s
```

## Fresh learner result

```text
Day 1 starts as a 30 min daily workout.
Start Today persists an In workout session.
A partial workout cannot be saved as Completed.
A finished workout with a proof note saves successfully.
Daily mission completion: 1/30
Lesson completion: 1/12
Review queue includes the learner's mistake card and proof-card next-review note.
```

## Known limitations

This environment still cannot run a real Streamlit browser-click session, Xcode Simulator, live OpenAI API call, or private cloud deployment. Those remain manual checks on your machine or hosting target.
