<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║   ATOMIC DREAM LABS  ·  BEYOND-REPAIR                        ║
╚══════════════════════════════════════════════════════════════╝
```

# Py2APK

### Claim-0 Python→Android packaging sketch (Chaquopy / ONNX-era experiment)

[![Lifecycle](https://img.shields.io/badge/●_ACTIVE_SKETCH-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_0-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

```
LIFECYCLE   RUNNABLE SKETCH (Claim-0)
CLAIM       0
NOT CLAIMED production APK converter · verified store build · profit
```

</div>

---

## CI

GitHub Actions workflow `pytest` installs the nested package and runs `pytest -q`.
A green run is an Actions conclusion for the SDK-free suite only.
It is not evidence of an APK build, store signing, or Chaquopy compatibility.

## Status

**RUNNABLE SKETCH — NOT A COMPLETE PRODUCT.**

This repository preserves a 2025-era experiment: package Python (often ONNX) into an Android app via Chaquopy-oriented scaffolding. On typical Linux boxes **without** Android SDK / Gradle / Chaquopy, a stranger can still:

1. Install the `py2apk` CLI
2. Analyze a Python project for dependency notes
3. Dry-run / scaffold an Android project tree from the bundled template
4. Run the pytest suite (no SDK required)

A **real APK** is **not** verified here. Use Android Studio + Chaquopy for that path.

---

## Layout (nested source preserved)

Installable package root lives one level down (historical zip nest):

```
-Py2APK-main/                 ← repo root (this README)
└── -Py2APK-main/             ← package root (awkward nest; preserved)
    ├── pyproject.toml
    ├── py2apk/               ← analyzer, builder, cli, config, signing, gui, utils
    │   └── android_project/  ← historical Java/Python Chaquopy sketch
    └── tests/                ← SDK-free pytest suite
```

---

## Quick start (stranger clone)

```bash
git clone https://github.com/beyond-repair/-Py2APK-main.git
cd -- -Py2APK-main/-Py2APK-main
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
py2apk --help
py2apk doctor
pytest -q
```

Demo against a tiny sample project:

```bash
mkdir -p /tmp/py2apk-demo && printf 'print("hi")\n' > /tmp/py2apk-demo/main.py
printf 'numpy==1.23.5\n' > /tmp/py2apk-demo/requirements.txt
py2apk analyze --project /tmp/py2apk-demo
py2apk dry-run --project /tmp/py2apk-demo --output /tmp/py2apk-out
ls /tmp/py2apk-out/DRY_RUN.txt /tmp/py2apk-out/app/src/main/python/main.py
```

Optional ONNX helpers (not required for CLI/tests):

```bash
pip install -e ".[onnx]"
```

Optional GUI (`py2apk gui`) needs system `python3-tk` (not available via pip alone).

---

## CLI

| Command | Purpose |
| --- | --- |
| `py2apk analyze --project PATH` | Dependency / structure summary |
| `py2apk dry-run --project PATH --output DIR` | Scaffold Android tree; **no** APK |
| `py2apk scaffold ...` | Same scaffold path |
| `py2apk doctor` | Report SDK / gradle / adb / apksigner |
| `py2apk build ...` | Attempt Gradle APK (needs SDK + gradlew; usually fails here) |
| `py2apk gui` | Tk UI if tkinter present |

---

## Not claimed

- Production-ready Python→APK converter
- Verified Chaquopy/ONNX APK build on this host
- Security of signing placeholders or API key helpers
- Maintained parity with current Chaquopy releases

See [CLAIM_STATUS.md](CLAIM_STATUS.md) and [ARCHIVED.md](ARCHIVED.md) (historical archive note; sketch repaired for Claim-0 runnability).

---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

**William (Brian) Ware** · [Atomic Dream Labs](https://github.com/beyond-repair)

</div>
