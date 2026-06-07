from focus_coach import (
    ADHD_DESIGN_PRINCIPLES,
    ENERGY_LEVELS,
    body_double_script,
    focus_blocks,
    focus_checkin_score,
    recommended_focus_mode,
    total_focus_minutes,
)


def test_focus_blocks_offer_adhd_friendly_timeboxes():
    assert "Low" in ENERGY_LEVELS
    standard = focus_blocks(30, "Medium")
    assert total_focus_minutes(standard) == 30
    assert any(block.label == "Brain dump" for block in standard)
    assert any("Tiny start" == block.label for block in standard)
    assert all(block.minutes <= 10 for block in standard)


def test_rescue_mode_protects_low_energy_days():
    low_mode = recommended_focus_mode("Low", 30)
    assert low_mode.id == "rescue_10"
    low_blocks = focus_blocks(low_mode.minutes, "Low")
    assert total_focus_minutes(low_blocks) == 10
    assert low_blocks[0].label == "Open the app"


def test_high_energy_can_use_deep_build_when_time_exists():
    mode = recommended_focus_mode("High", 45)
    assert mode.id == "deep_45"
    assert total_focus_minutes(focus_blocks(mode.minutes, "High")) == 45


def test_body_double_script_and_principles_are_kind_not_pressure_based():
    script = body_double_script("Variables are labels")
    joined = " ".join(script)
    assert "Variables are labels" in joined
    assert "next tiny action" in joined
    assert len(ADHD_DESIGN_PRINCIPLES) >= 6
    assert any("shame-free" in principle.lower() for principle in ADHD_DESIGN_PRINCIPLES)


def test_focus_checkin_score_is_bounded():
    assert focus_checkin_score("Low", "Scattered") == 2
    assert focus_checkin_score("Medium", "Warming up") == 4
    assert focus_checkin_score("High", "Locked in") == 6
    assert focus_checkin_score("unknown", "unknown") == 4
