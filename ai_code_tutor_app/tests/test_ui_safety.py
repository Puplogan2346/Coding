from ui_safety import safe_html_text, truncate_text


def test_safe_html_text_escapes_learner_entered_html():
    payload = "<img src=x onerror=alert(1)> & 'quote'"
    escaped = safe_html_text(payload)
    assert "<img" not in escaped
    assert "onerror" in escaped  # preserved as text, not as an executable attribute
    assert "&lt;img" in escaped
    assert "&#x27;quote&#x27;" in escaped


def test_truncate_text_keeps_short_text_and_marks_long_text():
    assert truncate_text("hello", 10) == "hello"
    assert truncate_text("abcdefghij", 5) == "abcd…"
