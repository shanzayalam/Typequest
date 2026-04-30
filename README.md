# TypeQuest

TypeQuest is a high-fidelity, adaptive MBTI assessment experience with:

- A React + Tailwind frontend for a 30-question cognitive function quiz
- A FastAPI backend for quiz orchestration and analysis
- An MCP server exposing `analyze_personality` for tool-based integration

## Project Structure

```text
frontend/   React + Vite + Tailwind + Recharts
backend/    FastAPI app, quiz logic, MCP server
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://127.0.0.1:8000`.

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## MCP Server

```bash
cd backend
python -m app.mcp_server
```

## Verify MCP Integration

You can verify that the MCP integration is wired correctly in two quick ways:

```bash
cd backend
python verify_mcp.py
```

That script imports the MCP server module and calls the exposed `analyze_personality` tool function with sample data. If it prints a structured result, the shared analysis engine and MCP tool wiring are working.
It also writes a real artifact to [data/persona.json](C:/Users/HP/OneDrive/Documents/New%20project/data/persona.json), which you can verify in the file browser.


The FastAPI quiz result endpoint  writes the latest result to [data/persona.json](C:/Users/HP/OneDrive/Documents/New%20project/data/persona.json), so completing the quiz creates the same proof artifact.

## Free Public Link

TypeQuest is now structured so you can deploy it as a single free Vercel project and get one shareable public link.

### What is configured

- `frontend/` builds the React app
- `api/index.py` exposes the FastAPI app to Vercel
- `frontend/src/lib/api.js` uses same-origin `/api` requests
- `frontend/vite.config.js` proxies `/api` to the local backend in development

### Deploy

1. Push this repository to GitHub.
2. Import the repo into Vercel.
3. Keep the project root at the repository root.
4. Click deploy.

Vercel should generate a public URL like:

```text
https://your-project-name.vercel.app
```

That one link can be shared directly with friends or colleagues.
