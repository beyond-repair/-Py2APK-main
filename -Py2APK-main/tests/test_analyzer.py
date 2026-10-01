"""Tests for DependencyAnalyzer (no Android SDK)."""
from pathlib import Path

from py2apk.analyzer import DependencyAnalyzer


def test_missing_requirements(tmp_path: Path):
    issues = DependencyAnalyzer().check_compatibility(tmp_path / "requirements.txt")
    assert issues
    assert "not found" in issues[0].lower()


def test_compatible_pin(tmp_path: Path):
    req = tmp_path / "requirements.txt"
    req.write_text("numpy==1.23.5\nrequests==2.31.0\n", encoding="utf-8")
    issues = DependencyAnalyzer().check_compatibility(req)
    # pins within range -> no max/min violations
    assert not any("exceeds" in i or "requires at least" in i for i in issues)


def test_exceeds_max(tmp_path: Path):
    req = tmp_path / "requirements.txt"
    req.write_text("numpy==2.0.0\n", encoding="utf-8")
    issues = DependencyAnalyzer().check_compatibility(req)
    assert any("exceeds" in i for i in issues)


def test_invalid_requirement(tmp_path: Path):
    req = tmp_path / "requirements.txt"
    req.write_text("===not-a-requirement\n", encoding="utf-8")
    issues = DependencyAnalyzer().check_compatibility(req)
    assert any("Invalid" in i for i in issues)


def test_summarize_project(tmp_path: Path):
    (tmp_path / "main.py").write_text("print('hi')\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")
    summary = DependencyAnalyzer().summarize_project(tmp_path)
    assert summary["exists"] is True
    assert summary["has_main_py"] is True
    assert summary["python_files"] >= 1
