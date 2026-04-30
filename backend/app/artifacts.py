from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

from .models import Answer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PERSONA_PATH = DATA_DIR / "persona.json"


def write_persona_artifact(result: Dict[str, Any], answers: Iterable[Answer], source: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": source,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "answers": [answer.model_dump() for answer in answers],
        "result": result,
    }
    PERSONA_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return PERSONA_PATH
