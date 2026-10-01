"""CLI smoke tests via click CliRunner."""
from pathlib import Path

from click.testing import CliRunner

from py2apk.cli import main


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Claim-0" in result.output or "analyze" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "py2apk" in result.output


def test_doctor():
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert result.exit_code == 0
    assert "Android SDK" in result.output


def test_analyze_and_dry_run(tmp_path: Path):
    proj = tmp_path / "demo"
    proj.mkdir()
    (proj / "main.py").write_text("def main():\n    return 1\n", encoding="utf-8")
    (proj / "requirements.txt").write_text("numpy==1.23.5\n", encoding="utf-8")
    out = tmp_path / "out"

    runner = CliRunner()
    a = runner.invoke(main, ["analyze", "--project", str(proj)])
    assert a.exit_code == 0
    assert "Python files" in a.output

    d = runner.invoke(main, ["dry-run", "--project", str(proj), "--output", str(out)])
    assert d.exit_code == 0
    assert (out / "DRY_RUN.txt").exists()
    assert (out / "build.gradle").exists()
    assert (out / "app" / "src" / "main" / "AndroidManifest.xml").exists()
