from __future__ import annotations

from html import escape as html_escape
from typing import Any


def safe_html_text(value: Any) -> str:
    """Escape text before inserting it into raw HTML used by Streamlit cards.

    Streamlit's unsafe_allow_html=True is useful for lightweight UI cards, but
    learner-entered values must never be inserted directly. This helper keeps
    the visual card system while rendering user text as text instead of HTML.
    """
    if value is None:
        return ""
    return html_escape(str(value), quote=True)


def h(value: object) -> str:
    """Escape text before inserting it into custom HTML blocks.

    Thin alias of ``safe_html_text`` — kept short because it's used heavily
    inside f-strings that build HTML cards.
    """
    return safe_html_text(value)


def truncate_text(value: Any, limit: int = 300) -> str:
    """Return a safe, display-sized text preview."""
    text = "" if value is None else str(value)
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 0)] + "…"
