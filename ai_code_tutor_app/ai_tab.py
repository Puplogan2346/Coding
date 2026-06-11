"""AI Tutor tab — chat interface backed by the optional AI tutor.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from ai_tutor import ai_is_configured, call_ai_tutor


def render_ai_tab(lesson) -> None:
    st.header("🤖 AI Tutor")
    st.write("Ask about the current lesson, your code, debugging, project ideas, or prompt quality.")

    ai_ready = ai_is_configured()
    if not ai_ready:
        st.info("AI is optional. Add OPENAI_API_KEY to enable live tutor responses. The chat input is disabled until then.")

    if st.button("Clear chat"):
        st.session_state.ai_messages = []
        st.rerun()

    if "ai_messages" not in st.session_state or not st.session_state.ai_messages:
        st.session_state.ai_messages = [
            {
                "role": "assistant",
                "content": (
                    f"Hi. I can help with {lesson.title}. Ask me for a hint, an explanation, "
                    "a practice question, or help improving a prompt."
                ),
            }
        ]

    for message in st.session_state.ai_messages:
        role = message.get("role", "assistant")
        with st.chat_message(role):
            st.write(message.get("content", ""))

    chat_prompt = st.chat_input("Ask your tutor", disabled=not ai_ready)
    if chat_prompt:
        st.session_state.ai_messages.append({"role": "user", "content": chat_prompt})
        tutor_response = call_ai_tutor(
            st.session_state.ai_messages,
            lesson_title=lesson.title,
            lesson_level=lesson.level,
        )
        st.session_state.ai_messages.append({"role": "assistant", "content": tutor_response})
        st.rerun()
