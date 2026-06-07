# Private Product Guide

This app is now designed to be a private standalone learning product, not just a ChatGPT artifact.

## Private access

For local-only use, you can leave private mode off.

For any hosted link, set a private passcode before sharing:

```bash
APP_PRIVATE_MODE=true
APP_PRIVATE_PASSCODE="choose-a-long-private-code"
```

In Streamlit Community Cloud, add those values in the app secrets panel. Do not commit `.streamlit/secrets.toml`.

## Daily learning loop

The intended loop is:

1. Open the app.
2. Press **Start Today**.
3. Pick 10, 30, or 45 minutes based on your energy.
4. Complete one visible block at a time.
5. Use **Stop & save for later** when interrupted.
6. Resume later from the same pace, lesson, checked blocks, proof draft, and review note.
7. Save a proof card when done.

## Learning goal

By the end of the app, the learner should be able to:

- explain basic coding concepts in plain English;
- write small Python scripts;
- use variables, conditionals, loops, functions, lists, dictionaries, files/JSON, and classes at a beginner level;
- read and fix beginner error messages;
- write simple tests or checks;
- use AI for hints, review, explanation, and verification without skipping understanding;
- complete a small capstone project and explain how it works.

## Data and backups

Progress is saved to JSON for easy inspection and export. The app also writes a SQLite snapshot backup in:

```text
data/ai_code_tutor_progress.sqlite3
```

The sidebar includes a **Download private backup pack** button. That zip includes:

- `progress_backup.json`
- `learning_transcript.md`
- `graduation_certificate.md`
- `README.txt`

Keep backups private because they may include notes, proof cards, mistakes, and learning reflections.

## Graduation

Use the **Path** tab to see:

- milestone progress;
- graduation checklist;
- skill map;
- certificate preview;
- transcript export;
- capstone proof idea.

The certificate is personal proof, not an accredited credential.

## Recommended daily cadence

Most days: use **30 min daily**.

Low-energy days: use **10 min rescue**. It counts because the goal is to keep contact with code.

High-energy days: use **45 min deep dive** for projects, debugging, or capstone progress.

## Before making it public

Keep the repo private until you add real user accounts and a production-safe code runner. For personal private use, the passcode gate plus private GitHub repo is enough to start.
