"""Builder scaffold tests (no SDK / no Gradle)."""
from pathlib import Path

from py2apk.builder import APKBuilder


def test_scaffold_copies_template(tmp_path: Path):
    proj = tmp_path / "srcproj"
    proj.mkdir()
    (proj / "hello.py").write_text("x = 1\n", encoding="utf-8")
    out = tmp_path / "android_out"
    builder = APKBuilder(proj, out, require_sdk=False)
    assert builder.create_android_project(dry_run=True) is True
    assert (out / "DRY_RUN.txt").is_file()
    assert (out / "app" / "src" / "main" / "python" / "hello.py").is_file()
    # Historical Java bridge should be present from template
    java = list((out / "app").rglob("PythonBridge.java"))
    assert java, "expected PythonBridge.java from bundled template"


def test_build_apk_without_sdk(tmp_path: Path):
    proj = tmp_path / "p"
    proj.mkdir()
    (proj / "main.py").write_text("pass\n", encoding="utf-8")
    out = tmp_path / "o"
    builder = APKBuilder(proj, out, require_sdk=False)
    builder.create_android_project(dry_run=True)
    # Without SDK, build_apk must fail honestly
    if builder.android_sdk is None:
        assert builder.build_apk() is False
