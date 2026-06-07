"""Spaced-repetition flashcard logic (Leitner system) over the glossary terms.

Pure functions (no Streamlit) so the scheduling is easy to test. Each card lives
in a "box" 1-5; answering correctly promotes it to a higher box with a longer
interval before it is due again, while missing it resets it to box 1. State is
stored in ``progress_data["flashcards"]`` and persists via save_progress.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional

from glossary import GLOSSARY

# Days until a card is due again, by Leitner box. Higher box = seen more, longer wait.
BOX_INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
MAX_BOX = 5


def _all_terms() -> List[str]:
    return list(GLOSSARY.keys())


def get_cards(progress_data: dict) -> dict:
    cards = progress_data.get("flashcards")
    return cards if isinstance(cards, dict) else {}


def _card(progress_data: dict, term: str) -> dict:
    card = get_cards(progress_data).get(term)
    return card if isinstance(card, dict) else {}


def is_due(card: dict, today: date) -> bool:
    """A card with no schedule yet is due; otherwise due when its date has arrived."""
    if not card:
        return True
    due = card.get("due")
    if not due:
        return True
    try:
        return date.fromisoformat(str(due)) <= today
    except (TypeError, ValueError):
        return True


def is_mastered(card: dict) -> bool:
    return bool(card) and int(card.get("box", 0) or 0) >= MAX_BOX


def due_terms(progress_data: dict, terms: Optional[List[str]] = None, today: Optional[date] = None) -> List[str]:
    """Terms due for review now (including ones never studied), in glossary order."""
    today = today or date.today()
    terms = terms if terms is not None else _all_terms()
    return [term for term in terms if is_due(_card(progress_data, term), today)]


def ahead_terms(progress_data: dict, terms: Optional[List[str]] = None) -> List[str]:
    """Not-yet-mastered terms, lowest box first — for studying ahead of schedule."""
    terms = terms if terms is not None else _all_terms()
    not_mastered = [term for term in terms if not is_mastered(_card(progress_data, term))]
    return sorted(not_mastered, key=lambda term: int(_card(progress_data, term).get("box", 0) or 0))


def record_result(progress_data: dict, term: str, correct: bool, today: Optional[date] = None) -> dict:
    """Update a term's spaced-repetition state after a review. Mutates progress_data."""
    today = today or date.today()
    cards = progress_data.setdefault("flashcards", {})
    card = cards.get(term)
    if not isinstance(card, dict):
        card = {"box": 1, "seen": 0, "correct": 0}
    box = int(card.get("box", 1) or 1)
    if correct:
        box = min(box + 1, MAX_BOX)
        card["correct"] = int(card.get("correct", 0) or 0) + 1
    else:
        box = 1
    interval = BOX_INTERVALS.get(box, 1)
    card["box"] = box
    card["due"] = (today + timedelta(days=interval)).isoformat()
    card["seen"] = int(card.get("seen", 0) or 0) + 1
    card["last_reviewed"] = today.isoformat()
    cards[term] = card
    return card


def stats(progress_data: dict, terms: Optional[List[str]] = None, today: Optional[date] = None) -> dict:
    today = today or date.today()
    terms = terms if terms is not None else _all_terms()
    cards = get_cards(progress_data)
    studied = sum(1 for term in terms if isinstance(cards.get(term), dict))
    mastered = sum(1 for term in terms if is_mastered(_card(progress_data, term)))
    due = len(due_terms(progress_data, terms, today))
    return {"total": len(terms), "studied": studied, "mastered": mastered, "due": due}


def next_due_date(progress_data: dict, terms: Optional[List[str]] = None) -> Optional[str]:
    """Earliest upcoming due date among studied cards (for 'all caught up' messaging)."""
    terms = terms if terms is not None else _all_terms()
    cards = get_cards(progress_data)
    dues = [
        cards[term]["due"]
        for term in terms
        if isinstance(cards.get(term), dict) and cards[term].get("due")
    ]
    return min(dues) if dues else None
