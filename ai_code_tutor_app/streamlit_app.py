"""Streamlit Community Cloud entrypoint.

The main application lives in app.py. This wrapper lets hosting platforms that expect
`streamlit_app.py` run the same app without duplicating code.
"""

import runpy

runpy.run_path("app.py", run_name="__main__")
