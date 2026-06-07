from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class PrivateAccessStatus:
    """Runtime private-access state for a single-user Streamlit app."""

    required: bool
    configured: bool
    passcode_source: str = ""
    mode: str = "off"

    @property
    def private_mode(self) -> bool:
        return self.required

    @property
    def source(self) -> str:
        return self.passcode_source or "not configured"


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _safe_secret_get(secrets: Mapping[str, Any] | Any | None, key: str) -> str:
    if not secrets:
        return ""
    try:
        value = secrets.get(key, "")  # type: ignore[attr-defined]
    except Exception:
        try:
            value = secrets[key]  # type: ignore[index]
        except Exception:
            value = ""
    return str(value or "").strip()


def hash_passcode(passcode: str) -> str:
    return hashlib.sha256(str(passcode or "").encode("utf-8")).hexdigest()


def configured_passcode(
    env: Mapping[str, str] | None = None,
    secrets: Mapping[str, Any] | Any | None = None,
) -> tuple[str, str]:
    """Return the configured private passcode/hash and its source.

    Supported settings, in priority order:
    - APP_PRIVATE_PASSCODE_HASH
    - APP_PRIVATE_PASSCODE
    - APP_ACCESS_CODE_HASH
    - APP_ACCESS_CODE

    The APP_ACCESS_CODE names are accepted for backwards compatibility with
    earlier private-product builds.
    """
    source_env = env if env is not None else os.environ
    candidates = (
        ("APP_PRIVATE_PASSCODE_HASH", str(source_env.get("APP_PRIVATE_PASSCODE_HASH", "") or "").strip()),
        ("Streamlit secrets APP_PRIVATE_PASSCODE_HASH", _safe_secret_get(secrets, "APP_PRIVATE_PASSCODE_HASH")),
        ("APP_PRIVATE_PASSCODE", str(source_env.get("APP_PRIVATE_PASSCODE", "") or "").strip()),
        ("Streamlit secrets APP_PRIVATE_PASSCODE", _safe_secret_get(secrets, "APP_PRIVATE_PASSCODE")),
        ("APP_ACCESS_CODE_HASH", str(source_env.get("APP_ACCESS_CODE_HASH", "") or "").strip()),
        ("Streamlit secrets APP_ACCESS_CODE_HASH", _safe_secret_get(secrets, "APP_ACCESS_CODE_HASH")),
        ("APP_ACCESS_CODE", str(source_env.get("APP_ACCESS_CODE", "") or "").strip()),
        ("Streamlit secrets APP_ACCESS_CODE", _safe_secret_get(secrets, "APP_ACCESS_CODE")),
    )
    for source, value in candidates:
        if value:
            return value, source
    return "", ""


def private_access_status(
    env: Mapping[str, str] | None = None,
    secrets: Mapping[str, Any] | Any | None = None,
) -> PrivateAccessStatus:
    source_env = env if env is not None else os.environ
    passcode, source = configured_passcode(source_env, secrets)
    explicitly_private = _truthy(str(source_env.get("APP_PRIVATE_MODE", "") or ""))
    if passcode:
        return PrivateAccessStatus(True, True, source, mode="hash" if source.endswith("HASH") or "HASH" in source else "plain")
    if explicitly_private:
        return PrivateAccessStatus(True, False, "", mode="missing")
    return PrivateAccessStatus(False, False, "", mode="off")


def verify_passcode(candidate: str, configured: str) -> bool:
    """Verify a candidate against a plain passcode or a SHA-256 hex digest."""
    cleaned = str(candidate or "").strip()
    expected = str(configured or "").strip()
    if not cleaned or not expected:
        return False
    looks_hash = len(expected) == 64 and all(char in "0123456789abcdefABCDEF" for char in expected)
    if looks_hash:
        return hmac.compare_digest(hash_passcode(cleaned), expected.lower())
    return hmac.compare_digest(cleaned, expected)


def private_badge_text(status: PrivateAccessStatus, unlocked: bool = False) -> str:
    if not status.required:
        return "Local private mode"
    if not status.configured:
        return "Private setup needed"
    return "Private app unlocked" if unlocked else "Private app locked"


def access_setup_hint(status: PrivateAccessStatus | None = None) -> str:
    status = status or private_access_status()
    if status.configured:
        return f"Private gate will require a passcode from {status.passcode_source}."
    if status.required:
        return "APP_PRIVATE_MODE is on, but no APP_PRIVATE_PASSCODE or APP_PRIVATE_PASSCODE_HASH is configured."
    return "Set APP_PRIVATE_PASSCODE or APP_PRIVATE_PASSCODE_HASH to require a private code before the app opens."


# Compatibility helpers used by newer standalone checks.
def access_status(*_args: Any, **_kwargs: Any) -> PrivateAccessStatus:
    return private_access_status()


def redacted_access_summary(status: PrivateAccessStatus) -> str:
    return access_setup_hint(status)


@dataclass(frozen=True)
class PrivateAccessConfig:
    """Backwards-compatible private access-code config for standalone checks."""

    enabled: bool
    mode: str = "off"
    value: str = ""
    source: str = "not configured"

    @property
    def label(self) -> str:
        if not self.enabled:
            return "Private access code not configured"
        if self.mode == "hash":
            return f"Private gate enabled with hashed access code via {self.source}"
        return f"Private gate enabled via {self.source}"


def hash_access_code(access_code: str) -> str:
    return hash_passcode(access_code)


def private_access_config(
    env: Mapping[str, str] | None = None,
    secrets: Mapping[str, Any] | Any | None = None,
) -> PrivateAccessConfig:
    source_env = env if env is not None else os.environ
    env_hash = str(source_env.get("APP_ACCESS_CODE_HASH", "") or "").strip()
    secret_hash = _safe_secret_get(secrets, "APP_ACCESS_CODE_HASH")
    env_private_hash = str(source_env.get("APP_PRIVATE_PASSCODE_HASH", "") or "").strip()
    secret_private_hash = _safe_secret_get(secrets, "APP_PRIVATE_PASSCODE_HASH")
    env_code = str(source_env.get("APP_ACCESS_CODE", "") or "").strip()
    secret_code = _safe_secret_get(secrets, "APP_ACCESS_CODE")
    env_private_code = str(source_env.get("APP_PRIVATE_PASSCODE", "") or "").strip()
    secret_private_code = _safe_secret_get(secrets, "APP_PRIVATE_PASSCODE")

    if env_private_hash:
        return PrivateAccessConfig(True, "hash", env_private_hash, "environment APP_PRIVATE_PASSCODE_HASH")
    if secret_private_hash:
        return PrivateAccessConfig(True, "hash", secret_private_hash, "Streamlit secrets APP_PRIVATE_PASSCODE_HASH")
    if env_hash:
        return PrivateAccessConfig(True, "hash", env_hash, "environment APP_ACCESS_CODE_HASH")
    if secret_hash:
        return PrivateAccessConfig(True, "hash", secret_hash, "Streamlit secrets APP_ACCESS_CODE_HASH")
    if env_private_code:
        return PrivateAccessConfig(True, "plain", env_private_code, "environment APP_PRIVATE_PASSCODE")
    if secret_private_code:
        return PrivateAccessConfig(True, "plain", secret_private_code, "Streamlit secrets APP_PRIVATE_PASSCODE")
    if env_code:
        return PrivateAccessConfig(True, "plain", env_code, "environment APP_ACCESS_CODE")
    if secret_code:
        return PrivateAccessConfig(True, "plain", secret_code, "Streamlit secrets APP_ACCESS_CODE")
    return PrivateAccessConfig(False)


def verify_access_code(candidate: str, config: PrivateAccessConfig) -> bool:
    if not config.enabled:
        return True
    if config.mode == "hash":
        return hmac.compare_digest(hash_access_code(candidate), config.value.lower())
    return verify_passcode(candidate, config.value)
