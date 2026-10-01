# Claim Status

**Repository:** beyond-repair/-Py2APK-main  
**Classification:** RUNNABLE SKETCH (Claim-0)  
**Claim level:** 0  

## Allowed statements

- Historical / repaired demo of Python→Android packaging ideas using a Chaquopy-oriented template and ONNX-era helpers.
- Runnable Python CLI: analyze, doctor, dry-run/scaffold (no Android SDK required).
- Clean-clone verified: `pip install -e ".[dev]"`, `pytest`, and `py2apk dry-run` / `analyze` / `doctor`.

## Forbidden / unsupported

- Any claim of a production APK converter or store-ready build pipeline.
- Verified APK output on hosts without Android SDK / Gradle / Chaquopy.
- Security or performance guarantees for signing, Keystore, or API key helpers.
- Endorsement of current third-party Chaquopy / ONNX versions beyond the committed snapshot.

## Repair note

Product mutation allowed for Claim-0 runnability (installable package, SDK-free CLI, honest tests/docs). Nested `-Py2APK-main/` package root preserved.
