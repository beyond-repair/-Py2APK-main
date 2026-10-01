"""Optional ONNX inference helper (requires py2apk[onnx])."""
from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def process_input(input_json: str, model_path: str) -> str:
    """Process input JSON through an ONNX model; return JSON output string."""
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return json.dumps({"error": "numpy not installed; pip install 'py2apk[onnx]'"})

    try:
        # Historical Android-bundled model helper (optional path)
        from py2apk.android_project.app.src.main.python.ai_model import AIModel
    except Exception:
        try:
            AIModel = _load_ai_model_class()
        except Exception as e:
            return json.dumps({"error": f"AIModel unavailable: {e}"})

    try:
        data = json.loads(input_json)
        tensor = np.array(data["input"], dtype=np.float32)
        model = AIModel(model_path)
        output = model.run_inference(tensor)
        if output is None:
            return json.dumps({"error": "inference returned None"})
        return json.dumps({"output": output.tolist()})
    except Exception as e:
        logger.error("Error processing input: %s", e)
        return json.dumps({"error": str(e)})


def _load_ai_model_class() -> Any:
    import importlib.util
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[1]
        / "android_project"
        / "app"
        / "src"
        / "main"
        / "python"
        / "ai_model.py"
    )
    if not path.exists():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location("py2apk_ai_model", path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load ai_model")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.AIModel
