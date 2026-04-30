import json
from pathlib import Path

from app.mcp_server import analyze_personality


def main() -> None:
    sample_answers = [
        {"question_id": "q01", "value": 5},
        {"question_id": "q05", "value": 4},
        {"question_id": "q14", "value": 4},
        {"question_id": "q15", "value": 3},
        {"question_id": "q17", "value": 5},
        {"question_id": "q22", "value": 4},
    ]
    result = analyze_personality(answers=sample_answers)
    print("MCP tool smoke test succeeded.")
    print(json.dumps(result, indent=2))
    artifact_path = Path(__file__).resolve().parents[1] / "data" / "persona.json"
    print(f"Artifact written to: {artifact_path}")


if __name__ == "__main__":
    main()
