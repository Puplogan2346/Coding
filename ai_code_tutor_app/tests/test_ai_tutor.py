from ai_tutor import _sanitize_messages


def test_sanitize_messages_limits_and_filters_content():
    messages = [{"role": "system", "content": ""}]
    messages += [{"role": "user", "content": f"message {index}"} for index in range(20)]
    sanitized = _sanitize_messages(messages)
    assert len(sanitized) == 12
    assert sanitized[0]["content"] == "message 8"
    assert all(item["role"] in {"user", "assistant", "developer"} for item in sanitized)
