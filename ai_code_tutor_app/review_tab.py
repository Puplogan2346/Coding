"""Review section — progress-based lesson recommendations and a mixed quiz.

Read-only with respect to saved progress (it selects content based on progress
but does not record the review quiz). Imports straight from leaf modules so there
is no dependency back on ``app.py``.
"""
from __future__ import annotations

import streamlit as st

from curriculum import LESSONS
from progress import record_review_result, save_progress
from review import build_review_quiz, lessons_to_review, next_lesson_to_study, quiz_percent


def _go_to_lesson(lesson_id: str) -> None:
    st.session_state.selected_lesson_id = lesson_id
    st.rerun()


def render_review_tab(progress_data: dict, progress_path) -> None:
    st.subheader("🔁 Review — based on your progress")
    completed = set(progress_data.get("completed_lessons", []) or [])
    total = len(LESSONS)
    review_list = lessons_to_review(progress_data)

    taken = [quiz_percent(progress_data, lesson.id) for lesson in LESSONS]
    taken = [percent for percent in taken if percent is not None]
    avg_quiz = int(round(sum(taken) / len(taken))) if taken else 0

    cols = st.columns(3)
    cols[0].metric("Lessons done", f"{len(completed)}/{total}")
    cols[1].metric("To review", len(review_list))
    cols[2].metric("Avg quiz score", f"{avg_quiz}%")

    history = progress_data.get("review_history", []) or []
    if history:
        last = history[-1]
        st.caption(
            f"📈 Last review quiz: {last.get('score')}/{last.get('total')} "
            f"({last.get('percent')}%) · {len(history)} review(s) taken."
        )

    # Progress-based lesson recommendations.
    if len(completed) < total:
        nxt = next_lesson_to_study(progress_data)
        st.markdown(f"**📚 Study next:** {nxt.title}")
        if st.button(f"Open {nxt.title}", key="review_study_next", type="primary"):
            _go_to_lesson(nxt.id)
    else:
        st.success("🎉 You've completed every lesson. Use the review quiz to keep it sharp.")

    if review_list:
        st.markdown("**🔁 Worth reviewing** — completed, but the quiz isn't passed yet (70%+):")
        for lesson in review_list[:6]:
            percent = quiz_percent(progress_data, lesson.id)
            status = f"{int(percent)}%" if percent is not None else "not quizzed yet"
            if st.button(f"Review: {lesson.title} — {status}", key=f"review_pick_{lesson.id}"):
                _go_to_lesson(lesson.id)
    elif completed:
        st.caption("No weak spots right now — every completed lesson is passing. Nice work.")

    st.divider()

    # Progress-based mixed quiz.
    st.markdown("**🧠 Mixed review quiz** — questions pulled from the lessons you've completed.")
    review_quiz = build_review_quiz(progress_data, max_questions=5)
    if not review_quiz:
        st.info("Complete a lesson (and pass its quiz) to unlock a mixed review quiz.")
        return

    with st.form(key="mixed_review_quiz"):
        answers = []
        for index, (lesson, question) in enumerate(review_quiz, start=1):
            selected = st.radio(
                f"{index}. {question.prompt}  (from: {lesson.title})",
                question.options,
                index=None,
                key=f"review_q_{index}",
            )
            answers.append((lesson, question, selected))
        submitted = st.form_submit_button("Submit review quiz", type="primary")

    if submitted:
        if any(selected is None for _, _, selected in answers):
            st.warning("Please answer every question before submitting.")
            return
        score = sum(1 for _, question, selected in answers if selected == question.answer)
        total_q = len(answers)
        record_review_result(progress_data, score, total_q)
        save_progress(progress_data, progress_path)
        percent = round(score / total_q * 100)
        if percent >= 80:
            st.success(f"Review score: {score}/{total_q} ({percent}%). Strong recall!")
        elif percent >= 50:
            st.warning(f"Review score: {score}/{total_q} ({percent}%). Revisit the misses below.")
        else:
            st.error(f"Review score: {score}/{total_q} ({percent}%). Worth re-reading these lessons.")
        for lesson, question, selected in answers:
            if selected == question.answer:
                st.caption(f"✅ {question.prompt}")
            else:
                st.caption(f"❌ {question.prompt} — correct: **{question.answer}**  (review: {lesson.title})")
