from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .analysis import analyze_answers, select_adaptive_questions, select_initial_questions
from .artifacts import write_persona_artifact
from .models import AdaptRequest, AdaptResponse, AdaptiveHint, QuizStartResponse, ResultRequest


app = FastAPI(title="TypeQuest API", version="0.1.0")
STATIC_DIR = Path(__file__).resolve().parent / "static"
ASSETS_DIR = STATIC_DIR / "assets"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/api/quiz/start", response_model=QuizStartResponse)
def start_quiz() -> QuizStartResponse:
    return QuizStartResponse(questions=select_initial_questions(), total_questions=30, midpoint=15)


@app.post("/api/quiz/adapt", response_model=AdaptResponse)
def adapt_quiz(payload: AdaptRequest) -> AdaptResponse:
    questions, likely_axis, notes = select_adaptive_questions(payload.answers)
    return AdaptResponse(hint=AdaptiveHint(likely_axis=likely_axis, notes=notes), questions=questions)


@app.post("/api/quiz/result")
def get_result(payload: ResultRequest):
    result = analyze_answers(payload.answers)
    write_persona_artifact(result.model_dump(), payload.answers, source="fastapi")
    return result


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(STATIC_DIR / "index.html")
