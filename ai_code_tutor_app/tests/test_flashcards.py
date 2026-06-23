from datetime import date, timedelta

from curriculum import LESSONS
from flashcards import (
    BOX_INTERVALS,
    MAX_BOX,
    ahead_terms,
    due_terms,
    is_due,
    is_mastered,
    next_due_date,
    record_result,
    stats,
)
from glossary import GLOSSARY
from progress import default_progress, normalize_progress_data

TODAY = date(2026, 6, 6)
TERM = next(iter(GLOSSARY))
SECOND_TERM = list(GLOSSARY)[1]
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


def test_next_due_date_none_until_studied_then_earliest():
    assert next_due_date({}) is None
    data = {}
    record_result(data, TERM, True, today=TODAY)          # due in 2 days (box 2)
    record_result(data, SECOND_TERM, False, today=TODAY)  # due in 1 day (box 1)
    earliest = (TODAY + timedelta(days=BOX_INTERVALS[1])).isoformat()
    assert next_due_date(data) == earliest


def test_is_due_handles_missing_and_malformed_dates():
    assert is_due({}, TODAY) is True                       # never scheduled
    assert is_due({"due": "not-a-date"}, TODAY) is True    # junk parses as due
    assert is_due({"due": (TODAY + timedelta(days=3)).isoformat()}, TODAY) is False


def test_record_result_heals_a_corrupt_card():
    data = {"flashcards": {TERM: "corrupted-not-a-dict"}}
    card = record_result(data, TERM, True, today=TODAY)
    assert card["box"] == 2 and card["seen"] == 1 and card["correct"] == 1


def test_box_five_is_the_mastery_cap_with_16_day_interval():
    data = {}
    for _ in range(6):  # 1->2->3->4->5->5 (capped)
        card = record_result(data, TERM, True, today=TODAY)
    assert card["box"] == MAX_BOX == 5
    assert card["due"] == (TODAY + timedelta(days=BOX_INTERVALS[5])).isoformat()
    assert BOX_INTERVALS[5] == 16
    assert is_mastered(card) is True
