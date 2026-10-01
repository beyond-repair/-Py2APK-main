"""Configuration settings and constants."""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

DEFAULT_CONFIG = {
    "ANDROID_SDK_PATHS": [
        os.getenv("ANDROID_HOME"),
        os.getenv("ANDROID_SDK_ROOT"),
        str(Path.home() / "Android/Sdk"),
        "/usr/local/android-sdk",
        "/opt/android-sdk",
        "/Applications/Android Studio.app/Contents/Resources/sdk",
        r"C:\Program Files\Android\Android Studio\Sdk",
    ],
    "REQUIRED_PYTHON_PACKAGES": [
        "numpy",
        "onnxruntime",
    ],
    "MAX_APK_SIZE_MB": 150,
    "GRADLE_VERSION": "7.4",
    "PYTHON_VERSION": "3.8",
    "COMPILE_SDK": 34,
    "MIN_SDK": 21,
    "TARGET_SDK": 34,
    "APPLICATION_ID": "com.example.py2apk",
}


def android_sdk_candidates() -> List[Path]:
    """Return configured SDK path candidates (existing or not)."""
    out: List[Path] = []
    for path in DEFAULT_CONFIG["ANDROID_SDK_PATHS"]:
        if path:
            out.append(Path(path))
    return out


def find_android_sdk() -> Optional[Path]:
    """Locate Android SDK if present; return None when missing."""
    for path in android_sdk_candidates():
        if path.exists():
            return path
    return None


def require_android_sdk() -> Path:
    """Locate Android SDK or raise FileNotFoundError."""
    found = find_android_sdk()
    if found is None:
        raise FileNotFoundError(
            "Android SDK not found. Install Android Studio / set ANDROID_HOME, "
            "or use `py2apk dry-run` / `py2apk scaffold` (Claim-0; no APK build)."
        )
    return found
