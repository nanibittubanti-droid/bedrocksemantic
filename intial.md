# Quick Start (Initial) — Bedrock Agent

This file helps a new developer get started quickly with the Bedrock Agent workspace.

Prerequisites
- Git
- Python 3.12
- Docker & Docker Compose (for local Postgres and ingestion)
- Optional: GitHub CLI (`gh`) if you want to push and create PRs from CLI

Clone the repository

```bash
git clone <your-fork-or-upstream-url> bedrock-agent
cd bedrock-agent
```

Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Run unit tests

```bash
pytest -q
```

Local Postgres + PDF ingestion (quick)

1. Place `waf.pdf` under `data/waf.pdf`.
2. Start Postgres and run ingestion via docker-compose:

```bash
docker compose -f docker/docker-compose.yml up --build --abort-on-container-exit ingest
```

Run the agent locally

```bash
export DATABASE_URL=postgresql://app:pass@localhost:5432/bedrock
export AWS_REGION=us-east-1
export MODEL_ID=amazon.titan-text-bison
python -m app.main ./examples/assessment_request.json
```

CI and Repository Notes
- A GitHub Actions workflow is included at `.github/workflows/ci.yml` that runs unit tests and a Postgres schema smoke test.
- Add repository secrets for integrations (if needed): `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DATABASE_URL`.

Where to look
- Runtime entrypoint: `app/main.py`
- Orchestrator: `app/orchestrator/workflow.py`
- RAG & KB: `app/services/rag_service.py`, `app/services/knowledgebase_service.py`
- Postgres helper: `app/services/postgres_service.py`
- Embeddings: `app/services/embedding_service.py` (Bedrock + local fallback)
- Tests: `tests/`

If something fails
- Check that `DATABASE_URL` is reachable and correct.
- Ensure required DB extensions (`pgcrypto`, `vector` if using pgvector) are available in your Postgres image.
- For CI-related or Bedrock issues, consult `README.md` and `documentation.md`.

Want help pushing and creating a PR?
- I can generate the exact `git` and `gh` commands for your environment and create a branch and PR for you — tell me your remote URL and branch name.
