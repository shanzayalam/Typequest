from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

from .models import Answer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCAL_DATA_DIR = PROJECT_ROOT / "data"


def _artifact_dir() -> Path:
    if os.environ.get("VERCEL"):
        return Path(tempfile.gettempdir()) / "typequest"
    return LOCAL_DATA_DIR


def write_persona_artifact(result: Dict[str, Any], answers: Iterable[Answer], source: str) -> Path:
    data_dir = _artifact_dir()
    persona_path = data_dir / "persona.json"
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": source,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "answers": [answer.model_dump() for answer in answers],
        "result": result,
    }
    persona_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return persona_path
