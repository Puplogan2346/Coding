from curriculum import LESSONS
from home import build_todo_items, open_mistakes, project_rows
from progress import add_mistake_card, default_progress, mark_lesson_complete, record_quiz_score

LESSON_IDS = [lesson.id for lesson in LESSONS]


def _fresh():
    return default_progress(LESSON_IDS, profile_name="Home")


def test_new_user_todo_starts_with_mission_and_first_lesson():
    items = build_todo_items(_fresh())
    assert 1 <= len(items) <= 6
    assert "Day 1" in items[0]["label"]
    assert any(LESSONS[0].title in item["label"] for item in items)


def test_todo_includes_weak_quiz_and_caps_at_six():
    data = _fresh()
    for lesson_id in LESSON_IDS[:4]:
        mark_lesson_complete(data, lesson_id)
        record_quiz_score(data, lesson_id, 1, 3)  # all weak
    items = build_todo_items(data)
    assert len(items) <= 6
    assert any(item["label"].startswith("Pass the quiz:") for item in items)


def test_open_mistakes_newest_first_and_only_open():
    data = _fresh()
    add_mistake_card(data, "loops", "off by one", "check range end", lesson_id="04-loops")
    add_mistake_card(data, "dicts", "KeyError", "use .get", lesson_id="06-data-structures")
    data["mistake_cards"][0]["status"] = "Closed"
    cards = open_mistakes(data)
    assert len(cards) == 1
    assert cards[0]["concept"] == "dicts"


def test_project_rows_put_recommended_first():
    rows = project_rows(_fresh())
    assert rows[0]["recommended"] is True
    assert all(set(row) >= {"title", "level", "percent", "next_milestone"} for row in rows)
