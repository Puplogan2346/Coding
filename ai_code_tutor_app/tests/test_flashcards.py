from datetime import date, timedelta

from curriculum import LESSONS
from flashcards import (
    BOX_INTERVALS,
    ahead_terms,
    due_terms,
    record_result,
    stats,
)
from glossary import GLOSSARY
from progress import default_progress, normalize_progress_data

TODAY = date(2026, 6, 6)
TERM = next(iter(GLOSSARY))
LESSON_IDS = [lesson.id for lesson in LESSONS]


def test_new_terms_are_all_due():
    assert len(due_terms({}, today=TODAY)) == len(GLOSSARY)


def test_correct_answer_promotes_box_and_pushes_due_date():
    data = {}
    card = record_result(data, TERM, True, today=TODAY)
    assert card["box"] == 2
    assert card["due"] == (TODAY + timedelta(days=BOX_INTERVALS[2])).isoformat()
    assert card["seen"] == 1 and card["correct"] == 1
    assert TERM not in due_terms(data, today=TODAY)  # no longer due today


def test_card_becomes_due_again_after_its_interval():
    data = {}
    record_result(data, TERM, True, today=TODAY)  # due in 2 days
    assert TERM in due_terms(data, today=TODAY + timedelta(days=2))


def test_wrong_answer_resets_to_box_one():
    data = {}
    record_result(data, TERM, True, today=TODAY)  # box 2
    record_result(data, TERM, True, today=TODAY)  # box 3
    card = record_result(data, TERM, False, today=TODAY)
    assert card["box"] == 1
    assert card["due"] == (TODAY + timedelta(days=BOX_INTERVALS[1])).isoformat()


def test_five_correct_masters_the_card():
    data = {}
    for _ in range(5):
        record_result(data, TERM, True, today=TODAY)
    snapshot = stats(data, today=TODAY)
    assert snapshot["mastered"] >= 1
    assert snapshot["studied"] >= 1
    assert TERM not in ahead_terms(data)  # mastered cards drop out of "study ahead"


def test_flashcards_persist_through_normalize():
    data = default_progress(LESSON_IDS)
    record_result(data, TERM, True, today=TODAY)
    restored = normalize_progress_data(data, LESSON_IDS)
    assert TERM in restored["flashcards"]
    assert restored["flashcards"][TERM]["box"] == 2
