import logging
import json
import numpy as np
from py2apk.android_project.app.src.main.python.ai_model import AIModel

logger = logging.getLogger(__name__)


def process_input(input_json: str, model_path: str) -> str:
    """Process input from Android and return JSON output."""
    try:
        data = json.loads(input_json)
        tensor = np.array(data["input"], dtype=np.float32)
        model = AIModel(model_path)
        output = model.run_inference(tensor)
        return json.dumps({"output": output.tolist()})
    except Exception as e:
        logger.error(f"Error processing input: {e}")
        return json.dumps({"error": str(e)})
