"""Analyze Python project dependencies for Android/Chaquopy compatibility."""
from __future__ import annotations

import logging
import re
from importlib import resources
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version

logger = logging.getLogger(__name__)

# Fallback when packaged YAML is unavailable
_BUILTIN_COMPAT: Dict[str, dict] = {
    "numpy": {"min_version": "1.19.0", "max_version": "1.26.4"},
    "onnxruntime": {"min_version": "1.10.0", "max_version": "1.16.3"},
    "requests": {"min_version": "2.25.0", "max_version": "2.32.3"},
    "torch": {"max_version": "2.1.0", "note": "Heavy; often impractical in Chaquopy APKs"},
}


def _default_config_path() -> Path:
    try:
        ref = resources.files("py2apk").joinpath("data/dependency_config.yaml")
        with resources.as_file(ref) as p:
            return Path(p)
    except Exception:
        here = Path(__file__).resolve().parent / "data" / "dependency_config.yaml"
        return here


class DependencyAnalyzer:
    """Analyzes project dependencies for Android/Chaquopy-era compatibility."""

    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        path = Path(config_file) if config_file else _default_config_path()
        self.compatible_versions = self._load_compatible_versions(path)

    def _load_compatible_versions(self, config_path: Path) -> dict:
        try:
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                if isinstance(data, dict) and data:
                    return data
        except Exception as e:
            logger.warning("Failed to load dependency config %s: %s", config_path, e)
        return dict(_BUILTIN_COMPAT)

    @staticmethod
    def _extract_version(specifier: SpecifierSet) -> Optional[Version]:
        """Best-effort pin from a specifier set (e.g. ==1.2.3 or >=1.2,<2)."""
        for spec in specifier:
            if spec.operator in ("==", "===", "~="):
                try:
                    return Version(spec.version.split("*")[0].rstrip("."))
                except InvalidVersion:
                    continue
        # Prefer lower bound as proxy when no exact pin
        for spec in specifier:
            if spec.operator in (">=", ">"):
                try:
                    return Version(spec.version)
                except InvalidVersion:
                    continue
        return None

    def check_compatibility(self, requirements_path: Path) -> List[str]:
        """Return human-readable compatibility issues for a requirements file."""
        issues: List[str] = []
        path = Path(requirements_path)
        if not path.exists():
            return [f"Requirements file not found: {path}"]

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            logger.error("Dependency check failed: %s", e)
            return ["Error processing dependencies"]

        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Strip env markers for Requirement parsing of the name/spec part
            req_line = re.split(r"\s*;\s*", line, maxsplit=1)[0].strip()
            try:
                req = Requirement(req_line)
            except InvalidRequirement:
                issues.append(f"Invalid requirement format: {line}")
                continue

            name = req.name.lower()
            # normalize underscores/hyphens for lookup
            constraints = (
                self.compatible_versions.get(req.name)
                or self.compatible_versions.get(name)
                or self.compatible_versions.get(name.replace("-", "_"))
                or self.compatible_versions.get(name.replace("_", "-"))
            )
            if not constraints:
                continue

            if "note" in constraints and not req.specifier:
                issues.append(f"{req.name}: {constraints['note']}")

            pinned = self._extract_version(req.specifier) if req.specifier else None
            if pinned is None:
                continue

            if "max_version" in constraints:
                try:
                    if pinned > Version(str(constraints["max_version"])):
                        issues.append(
                            f"{req.name} {pinned} exceeds max supported "
                            f"{constraints['max_version']}"
                        )
                except InvalidVersion:
                    pass

            if "min_version" in constraints:
                try:
                    if pinned < Version(str(constraints["min_version"])):
                        issues.append(
                            f"{req.name} {pinned} requires at least "
                            f"{constraints['min_version']}"
                        )
                except InvalidVersion:
                    pass

            if "note" in constraints:
                note = f"{req.name}: {constraints['note']}"
                if note not in issues:
                    issues.append(note)

        return issues

    def summarize_project(self, project_path: Path) -> dict:
        """Lightweight project analysis for CLI dry-run/analyze."""
        project_path = Path(project_path)
        py_files = sorted(project_path.rglob("*.py")) if project_path.is_dir() else []
        req = project_path / "requirements.txt"
        pyproject = project_path / "pyproject.toml"
        issues = self.check_compatibility(req) if req.exists() else []
        return {
            "project": str(project_path.resolve()) if project_path.exists() else str(project_path),
            "exists": project_path.is_dir(),
            "python_files": len(py_files),
            "has_main_py": (project_path / "main.py").exists(),
            "has_requirements": req.exists(),
            "has_pyproject": pyproject.exists(),
            "compatibility_issues": issues,
        }
