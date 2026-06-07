# V11 Daily Coding Gym Optimization Report

## Goal

Convert the app from a dashboard-style learning tool into a daily-use coding gym for a beginner who wants to learn Python in short, repeatable sessions.

The intended daily loop is now:

```text
Open app -> Start Today -> complete one workout block at a time -> save a proof card -> stop
```

## Product changes

- Renamed the core Today experience to **Daily Coding Gym**.
- Added a large **Start Today** entry point so a new user does not need to decide where to go.
- Added workout modes:
  - **10 min rescue**: show up, touch one code idea, save proof.
  - **30 min daily**: warm-up, lesson, coding reps, AI/prompt drill, proof card.
  - **45 min deep dive**: review, lesson, project/code reps, debug, proof card.
- Added one-screen workout blocks with minutes, action, proof, and why-it-helps copy.
- Added a **proof card** closeout with next-review text.
- Added a **mistake notebook** so bugs and confusion become future review cards.
- Added a lightweight adaptive **review queue** from weak quiz scores, mistake cards, and recent lessons.
- Added daily-gym and mistake-card XP/badges.
- Kept the existing advanced tabs available, but the first path now feels more like a guided workout than a dashboard.

## Code changes

New module:

```text
coding_gym.py
```

Main helpers added:

```text
gym_blocks_for_choice
gym_completion
gym_progress_label
next_gym_action
gym_motivation_copy
build_review_items
proof_card_summary
workout_finish_status
```

Progress schema additions:

```text
gym_sessions
mistake_cards
```

Progress helpers added:

```text
record_gym_session
gym_session_is_saved
add_mistake_card
close_mistake_card
```

Gamification additions:

```text
Daily Gym badge
Mistake Mapper badge
gym-session XP
mistake-card XP
```

## Fresh new-user QA

```text
profile: V11 New User QA
initial mission: Day 1 - Start Python without fear
workout blocks: Warm-up review, Learn one idea, Coding reps, AI/prompt drill, Proof card
workout minutes: 30
initial gym completion: 0.0
initial next action: Next rep: Warm-up review
initial motivation: Press Start Today, then only do the first block. No planning required.
after workout gym saved: True
after workout gym completion: 1.0
daily plan completion: 0.033
finish status: Saved
proof card: Day 1 proof: Start Python without fear | I learned the difference between print and return. | next return values
review queue count: 2
first review: Quiz score 66.7% -> Redo one missed idea, then write the correct pattern from memory.
xp: 52
level: Level 1 - New Coder
badges: daily_gym, mistake_mapper, quiz_starter
```

## Automated QA

```text
python -m compileall -q .
completed successfully

python -m pytest -q
81 passed in 1.91s
```

## Known limitation

This environment still cannot run a real Streamlit browser-click test or an Xcode Simulator test. The app was tested through compile checks, unit tests, static app integrity checks, a fake-Streamlit import smoke test, and a fresh-user daily-gym simulation.
