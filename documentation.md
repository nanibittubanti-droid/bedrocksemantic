## Project Documentation & Phased Implementation Plan

This document describes a phased implementation plan for the Bedrock Agent project, with recommended milestones, design notes, and future enhancements. It's intended for new contributors or teams who will implement this project in stages.

**Goal:** Implement a SOW-compliant agent orchestration runtime that runs on AWS Bedrock AgentCore, uses Semantic Kernel for orchestration, and stores knowledge, sessions, and memory in PostgreSQL with RAG (Retrieval-Augmented Generation).

---

**Phase 0 — Foundations (Existing)**
- Project scaffold with `app/`, `docker/`, `terraform/`, `scripts/` and `tests/`.
- Core runtime entrypoint: `app/main.py` (AgentCore-only, no HTTP server).
- Semantic Kernel runtime wrapper: `app/kernel/kernel.py`.
- Prompt templates under `app/prompts` and `app/prompts/prompt_set.py`.
- Orchestrator implemented: `app/orchestrator/workflow.py` wiring System → Pillars → Workload → Service → Recommendation Engine.
- Basic persistence layer: `app/services/postgres_service.py` (DB schema, connection helper).

**Phase 1 — Persisted Knowledge & Basic RAG (Current Completed Work)**
- Knowledge ingestion: `app/services/knowledgebase_service.py` and `app/services/pdf_ingest_service.py` for PDF chunking & ingestion.
- Postgres-backed RAG: `app/services/rag_service.py` (full-text) and `app/services/postgres_service.py` schema for `knowledge_documents`.
- Session & Memory services: `app/services/session_service.py` and `app/services/memory_service.py`.
- Bedrock wrapper: `app/services/bedrock_service.py` — registers agent semantic functions and loads retrieved context into prompts.
- Local testing: `docker/docker-compose.yml`, `scripts/ingest_pdf.py`, `scripts/run_ingest_container.sh`.

Testing & CI:
- Unit tests in `tests/` mocking Postgres and Bedrock kernel where needed.
- `requirements.txt` updated — include `psycopg[binary]` and `pypdf` for ingestion and DB connectivity.

**Phase 2 — Vector Search (pgvector) & Embeddings (In-Progress)**
- Add `PgVectorService` (`app/services/pgvector_service.py`) and DB init SQL (`docker/init-db/init-pgvector.sql`).
- Add `EmbeddingService` (`app/services/embedding_service.py`) to produce embeddings via Bedrock or local fallback.
- Update `RAGService` to prefer vector similarity retrieval; fall back to full-text search.
- Update ingestion pipeline to compute and upsert embeddings for each document chunk.

Acceptance criteria:
- Vector queries return semantically relevant documents for sample queries.
- Ingestion and retrieval validated by unit tests and a docker-compose-based integration test.

**Phase 3 — Robustness, Scalability & Operationalization**
- Replace local Postgres with managed Postgres or an external vector DB (e.g., Pinecone, Milvus) for scale.
- Implement batching and async ingestion for large corpora.
- Add rate-limiting, retries, and exponential backoff to all external calls (Bedrock, DB connections).
- Add structured logging and metrics (Prometheus + Grafana, CloudWatch metrics), and distributed tracing.

Operational concerns:
- DB migrations with `alembic` or `liquibase`.
- Containerize ingestion as a job for Kubernetes CronJob or AWS Batch for scheduled imports.

**Phase 4 — Security, Governance & Compliance**
- Add KMS encryption for stored documents and environment secrets.
- Implement access control for agent operations and APIs (if adding REST later).
- Sanitize or redact sensitive content during ingestion.
- Add audit logs for agent decisions and user interactions.

**Phase 5 — Feature Expansion & UX**
- Add a lightweight web UI for human-in-the-loop review and feedback.
- Add interactive agent CLI with session-scoped context and tooling to replay assessments.
- Build a feedback loop to capture user corrections and use them to improve prompt templates or memory entries.

---

Development Checklist (developer onboarding)
- Install Python 3.12 and dependencies: `pip install -r requirements.txt`.
- Start local Postgres (Docker): `docker compose -f docker/docker-compose.yml up db`.
- Ingest a sample PDF: `python scripts/ingest_pdf.py data/waf.pdf` or use the ingest service from `docker compose`.
- Run unit tests: `pytest -q` (consider using a virtualenv).

Future enhancement ideas
- Embed model selection: Provide a configuration to choose embedding models per workload and experiment with different dimensions.
- Cross-document summarization: Add pipeline to automatically generate high-quality summaries per document chunk and store them as metadata.
- Fine-grained caching and TTLs: Cache retrieval results with short TTLs to reduce cost on embedding calls.
- Multi-language support: Detect language and use appropriate tokenizers / embedding models.
- Active learning loop: Surface low-confidence agent outputs for human labeling and incorporate labels back into search/filters.

Security & Data Privacy Notes
- Remove or obfuscate PII on ingestion by adding a preprocessing step.
- Use `DATABASE_URL` and AWS credentials from a secrets manager (AWS Secrets Manager) in production.

Maintenance & Ownership
- Ownership: Create a small on-call rotation for production incidents related to the agent runtime.
- Upgrades: Keep a dependency matrix for `semantic-kernel` and Bedrock runtime compatibility.

Appendix: Key Files and Responsibilities
- `app/main.py` — runtime entrypoint (AgentCore-only)
- `app/kernel/kernel.py` — Semantic Kernel runtime initialization
- `app/orchestrator/workflow.py` — SOW-orchestrator that sequences agents
- `app/services/` — Postgres, RAG, Embeddings, Memory, Session, PDF ingest
- `docker/docker-compose.yml` — local testing with Postgres and ingestion job
- `docker/init-db/init-pgvector.sql` — example DB init for pgvector

---

If you'd like, I can also:
- Add a phase-by-phase checklist file with issues/PR templates for each milestone.
- Create an `architectural_diagram.mmd` (Mermaid) to visualize the runtime and data flows.
