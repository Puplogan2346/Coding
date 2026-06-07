from __future__ import annotations

from private_access import private_access_status, private_badge_text, verify_passcode


def test_private_access_optional_when_unconfigured():
    status = private_access_status(env={}, secrets={})
    assert status.required is False
    assert status.configured is False
    assert private_badge_text(status) == "Local private mode"


def test_private_access_requires_passcode_when_configured():
    status = private_access_status(env={"APP_PRIVATE_PASSCODE": "secret"}, secrets={})
    assert status.required is True
    assert status.configured is True
    assert status.passcode_source == "APP_PRIVATE_PASSCODE"
    assert verify_passcode("secret", "secret") is True
    assert verify_passcode("wrong", "secret") is False


def test_private_mode_requested_without_passcode_needs_setup():
    status = private_access_status(env={"APP_PRIVATE_MODE": "true"}, secrets={})
    assert status.required is True
    assert status.configured is False
    assert private_badge_text(status) == "Private setup needed"
