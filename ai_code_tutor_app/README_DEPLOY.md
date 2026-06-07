# Deployment Guide

This app can live outside ChatGPT as a real web app. While it is still being built, keep the GitHub repository private and do not publish a public app URL. The simplest future deployment path is Streamlit Community Cloud. Docker and Render-style deployment files are also included.

## Keep it private while building

Create the GitHub repository with **Private** visibility. GitHub Actions can still run tests in a private repository, and your code will not be publicly browsable. See `PRIVATE_GITHUB_SETUP.md` for the exact setup steps.

Local git setup after creating the private GitHub repo:

```bash
git init
git add .
git commit -m "Initial private AI Code Tutor app"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/ai-code-tutor.git
git push -u origin main
```

## Option 1: Streamlit Community Cloud

Best for: quick sharing and demos after you are ready to share. Do not deploy publicly yet if you want the app private to you.

1. Create a new private GitHub repository.
2. Upload this whole folder to the repository.
3. Make sure the repo includes:
   - `app.py`
   - `streamlit_app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
4. Go to Streamlit Community Cloud and create a new app from your GitHub repo.
5. Select `streamlit_app.py` or `app.py` as the entrypoint.
6. Add secrets in the Streamlit Cloud secrets panel. For a private hosted app, include the private passcode settings too:

```toml
OPENAI_API_KEY = "your_api_key_here"
OPENAI_MODEL = "gpt-5.5"
APP_PRIVATE_MODE = true
APP_PRIVATE_PASSCODE = "choose-a-long-private-code"
```

7. Keep the code runner disabled for public users:

```text
ALLOW_CODE_RUNNER=false
```

8. Deploy and share the generated app URL.

## Option 2: Docker

Best for: VPS, cloud hosts, private servers, or platforms that support containers.

```bash
cp .env.example .env
# Add OPENAI_API_KEY to .env only on your own machine or server.

docker build -t ai-code-tutor .
docker run -p 8501:8501 --env-file .env ai-code-tutor
```

With Docker Compose:

```bash
docker compose up --build
```

The Docker setup exposes port `8501` and keeps `ALLOW_CODE_RUNNER=false` by default.

## Option 3: Render-style Python service

Best for: a simple hosted service with a web URL.

A `render.yaml` file is included. You can connect the GitHub repo to Render and use this setup:

```bash
pip install -r requirements.txt
streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
```

Set these environment variables on the hosting platform:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.5
ALLOW_CODE_RUNNER=false
APP_DATA_DIR=data
APP_PRIVATE_MODE=true
APP_PRIVATE_PASSCODE=choose-a-long-private-code
```

## Progress storage

This version saves readable JSON progress files in the `data/` folder and also writes a SQLite snapshot backup to `data/ai_code_tutor_progress.sqlite3`. That is good for private single-user learning. For multi-user public release, move progress to a hosted database such as Postgres, Supabase, Firebase, or another managed database.

## Public code execution warning

The Code Lab can run Python tests locally only if you set:

```bash
ALLOW_CODE_RUNNER=true
```

Do not enable this for a public app unless you add a real sandbox/container isolation system. Running arbitrary user code on a public server is dangerous.

## Private-before-public checklist

Before making the repository public or sharing a deployment URL:

- Set `APP_PRIVATE_MODE=true` and `APP_PRIVATE_PASSCODE` for any hosted personal link.
- Add real user accounts if anyone besides you will use it.
- Replace local JSON/SQLite progress with a hosted database if multiple users will use it.
- Keep `ALLOW_CODE_RUNNER=false` unless a real sandbox is added.
- Verify no secret files are committed.
- Review the AI Certs official-resource links.
- Run the tests below.

## Pre-share test commands

```bash
pytest -q
python -m compileall .
```

Before sharing the URL, verify:

- AI Tutor works when the API key is configured.
- App still works when the API key is missing.
- Code runner is disabled publicly.
- No `.env` or `.streamlit/secrets.toml` file is committed.
- Learner profiles create separate progress files.
- AI Certs statuses and notes save correctly for your profile.

## Private mobile preview through Xcode

This app is not a native iOS app, but you can test the mobile feel before deployment:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then open Xcode's iOS Simulator and load:

```text
http://localhost:8501
```

If localhost does not work in the Simulator, use your Mac's local IP address. For a more app-like shell, see the SwiftUI `WKWebView` files in `ios_wrapper/` and the step-by-step guide in `XCODE_IOS_TESTING.md`.

## V16 standalone readiness check

The Deploy tab now includes a built-in standalone readiness check. It verifies required files, writable progress storage, SQLite backup storage, private-access setup, safe code-runner defaults, secrets-file risk, and optional AI-key status.

Run these before you deploy or share a private link:

```bash
python -m compileall -q .
pytest -q
streamlit run app.py
```

Then open the **Deploy** tab and review the standalone checks. A warning about `OPENAI_API_KEY` is okay if you do not want the AI Tutor enabled yet. A warning about `ALLOW_CODE_RUNNER=true` should be fixed before any hosted deployment.
