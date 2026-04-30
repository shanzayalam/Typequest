from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from app.models import AnalysisResult, Answer, Question
from app.quiz_data import BASE_QUESTION_IDS, QUESTION_BANK


FUNCTIONS = ["Ni", "Ne", "Si", "Se", "Ti", "Te", "Fi", "Fe"]
QUESTION_LOOKUP = {question.id: question for question in QUESTION_BANK}

TYPE_STACKS = {
    "INTJ": ["Ni", "Te", "Fi", "Se"], "INFJ": ["Ni", "Fe", "Ti", "Se"], "ENTJ": ["Te", "Ni", "Se", "Fi"], "ENFJ": ["Fe", "Ni", "Se", "Ti"],
    "INTP": ["Ti", "Ne", "Si", "Fe"], "INFP": ["Fi", "Ne", "Si", "Te"], "ENTP": ["Ne", "Ti", "Fe", "Si"], "ENFP": ["Ne", "Fi", "Te", "Si"],
    "ISTJ": ["Si", "Te", "Fi", "Ne"], "ISFJ": ["Si", "Fe", "Ti", "Ne"], "ESTJ": ["Te", "Si", "Ne", "Fi"], "ESFJ": ["Fe", "Si", "Ne", "Ti"],
    "ISTP": ["Ti", "Se", "Ni", "Fe"], "ISFP": ["Fi", "Se", "Ni", "Te"], "ESTP": ["Se", "Ti", "Fe", "Ni"], "ESFP": ["Se", "Fi", "Te", "Ni"],
}

TYPE_FULL_NAMES = {
    "INTJ": "Introverted, Intuitive, Thinking, Judging",
    "INFJ": "Introverted, Intuitive, Feeling, Judging",
    "ENTJ": "Extraverted, Intuitive, Thinking, Judging",
    "ENFJ": "Extraverted, Intuitive, Feeling, Judging",
    "INTP": "Introverted, Intuitive, Thinking, Perceiving",
    "INFP": "Introverted, Intuitive, Feeling, Perceiving",
    "ENTP": "Extraverted, Intuitive, Thinking, Perceiving",
    "ENFP": "Extraverted, Intuitive, Feeling, Perceiving",
    "ISTJ": "Introverted, Sensing, Thinking, Judging",
    "ISFJ": "Introverted, Sensing, Feeling, Judging",
    "ESTJ": "Extraverted, Sensing, Thinking, Judging",
    "ESFJ": "Extraverted, Sensing, Feeling, Judging",
    "ISTP": "Introverted, Sensing, Thinking, Perceiving",
    "ISFP": "Introverted, Sensing, Feeling, Perceiving",
    "ESTP": "Extraverted, Sensing, Thinking, Perceiving",
    "ESFP": "Extraverted, Sensing, Feeling, Perceiving",
}

TYPE_SUMMARIES = {
    "INTJ": "You likely prefer seeing the big picture, thinking ahead, and making a clear plan.",
    "INFJ": "You likely mix strong intuition with a thoughtful awareness of people and meaning.",
    "ENTJ": "You likely enjoy setting direction, making decisions, and moving ideas into action.",
    "ENFJ": "You likely read people well and like helping groups move toward a shared goal.",
    "INTP": "You likely enjoy understanding how things work and refining ideas until they make sense.",
    "INFP": "You likely care deeply about staying true to your values while exploring possibilities.",
    "ENTP": "You likely enjoy exploring new ideas, asking questions, and testing different angles.",
    "ENFP": "You likely bring curiosity, energy, and personal meaning into the way you explore ideas.",
    "ISTJ": "You likely value reliability, structure, and doing things in a steady, proven way.",
    "ISFJ": "You likely pay close attention to people, details, and the things that help life run smoothly.",
    "ESTJ": "You likely like creating order, setting standards, and getting practical results.",
    "ESFJ": "You likely enjoy supporting people in practical ways and keeping relationships steady.",
    "ISTP": "You likely prefer calm problem-solving, hands-on learning, and figuring things out directly.",
    "ISFP": "You likely move through life in a personal, grounded, and quietly values-driven way.",
    "ESTP": "You likely respond quickly to what is happening around you and enjoy adapting in real time.",
    "ESFP": "You likely bring warmth, spontaneity, and energy to people and everyday experiences.",
}


def _normalize_scores(function_strengths: Dict[str, float]) -> Dict[str, float]:
    if not function_strengths:
        return {key: 0.0 for key in FUNCTIONS}
    minimum = min(function_strengths.values())
    maximum = max(function_strengths.values())
    spread = maximum - minimum
    if spread <= 0:
        return {key: 50.0 for key in FUNCTIONS}
    return {key: round(((value - minimum) / spread) * 100, 1) for key, value in function_strengths.items()}


def score_answers(answers: Iterable[Answer]) -> Dict[str, float]:
    scores = {function: 0.0 for function in FUNCTIONS}
    for answer in answers:
        question = QUESTION_LOOKUP.get(answer.question_id)
        if not question:
            continue
        centered = answer.value - 3
        for function, weight in question.weights.items():
            scores[function] += centered * weight
    return scores


def get_axis_signal(scores: Dict[str, float]) -> Dict[str, float]:
    return {"Ni_vs_Ne": scores["Ni"] - scores["Ne"], "Si_vs_Se": scores["Si"] - scores["Se"], "Ti_vs_Te": scores["Ti"] - scores["Te"], "Fi_vs_Fe": scores["Fi"] - scores["Fe"]}


def infer_likely_axis(scores: Dict[str, float]) -> Tuple[str, str]:
    axis_signal = get_axis_signal(scores)
    axis_name, delta = min(axis_signal.items(), key=lambda item: abs(item[1]))
    leaning = "balanced"
    if delta > 0.75:
        leaning = axis_name.split("_vs_")[0]
    elif delta < -0.75:
        leaning = axis_name.split("_vs_")[1]
    notes = f"Midpoint suggests the clearest uncertainty is {axis_name.replace('_vs_', ' vs ')}. Current lean: {leaning}."
    return axis_name, notes


def _attitude_letter(primary_function: str) -> str:
    return "E" if primary_function.endswith("e") else "I"


def _judging_letter(scores: Dict[str, float]) -> str:
    return "T" if (scores["Ti"] + scores["Te"]) >= (scores["Fi"] + scores["Fe"]) else "F"


def _perceiving_letter(scores: Dict[str, float]) -> str:
    return "N" if (scores["Ni"] + scores["Ne"]) >= (scores["Si"] + scores["Se"]) else "S"


def _lifestyle_letter(primary_function: str) -> str:
    if primary_function in {"Te", "Fe", "Ni", "Si"}:
        return "J"
    return "P"


def _grant_style_type(scores: Dict[str, float]) -> str:
    dominant = max(FUNCTIONS, key=lambda function: scores[function])
    return f"{_attitude_letter(dominant)}{_perceiving_letter(scores)}{_judging_letter(scores)}{_lifestyle_letter(dominant)}"


def _stack_fit_score(stack: List[str], scores: Dict[str, float]) -> float:
    weights = [1.0, 0.82, 0.58, 0.36]
    return sum(scores[function] * weights[index] for index, function in enumerate(stack))


def rank_types(scores: Dict[str, float]) -> List[Tuple[str, float]]:
    ranking = [(mbti_type, _stack_fit_score(stack, scores)) for mbti_type, stack in TYPE_STACKS.items()]
    ranking.sort(key=lambda item: item[1], reverse=True)
    grant_guess = _grant_style_type(scores)
    if ranking and ranking[0][0] != grant_guess:
        boosted = [(mbti_type, fit + 2.5 if mbti_type == grant_guess else fit) for mbti_type, fit in ranking]
        boosted.sort(key=lambda item: item[1], reverse=True)
        return boosted
    return ranking


def summarize_type(primary_type: str, secondary_type: str, scores: Dict[str, float]) -> str:
    strongest = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:2]
    strengths = " and ".join(function_name for function_name, _ in strongest)
    base = TYPE_SUMMARIES.get(primary_type, "A differentiated personality profile with a distinct cognitive style.")
    primary_full = TYPE_FULL_NAMES.get(primary_type, primary_type)
    secondary_full = TYPE_FULL_NAMES.get(secondary_type, secondary_type)
    primary_stack = "-".join(TYPE_STACKS.get(primary_type, []))
    return (
        f"Your strongest fit is {primary_type} ({primary_full}). {base} "
        f"Your answers most strongly matched the {primary_stack} function pattern, with {strengths} standing out the most. "
        f"A close second was {secondary_type} ({secondary_full})."
    )


def analyze_answers(answers: Iterable[Answer]) -> AnalysisResult:
    scored = score_answers(answers)
    normalized = _normalize_scores(scored)
    ranked = rank_types(scored)
    primary_type, primary_fit = ranked[0]
    secondary_type, secondary_fit = ranked[1]
    fit_ratio = round((secondary_fit / primary_fit) * 100, 1) if primary_fit else 0.0
    likely_axis, _ = infer_likely_axis(scored)
    return AnalysisResult(primary_type=primary_type, secondary_type=secondary_type, fit_ratio=fit_ratio, function_strengths=normalized, summary=summarize_type(primary_type, secondary_type, scored), likely_axis=likely_axis)


def select_initial_questions() -> List[Question]:
    lookup = {question.id: question for question in QUESTION_BANK}
    return [lookup[question_id] for question_id in BASE_QUESTION_IDS]


def select_adaptive_questions(answers: Iterable[Answer]) -> Tuple[List[Question], str, str]:
    scores = score_answers(answers)
    likely_axis, notes = infer_likely_axis(scores)
    remaining = [question for question in QUESTION_BANK if question.id not in BASE_QUESTION_IDS]
    axis_tag = likely_axis.replace("_vs_", "-").lower()
    prioritized = [question for question in remaining if axis_tag in [tag.lower() for tag in question.tags]]
    fallback = [question for question in remaining if question not in prioritized]
    return (prioritized + fallback)[:15], likely_axis, notes
