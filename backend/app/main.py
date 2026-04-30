from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from .analysis import analyze_answers, select_adaptive_questions, select_initial_questions
from .artifacts import write_persona_artifact
from .models import AdaptRequest, AdaptResponse, AdaptiveHint, QuizStartResponse, ResultRequest


app = FastAPI(title="TypeQuest API", version="0.1.0")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


def _serve_spa(full_path: str = ""):
    if not FRONTEND_DIST.exists():
        return JSONResponse(
            {"error": "Frontend build not found. Run the frontend build before deployment."},
            status_code=503,
        )

    if full_path:
        candidate = (FRONTEND_DIST / full_path).resolve()
        if candidate.is_file() and FRONTEND_DIST in candidate.parents:
            return FileResponse(candidate)

    index_file = FRONTEND_DIST / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    return JSONResponse({"error": "Frontend index.html not found."}, status_code=503)


@app.get("/", include_in_schema=False)
def serve_root():
    return _serve_spa()


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    return _serve_spa(full_path)
