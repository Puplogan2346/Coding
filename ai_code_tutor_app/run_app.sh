#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
. .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
