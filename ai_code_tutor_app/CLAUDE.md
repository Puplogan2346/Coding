# AI Code Tutor — session bootstrap (keep this file tiny)

**Do not explore this repo.** Everything needed is pre-mapped:

1. Read `.claude/skills/improve-tutor/SKILL.md` — file map, conventions, the
   stdlib-only auto-grader constraint, verify + ship workflow.
2. Picking work? Read `ROADMAP.md` — ready-to-execute specs with exact files,
   patterns to copy, and tests. Implement from the spec; open only named files.
3. Verify once at the end: `./.venv/bin/python -m pytest -q` (system python3
   is 3.9 — don't use it; the venv runs 3.12 + pinned streamlit), then the
   AppTest render check from the playbook.
4. One commit per task. Push to `main` auto-deploys (Streamlit Cloud). CI runs
   the suite on every push.
5. Working style: push multi-step work through to done without pausing to ask
   permission mid-way; stop only for destructive actions or real scope changes.
6. New machine or account? `MIGRATION.md` is the one-time setup runbook.
