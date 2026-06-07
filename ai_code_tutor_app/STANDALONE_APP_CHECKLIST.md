# Standalone app checklist

This app is meant to live outside ChatGPT as a private Streamlit app.

## Local daily use

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Private GitHub use

Keep the repo private until authentication, database-backed progress, and a safer public code runner are added.

```bash
git init
git add .
git commit -m "Add daily coding gym learning app"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/ai-code-tutor.git
git push -u origin main
```

## Required files for standalone readiness

The Deploy tab checks for these files:

- `app.py`
- `streamlit_app.py`
- `requirements.txt`
- `README.md`
- `README_DEPLOY.md`
- `.streamlit/config.toml`
- `Dockerfile`
- `.github/workflows/tests.yml`

It also checks whether the local progress directory is writable, whether a real secrets file is present, whether the public code runner is off, and whether the optional AI tutor key is configured.

## Public sharing safety

For personal use, the app is ready to run locally or in a private deployment.

Before public sharing, add:

- Authentication.
- Database-backed progress storage.
- A proper sandboxed code runner.
- Privacy review for saved notes/progress.
- Deployment smoke test on the exact hosting platform.

Keep this setting for public deployments:

```bash
ALLOW_CODE_RUNNER=false
```
