from typing import Dict, List, Optional

from pydantic import BaseModel, Field


FunctionCode = str


class Question(BaseModel):
    id: str
    prompt: str
    weights: Dict[FunctionCode, float]
    tags: List[str] = Field(default_factory=list)


class Answer(BaseModel):
    question_id: str
    value: int = Field(ge=1, le=5)


class QuizStartResponse(BaseModel):
    questions: List[Question]
    total_questions: int
    midpoint: int


class AdaptiveHint(BaseModel):
    likely_axis: str
    notes: str


class AdaptRequest(BaseModel):
    answers: List[Answer]


class AdaptResponse(BaseModel):
    hint: AdaptiveHint
    questions: List[Question]


class ResultRequest(BaseModel):
    answers: List[Answer]


class AnalysisResult(BaseModel):
    primary_type: str
    secondary_type: str
    fit_ratio: float
    function_strengths: Dict[FunctionCode, float]
    summary: str
    likely_axis: Optional[str] = None
