"""Quiz tab — per-lesson quiz form, scoring, and saved results.

Imports come straight from the leaf domain modules so there is no dependency
back on ``app.py``, keeping the per-tab split acyclic.
"""
from __future__ import annotations

import streamlit as st

from progress import record_quiz_score, save_progress
from ui_components import render_score_badge


def render_quiz_tab(progress_data: dict, progress_path, lesson) -> None:
    st.header(f"Quiz: {lesson.title}")
    st.write("Answer all questions, then submit. You can retake quizzes anytime.")

    with st.form(key=f"quiz_form_{lesson.id}"):
        selected_answers = []
        for index, question in enumerate(lesson.quiz, start=1):
            selected = st.radio(
                f"{index}. {question.prompt}",
                question.options,
                index=None,
                key=f"quiz_{lesson.id}_{index}",
            )
            selected_answers.append(selected)

        submitted = st.form_submit_button("Submit quiz", type="primary")

    if submitted:
        if any(answer is None for answer in selected_answers):
            st.warning("Please answer every question before submitting.")
        else:
            score = 0
            details = []
            for selected, question in zip(selected_answers, lesson.quiz):
                is_correct = selected == question.answer
                score += int(is_correct)
                details.append((question, selected, is_correct))

            record_quiz_score(progress_data, lesson.id, score, len(lesson.quiz))
            save_progress(progress_data, progress_path)
            render_score_badge(score, len(lesson.quiz))

            for question, selected, is_correct in details:
                if is_correct:
                    st.success(f"Correct: {question.prompt}")
                else:
                    st.error(f"Missed: {question.prompt}")
                    st.write(f"Your answer: {selected}")
                    st.write(f"Correct answer: {question.answer}")
                st.caption(question.explanation)

    existing_score = progress_data.get("quiz_scores", {}).get(lesson.id)
    if existing_score:
        st.divider()
        st.write(
            f"Last saved score for this lesson: **{existing_score['score']}/{existing_score['total']}** "
            f"({existing_score['percent']}%)."
        )
