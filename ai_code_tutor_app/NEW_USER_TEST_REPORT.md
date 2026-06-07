# New User Test Report

Date: 2026-05-28

## What was tested

A fresh learner profile was created with no existing progress. The test simulated the first learning loop:

1. Load a new learner profile.
2. Confirm progress starts at zero.
3. Complete lesson 1.
4. Save a perfect lesson 1 quiz result.
5. Run the lesson 1 sample code against the lesson tests.
6. Save a learner note.
7. Score a beginner prompt in Prompt Lab.
8. Reload the profile and confirm the data persisted.

## Result

Passed.

```text
profile: New User Smoke Test
starting lessons: 12
first lesson: Python mindset: commands, output, and mistakes
completion after one lesson: 0.083
lessons remaining after one lesson: 11
quiz percent: 100.0
code lab sample solution passed: true
prompt score: 10/10
```

## UX observations from the new-user flow

Good:

- The first lesson is beginner-friendly and starts with output, errors, and tiny experiments.
- The dashboard recommends the next lesson automatically.
- Progress, quiz scores, notes, and prompt scores persist correctly.
- The app works without the AI tutor connected.
- The code runner is safely off by default for sharing.

Improved in this version:

- Added a first-run welcome message for empty profiles.
- Added a “Start here: your first 10 minutes” checklist.
- Disabled AI action buttons when `OPENAI_API_KEY` is missing, instead of letting users click into a setup error.
- Added a Private GitHub checklist and git commands directly inside the Deploy tab.
- Added this new-user journey as an automated test.

Still worth improving later:

- Add true accounts/login before sharing with other learners.
- Move progress storage from JSON files to a database.
- Add a real sandbox before enabling public code execution.
- Add visual badges or celebrations after a learner finishes a lesson.


## v6 30-minute daily-flow smoke test

A brand-new learner profile was simulated from zero progress through the first daily mission, first lesson, first quiz, first code-lab sample solution, first prompt score, and first official AI resource queue.

```text
initial_mission: 1 Start Python without fear
initial_plan_completion: 0.0
initial_review_queue: 01-python-mindset, 02-variables-types, 03-conditionals
initial_xp: 0 Level 1 - New Coder
after_day1_mission: 2 Variables are labels
daily_missions_complete: 1
study_streak: 1
lesson_completion: 0.083
lessons_remaining: 11
quiz_percent: 100.0
code_solution_passed: True
prompt_score: 10/10
xp_level: 115 Level 1 - New Coder
badges: First Step, Quiz Starter, Prompt Builder, AI Track Starter
next_ai: gumloop_ai_fundamentals
```
