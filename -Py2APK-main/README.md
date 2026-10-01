# Py2APK (package root)

> **Claim-0 runnable sketch.** Nested under the GitHub repo root as `-Py2APK-main/` (preserved historical layout).  
> Root docs: [../README.md](../README.md) · [../CLAIM_STATUS.md](../CLAIM_STATUS.md)

## Install

```bash
cd -- -Py2APK-main   # this directory (inside the cloned repo)
pip install -e ".[dev]"
py2apk --help
pytest -q
```

## What works without Android SDK

- `py2apk analyze` / `doctor` / `dry-run` / `scaffold`
- pytest suite under `tests/`

## What does not

- Verified `assembleRelease` APK on a headless box without Android Studio, SDK, and a complete Gradle wrapper/Chaquopy classpath.

The bundled `py2apk/android_project/` tree is a **historical Chaquopy/ONNX sketch** (Java bridge + Python `ai_model.py`). Dry-run copies it into your output directory for further work in Android Studio.

## License

MIT — see [LICENSE](LICENSE).
