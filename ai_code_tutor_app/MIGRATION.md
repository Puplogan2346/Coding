# Migration runbook — new laptop / new Claude account

Everything needed to continue this project lives in this GitHub repo
(`Puplogan2346/Coding`, private). Nothing important is stranded on any one
laptop. Follow this once on the new machine and you're fully set up.

## 1. GitHub access (new laptop)

The remote uses SSH. On the new laptop:

```bash
ssh-keygen -t ed25519 -C "your_email"        # accept defaults
cat ~/.ssh/id_ed25519.pub                    # copy the output
```

Add that key at github.com → Settings → SSH and GPG keys → New SSH key. Then:

```bash
git clone git@github.com:Puplogan2346/Coding.git
cd Coding/ai_code_tutor_app
```

## 2. Python + project environment

The app requires **Python 3.10+** (streamlit 1.58 dropped 3.9; macOS system
Python is 3.9). Easiest on a fresh Mac: install the latest Python from
https://www.python.org/downloads/ (or `brew install python` if you use
Homebrew). Then:

```bash
python3.12 -m venv .venv          # use whatever 3.10+ you installed
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q               # expect 160+ passed
streamlit run app.py              # local run
```

## 3. Claude Code (new account)

Install Claude Code, then open the `ai_code_tutor_app` folder and start a
session. **No setup or context transfer needed:**

- `CLAUDE.md` auto-loads and tells the session not to explore.
- `.claude/skills/improve-tutor/SKILL.md` (committed) is the codebase map,
  conventions, and verify/ship workflow.
- `ROADMAP.md` holds ready-to-execute improvement specs. The cheap loop is:
  *"do roadmap item 1.2"* → session reads ~3 small files → implements → runs
  the suite once → one commit → push (auto-deploys).

Claude memory from the old account does not transfer — by design it isn't
needed; the repo docs above carry all project knowledge.

## 4. What does NOT auto-transfer (and what to do)

| Thing | Where it lives | Action |
|---|---|---|
| App source, tests, docs, playbook, roadmap | This repo | Nothing — clone gets it all |
| Deployed app | Streamlit Cloud, deploys from this repo's `main` | Nothing — pushing still auto-deploys. Dashboard access is via your GitHub login at share.streamlit.io |
| `OPENAI_API_KEY` (AI tutor) | Streamlit Cloud → app → Settings → Secrets | Nothing for the deployed app. For local AI, re-export the key in your shell or `.streamlit/secrets.toml` (never commit it) |
| `APP_PRIVATE_PASSCODE` (private gate) | Streamlit Cloud secrets | Nothing — stays configured in the Cloud panel |
| Your learning progress | The deployed app's container + in-app exports | Old-laptop local data was verified empty (test artifacts only). For durable backups of real progress, use sidebar → **Progress tools → Download private backup pack** in the deployed app periodically — Cloud container storage is wiped on redeploys |
| Local dev progress files (`data/`, `*.json`) | Gitignored by design | Disposable test artifacts; don't migrate |

## 5. Sanity checklist after migrating

- [ ] `git push` works from the new laptop (SSH key OK)
- [ ] `python -m pytest -q` green in the new venv
- [ ] `streamlit run app.py` opens the app locally
- [ ] A trivial commit pushed to `main` redeploys the Cloud app
- [ ] Claude Code session in the folder answers "what's next?" from ROADMAP.md
  without scanning the repo
