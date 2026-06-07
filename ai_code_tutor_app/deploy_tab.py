"""Deploy tab — sharing, standalone readiness, and deployment checklist.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from progress import progress_db_path
from standalone_check import standalone_checks, standalone_summary
from ui_components import render_card, render_standalone_check

# The app's source files live in this module's directory. Resolve checks against
# it so the readiness check works regardless of the process working directory
# (e.g. Streamlit Cloud runs from the repo root, not ai_code_tutor_app/).
APP_DIR = Path(__file__).resolve().parent


def render_deploy_tab(progress_path) -> None:
    st.header("Make it shareable")
    st.write(
        "This package is set up for Streamlit Community Cloud, Docker-based hosting, and Render-style Python services."
    )

    render_card(
        "Public-safe default",
        "The code runner is off unless ALLOW_CODE_RUNNER=true. Keep it off when other people can use the app.",
        "warning-soft",
    )

    st.subheader("Private GitHub checklist")
    st.markdown(
        "Keep the repository visibility set to **Private** while you are building. "
        "Only deploy or make public after the app has authentication, safer progress storage, and a production code-runner plan."
    )
    st.code(
        """git init
git add .
git commit -m "Initial private AI Code Tutor app"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/ai-code-tutor.git
git push -u origin main""",
        language="bash",
    )

    st.subheader("Standalone readiness check")
    st.caption(f"SQLite backup store: `{progress_db_path()}`")
    checks = standalone_checks(app_dir=APP_DIR, data_dir=progress_path.parent)
    st.caption(standalone_summary(checks))
    for check in checks:
        render_standalone_check(check)

    st.subheader("Deployment checklist")
    st.checkbox("Create the GitHub repository with visibility set to Private", value=False)
    st.checkbox("Add OPENAI_API_KEY as a platform secret, not inside code", value=False)
    st.checkbox("Set ALLOW_CODE_RUNNER=false for public deployments", value=True)
    st.checkbox("Review official AI resource links before sharing publicly", value=True)
    st.checkbox("Run pytest before sharing the link", value=True)
    st.checkbox("Complete the new-user 30-day flow smoke test after big changes", value=True)

    st.subheader("Useful commands")
    st.code(
        """# Local
pip install -r requirements.txt
streamlit run app.py

# Tests
pytest -q

# Docker
docker build -t ai-code-tutor .
docker run -p 8501:8501 --env-file .env ai-code-tutor""",
        language="bash",
    )

    st.subheader("Test on iPhone Simulator through Xcode")
    st.write(
        "Run the Streamlit app locally, open Xcode's iOS Simulator, and load the app in Simulator Safari. "
        "The package also includes a simple SwiftUI WKWebView wrapper in `ios_wrapper/`."
    )
    st.code(
        """streamlit run app.py --server.address 0.0.0.0 --server.port 8501
# Then open http://localhost:8501 in iOS Simulator Safari.""",
        language="bash",
    )
    st.info("See README_DEPLOY.md and XCODE_IOS_TESTING.md for the full step-by-step guides.")
