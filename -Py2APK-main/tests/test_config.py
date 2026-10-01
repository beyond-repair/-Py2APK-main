"""Tests for config helpers."""
from py2apk.config import DEFAULT_CONFIG, android_sdk_candidates, find_android_sdk


def test_default_config_keys():
    assert "COMPILE_SDK" in DEFAULT_CONFIG
    assert DEFAULT_CONFIG["MIN_SDK"] == 21


def test_sdk_candidates_nonempty():
    assert len(android_sdk_candidates()) >= 1


def test_find_android_sdk_optional():
    # On this CI/box, SDK may be absent — must not raise
    result = find_android_sdk()
    assert result is None or result.exists()
