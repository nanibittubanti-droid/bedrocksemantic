import logging
from typing import Iterable, Optional

from app.config import Config
from app.models.request import AssessmentRequest
from app.services.postgres_service import PostgresService
from app.services.knowledgebase_service import KnowledgeBaseService
from app.services.pgvector_service import PgVectorService
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(
        self,
        config: Config,
        postgres: PostgresService,
        knowledge_service: KnowledgeBaseService,
        pgvector: Optional[PgVectorService] = None,
        embedder: Optional[EmbeddingService] = None,
    ) -> None:
        self.config = config
        self.postgres = postgres
        self.knowledge_service = knowledge_service
        self.pgvector = pgvector
        self.embedder = embedder

    def ingest_document(self, source: str, content: str, metadata: dict[str, str] | None = None) -> None:
        logger.info("Ingesting knowledge document from %s", source)
        # generate uuid for the document so we can reference it in the vector table
        doc_id = self.postgres.generate_uuid()
        self.postgres.insert(
            "INSERT INTO knowledge_documents (id, source, chunk_index, content, metadata) VALUES (%s, %s, %s, %s, %s)",
            (doc_id, source, 0, content, metadata or {}),
        )

        if self.pgvector and self.embedder:
            vector = self.embedder.embed(content, dim=self.config.embedding_dim)
            try:
                self.pgvector.upsert(doc_id, vector, metadata=metadata or {})
            except Exception:
                logger.exception("Failed to upsert embedding for doc %s", doc_id)

    def retrieve(self, query: str, limit: int = 5) -> list[str]:
        logger.info("Retrieving RAG documents for query: %s", query)

        # Prefer vector similarity search when available
        if self.pgvector and self.embedder:
            try:
                qvec = self.embedder.embed(query, dim=self.config.embedding_dim)
                rows = self.pgvector.query_similar(qvec, top_k=limit)
                doc_ids = [r["doc_id"] for r in rows]
                if doc_ids:
                    placeholders = ",".join(["%s"] * len(doc_ids))
                    sql = f"SELECT content FROM knowledge_documents WHERE id IN ({placeholders}) ORDER BY created_at DESC"
                    docs = self.postgres.fetchall(sql, tuple(doc_ids))
                    return [d["content"] for d in docs]
            except Exception:
                logger.exception("Vector retrieval failed; falling back to full-text")

        documents = self.postgres.fetchall(
            "SELECT content FROM knowledge_documents WHERE to_tsvector('english', content) @@ plainto_tsquery('english', %s) ORDER BY created_at DESC LIMIT %s",
            (query, limit),
        )
        return [row["content"] for row in documents]

    def enrich_prompt(
        self,
        agent_name: str,
        request: AssessmentRequest,
        extra_context: dict[str, str] | None = None,
    ) -> list[str]:
        query = request.request_id
        if extra_context:
            query = " ".join(extra_context.values())
        retrieved = self.retrieve(query)
        logger.debug("Retrieved %d documents for agent %s", len(retrieved), agent_name)
        return retrieved
