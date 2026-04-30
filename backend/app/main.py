from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .analysis import analyze_answers, select_adaptive_questions, select_initial_questions
from .artifacts import write_persona_artifact
from .models import AdaptRequest, AdaptResponse, AdaptiveHint, QuizStartResponse, ResultRequest


app = FastAPI(title="TypeQuest API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/quiz/start", response_model=QuizStartResponse)
def start_quiz() -> QuizStartResponse:
    return QuizStartResponse(questions=select_initial_questions(), total_questions=30, midpoint=15)


@app.post("/quiz/adapt", response_model=AdaptResponse)
def adapt_quiz(payload: AdaptRequest) -> AdaptResponse:
    questions, likely_axis, notes = select_adaptive_questions(payload.answers)
    return AdaptResponse(hint=AdaptiveHint(likely_axis=likely_axis, notes=notes), questions=questions)


@app.post("/quiz/result")
def get_result(payload: ResultRequest):
    result = analyze_answers(payload.answers)
    write_persona_artifact(result.model_dump(), payload.answers, source="fastapi")
    return result
