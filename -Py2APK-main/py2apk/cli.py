"""Command-line interface for Py2APK (Claim-0)."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import click

from . import __version__
from .analyzer import DependencyAnalyzer
from .builder import APKBuilder
from .config import find_android_sdk
from .utils.system_check import SystemValidator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def _validate_project(project_path: Path, *, require_main: bool = False) -> bool:
    if not project_path.is_dir():
        logger.error("Project path is not a directory: %s", project_path)
        return False
    if require_main and not (project_path / "main.py").exists():
        logger.error("Missing required file: main.py")
        return False
    req = project_path / "requirements.txt"
    if req.exists():
        issues = DependencyAnalyzer().check_compatibility(req)
        if issues:
            logger.warning("Dependency compatibility notes:")
            for issue in issues:
                logger.warning("- %s", issue)
    return True


@click.group(invoke_without_command=True)
@click.option("--version", "show_version", is_flag=True, help="Show version and exit")
@click.pass_context
def main(ctx: click.Context, show_version: bool) -> None:
    """Py2APK — Claim-0 Python→Android packaging sketch (not a production APK converter)."""
    if show_version:
        click.echo(f"py2apk {__version__}")
        ctx.exit(0)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command("analyze")
@click.option(
    "--project",
    "project",
    required=True,
    type=click.Path(),
    help="Python project directory",
)
@click.option("--json-out", is_flag=True, help="Emit JSON summary")
def analyze_cmd(project: str, json_out: bool) -> None:
    """Analyze a Python project for packaging readiness (no SDK required)."""
    path = Path(project)
    summary = DependencyAnalyzer().summarize_project(path)
    if json_out:
        click.echo(json.dumps(summary, indent=2))
    else:
        click.echo(f"Project: {summary['project']}")
        click.echo(f"Exists: {summary['exists']}")
        click.echo(f"Python files: {summary['python_files']}")
        click.echo(f"main.py: {summary['has_main_py']}")
        click.echo(f"requirements.txt: {summary['has_requirements']}")
        click.echo(f"pyproject.toml: {summary['has_pyproject']}")
        if summary["compatibility_issues"]:
            click.echo("Compatibility notes:")
            for issue in summary["compatibility_issues"]:
                click.echo(f"  - {issue}")
        else:
            click.echo("Compatibility notes: (none)")
    if not summary["exists"]:
        sys.exit(1)


@main.command("doctor")
def doctor_cmd() -> None:
    """Report host tools / Android SDK availability."""
    sdk = find_android_sdk()
    click.echo(f"py2apk {__version__}")
    click.echo(
        f"Android SDK: {sdk if sdk else 'NOT FOUND (dry-run/scaffold still work)'}"
    )
    report = SystemValidator().report()
    for name, present in report.items():
        click.echo(f"{name}: {'ok' if present else 'missing'}")
    click.echo(
        "Note: Claim-0 does not claim a verified APK build on this host without SDK/Gradle."
    )


@main.command("dry-run")
@click.option(
    "--project",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Python project directory",
)
@click.option("--output", default="dist", show_default=True, help="Output directory for scaffold")
def dry_run_cmd(project: str, output: str) -> None:
    """Scaffold Android project tree without invoking Gradle/APK build."""
    project_path = Path(project)
    output_path = Path(output)
    if not _validate_project(project_path, require_main=False):
        sys.exit(1)
    summary = DependencyAnalyzer().summarize_project(project_path)
    click.echo(
        json.dumps(
            {k: summary[k] for k in summary if k != "compatibility_issues"},
            indent=2,
        )
    )
    builder = APKBuilder(project_path, output_path, require_sdk=False)
    if builder.create_android_project(dry_run=True):
        click.echo(f"Dry-run scaffold written to {output_path.resolve()}")
        click.echo("No APK was built (Claim-0).")
    else:
        logger.error("Dry-run scaffold failed.")
        sys.exit(1)


@main.command("scaffold")
@click.option(
    "--project",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Python project directory",
)
@click.option("--output", default="dist", show_default=True, help="Output directory")
def scaffold_cmd(project: str, output: str) -> None:
    """Create Android project scaffold (no Gradle/APK)."""
    project_path = Path(project)
    output_path = Path(output)
    if not _validate_project(project_path, require_main=False):
        sys.exit(1)
    builder = APKBuilder(project_path, output_path, require_sdk=False)
    if builder.create_android_project(dry_run=True):
        click.echo(f"Scaffold written to {output_path.resolve()}")
    else:
        sys.exit(1)


@main.command("build")
@click.option(
    "--project",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Python project directory",
)
@click.option("--output", default="dist", show_default=True, help="Output directory")
def build_cmd(project: str, output: str) -> None:
    """Attempt real APK build (requires Android SDK + Gradle wrapper)."""
    project_path = Path(project)
    output_path = Path(output)
    if not _validate_project(project_path, require_main=True):
        sys.exit(1)
    try:
        builder = APKBuilder(project_path, output_path, require_sdk=True)
    except FileNotFoundError as e:
        logger.error("%s", e)
        sys.exit(2)
    if not builder.create_android_project(dry_run=False):
        sys.exit(1)
    if builder.build_apk():
        click.echo(f"APK build reported success under {output_path}")
    else:
        logger.error("APK build failed or unsupported in this environment.")
        sys.exit(1)


@main.command("gui")
def gui_cmd() -> None:
    """Launch Tk GUI if system tkinter is available."""
    try:
        from .gui.main_window import launch_gui
    except ImportError as e:
        logger.error("GUI unavailable (install python3-tk): %s", e)
        sys.exit(1)
    launch_gui()


if __name__ == "__main__":
    main()
