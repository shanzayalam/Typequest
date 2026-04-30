from mcp.server.fastmcp import FastMCP

from .analysis import analyze_answers
from .artifacts import write_persona_artifact
from .models import Answer


mcp = FastMCP("TypeQuest-MBTI")


@mcp.tool()
def analyze_personality(raw_scores: dict | None = None, answers: list[dict] | None = None) -> dict:
    """
    Analyze MBTI cognitive function data and return a structured profile.
    Accepts either a list of answer objects or raw function scores.
    """
    if answers:
        parsed_answers = [Answer(**answer) for answer in answers]
        result = analyze_answers(parsed_answers).model_dump()
        write_persona_artifact(result, parsed_answers, source="mcp")
        return result

    raw_scores = raw_scores or {}
    synthetic_question_map = {"Ni": "q01", "Ne": "q02", "Si": "q03", "Se": "q04", "Ti": "q05", "Te": "q06", "Fi": "q07", "Fe": "q08"}
    normalized_answers = []
    for function_name, question_id in synthetic_question_map.items():
        value = raw_scores.get(function_name, 0)
        scaled_value = max(1, min(5, int(round((value / 25) + 3))))
        normalized_answers.append(Answer(question_id=question_id, value=scaled_value))
    result = analyze_answers(normalized_answers).model_dump()
    write_persona_artifact(result, normalized_answers, source="mcp")
    return result


if __name__ == "__main__":
    mcp.run()
