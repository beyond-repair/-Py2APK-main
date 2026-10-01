"""Host environment checks for Android packaging tools."""
from __future__ import annotations

import logging
import shutil
from typing import Dict, List

logger = logging.getLogger(__name__)


class SystemValidator:
    REQUIRED_COMMANDS = ["gradle", "apksigner", "adb"]

    def report(self) -> Dict[str, bool]:
        """Return presence map for known tools (never raises)."""
        return {cmd: shutil.which(cmd) is not None for cmd in self.REQUIRED_COMMANDS}

    def missing(self) -> List[str]:
        return [cmd for cmd, ok in self.report().items() if not ok]

    def validate_environment(self) -> bool:
        """Check if required system tools are installed."""
        missing = self.missing()
        if missing:
            logger.error("Missing required system tools: %s", ", ".join(missing))
            return False
        return True
