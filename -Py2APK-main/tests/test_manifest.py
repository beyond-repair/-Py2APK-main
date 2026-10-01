"""Manifest generator tests."""
from pathlib import Path

from py2apk.utils.manifest import AppConfig, ManifestGenerator


def test_create_manifest(tmp_path: Path):
    path = ManifestGenerator().create_manifest(tmp_path, AppConfig(package_name="com.demo.app"))
    text = path.read_text(encoding="utf-8")
    assert "com.demo.app" in text
    assert "minSdkVersion" in text
