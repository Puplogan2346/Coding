# V18 Layout Fix Report

This version fixes the first real usability issue found during local testing: the app worked, but the daily learning flow required too much scrolling and the Stop & save action was too hard to find.

## Changes

- Removed the large feature-card row from the top of the app.
- Made the hero smaller and more focused on the daily coding gym.
- Collapsed the sidebar by default so the learner has more space.
- Collapsed path/milestone details under an optional expander.
- Added a sticky daily action card near the top of Today.
- Added a visible Stop & save for later button beside the current rep controls.
- Kept the proof-card stop button as a backup.
- Pinned Streamlit to 1.50.0 for Python 3.9 compatibility.
- Removed the unsupported st.pills(required=True) argument.
- Cleaned Streamlit config to avoid the local CORS/XSRF warning.

## Test results

```text
python3 -m py_compile app.py
passed

pytest -q
123 passed
```

## Daily flow target

Open app -> Today -> Start/Resume -> Do one rep -> Stop & save or Save proof -> leave.
