# New User Official AI Tracker Smoke Test

Date: 2026-05-28

A fresh learner profile was simulated from zero official AI progress through the starter AI resource path.

## Scenario

- Create a fresh profile named `New Official AI User`.
- Queue the starter path resources:
  - Gumloop AI Fundamentals
  - Getting Started with Gumloop
  - Anthropic Academy
- Mark Gumloop AI Fundamentals as completed.
- Save and reload the profile.

## Result

```text
resource catalog count: 21
starter path ids: gumloop_ai_fundamentals, gumloop_getting_started, anthropic_academy
started count: 3
completed count: 1
gumloop note: Finished first Gumloop AI foundation resource.
progress file exists: True
```

## Takeaway

The AI Certs section can store official-resource status and private notes for a brand-new user without interfering with Python lesson progress.
