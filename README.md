# BookPilot

BookPilot is a modular-monolith PDF-to-audiobook application. A user uploads a PDF, the worker parses it into reviewable chapters, and chapter-level generation creates local audio playable in the browser.

## Current V1 scope

Included: registration/login, protected user-owned books, PDF validation and local storage, parsing and heuristic chapter detection, chapter review, deterministic chunking, background ingestion/generation jobs, mock TTS audio, chapter audio, and persisted playback position.

Out of scope: marketplace/catalog, payments, RAG, collaboration, mobile apps, voice cloning, and mandatory paid providers.

## Architecture

React/Vite calls a FastAPI API. SQLAlchemy/Alembic persist users, books, document assets, jobs, chapters, chunks, audio assets, and playback progress in PostgreSQL. A separate `worker.py` process claims queued jobs. Parser, TTS fallback, and filesystem storage are isolated service modules.

## Local setup

Prerequisites: Python 3.11, Node.js 20+, and Docker Desktop.

```powershell
Copy-Item .env.example .env
docker compose up -d db
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH='.'
alembic upgrade head
uvicorn app.main:app --reload
```

In another terminal run `cd frontend; npm install; npm run dev`. In a third terminal run `cd backend; .\.venv\Scripts\Activate.ps1; $env:PYTHONPATH='.'; python worker.py`. Open `http://localhost:5173`, register, upload a PDF, wait for ingestion, review/save chapters, then start generation.

Mock generation uses the bundled short demo voice clips so playback can be exercised offline without credentials. These clips are playback fixtures and do not narrate the uploaded chapter text; connect a real TTS provider when text-matched narration is needed.

## Environment variables

See [.env.example](.env.example) for `DATABASE_URL`, `JWT_SECRET`, `STORAGE_ROOT`, upload limits, `TTS_PROVIDER`, `CORS_ORIGINS`, and `VITE_API_URL`. `TTS_PROVIDER=mock` requires no external account.

## Database and storage

PostgreSQL is defined in `docker-compose.yml`. Run `alembic upgrade head` against a clean database; the migration chain is a single coherent V1 baseline. Uploaded PDFs and generated audio live under ignored `storage/`.

## Testing

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH='.'
pytest -q
cd ..\frontend
npm run build
```

## Documentation and team workflow

Start with [docs/README.md](docs/README.md), followed by the vision, requirements, architecture, data flow, data model, parsing, and audio documents. These files copied from `bookpilot-design-docs.zip` are the canonical product/architecture reference.

Backend domain and pipeline code is under `backend/app/`; routes are under `backend/app/api/routes/`; the worker is `backend/worker.py`; the client entry point is `frontend/src/app/router.tsx`. Keep provider-specific details out of routes and update the relevant design document when architecture changes.
