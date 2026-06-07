from datetime import date, timedelta

from curriculum import LESSONS
from gamification import calculate_xp, earned_badges, level_for_xp
from progress import (
    completed_daily_missions_count,
    default_progress,
    mark_lesson_complete,
    record_daily_mission,
    record_official_ai_resource,
    record_prompt_score,
    record_quiz_score,
)
from study_plan import (
    DAILY_PLAN,
    completed_mission_days,
    mission_by_day,
    next_mission,
    next_mission_day,
    plan_completion_percent,
    resolved_mission_days,
    review_queue,
    total_plan_minutes,
)


def test_daily_plan_is_30_days_and_30_minutes_each():
    lesson_ids = {lesson.id for lesson in LESSONS}
    assert len(DAILY_PLAN) == 30
    assert total_plan_minutes() == 900
    assert [mission.day for mission in DAILY_PLAN] == list(range(1, 31))
    for mission in DAILY_PLAN:
        assert mission.total_minutes == 30
        assert mission.title
        assert mission.fun_challenge
        assert mission.proof
        if mission.lesson_id is not None:
            assert mission.lesson_id in lesson_ids
        assert set(mission.review_lesson_ids).issubset(lesson_ids)


def test_next_mission_advances_and_skipped_days_do_not_count_as_completed():
    progress = default_progress([lesson.id for lesson in LESSONS], profile_name="Ava")
    assert next_mission_day(progress) == 1
    assert next_mission(progress).day == 1

    record_daily_mission(progress, 1, status="Completed", session_date=date(2026, 1, 1))
    assert completed_mission_days(progress) == {1}
    assert resolved_mission_days(progress) == {1}
    assert next_mission_day(progress) == 2

    record_daily_mission(progress, 2, status="Skipped", session_date=date(2026, 1, 2))
    assert completed_daily_missions_count(progress) == 1
    assert completed_mission_days(progress) == {1}
    assert resolved_mission_days(progress) == {1, 2}
    assert next_mission_day(progress) == 3


def test_daily_streak_updates_idempotently_and_resets_after_gap():
    progress = default_progress(["one"], profile_name="Ava")
    record_daily_mission(progress, 1, session_date=date(2026, 1, 1))
    assert progress["study_streak"] == 1
    assert progress["longest_streak"] == 1

    record_daily_mission(progress, 1, session_date=date(2026, 1, 1))
    assert progress["study_streak"] == 1

    record_daily_mission(progress, 2, session_date=date(2026, 1, 2))
    assert progress["study_streak"] == 2
    assert progress["longest_streak"] == 2

    record_daily_mission(progress, 3, session_date=date(2026, 1, 4))
    assert progress["study_streak"] == 1
    assert progress["longest_streak"] == 2


def test_review_queue_uses_mission_reviews_then_recent_lessons():
    lesson_ids = [lesson.id for lesson in LESSONS]
    progress = default_progress(lesson_ids, profile_name="Ava")
    record_daily_mission(progress, 1, status="Completed")
    record_daily_mission(progress, 2, status="Completed")
    queue = review_queue(progress, lesson_ids)
    assert queue[:2] == ["01-python-mindset", "02-variables-types"]

    mark_lesson_complete(progress, lesson_ids[4])
    mark_lesson_complete(progress, lesson_ids[5])
    assert lesson_ids[5] in review_queue(progress, lesson_ids, limit=3)


def test_xp_levels_and_badges_grow_with_real_actions():
    lesson_ids = [lesson.id for lesson in LESSONS]
    progress = default_progress(lesson_ids, profile_name="Ava")
    assert calculate_xp(progress) == 0
    assert level_for_xp(0) == "Level 1 - New Coder"
    assert earned_badges(progress, len(LESSONS)) == []

    mark_lesson_complete(progress, lesson_ids[0])
    record_quiz_score(progress, lesson_ids[0], score=3, total=3)
    record_prompt_score(progress, 9, "Role: tutor. Task: explain code. Context: beginner. Constraints: no answer. Output format: steps. Verification: test me.")
    record_official_ai_resource(progress, "gumloop_ai_fundamentals", "Queued")
    for day in range(1, 8):
        record_daily_mission(progress, day, status="Completed", session_date=date(2026, 1, 1) + timedelta(days=day - 1))

    badge_ids = {badge.id for badge in earned_badges(progress, len(LESSONS))}
    assert {"first_step", "quiz_starter", "prompt_builder", "week_one", "ai_track"}.issubset(badge_ids)
    assert calculate_xp(progress) > 200
    assert plan_completion_percent(progress) == 0.233


def test_mission_by_day_validates_bounds():
    assert mission_by_day(30).day == 30
    try:
        mission_by_day(31)
    except ValueError as exc:
        assert "between 1 and 30" in str(exc)
    else:
        raise AssertionError("mission_by_day should reject out-of-range days")
