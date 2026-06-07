"""Glossary tab — a searchable reference of every key term in the course.

Read-only; lives in the More tab. Imports straight from the leaf ``glossary``
module so there is no dependency back on ``app.py``.
"""
from __future__ import annotations

import streamlit as st

from glossary import GLOSSARY


def render_glossary_tab() -> None:
    st.subheader("📖 Glossary")
    st.caption(f"Plain-English definitions for all {len(GLOSSARY)} key terms across the lessons.")

    query = st.text_input(
        "Search terms",
        placeholder="e.g. function, JSON, loop, groupby",
        key="glossary_search",
    ).strip().lower()

    terms = sorted(GLOSSARY)
    if query:
        terms = [term for term in terms if query in term or query in GLOSSARY[term].lower()]

    st.caption(f"Showing {len(terms)} of {len(GLOSSARY)} terms.")
    if not terms:
        st.info("No terms match your search. Try a simpler word.")
        return
    for term in terms:
        st.markdown(f"- **{term}** — {GLOSSARY[term]}")
