from gamification import level_for_xp, level_progress_percent, xp_to_next_level


def test_level_progress_and_next_xp_are_stable():
    assert level_for_xp(0) == "Level 1 - New Coder"
    assert xp_to_next_level(0) == 150
    assert level_progress_percent(75) == 0.5
    assert level_for_xp(150) == "Level 2 - Habit Builder"
    assert xp_to_next_level(150) == 300
    assert level_progress_percent(2100) == 1.0
    assert xp_to_next_level(2100) == 0

from gamification import calculate_xp, earned_badges
from progress import add_mistake_card, default_progress, record_gym_session


def test_daily_gym_and_mistake_cards_add_xp_and_badges():
    data = default_progress(["one"], profile_name="Ava")
    record_gym_session(data, 1, "30 min daily", "Saved", "proof", lesson_id="one", step_state={"warmup": True})
    assert add_mistake_card(data, "syntax", "forgot colon", "use colon", lesson_id="one")

    badge_ids = {badge.id for badge in earned_badges(data, total_lessons=1)}
    assert "daily_gym" in badge_ids
    assert "mistake_mapper" in badge_ids
    assert calculate_xp(data) == 20
