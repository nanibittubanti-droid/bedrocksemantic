import logging
from typing import Any

from app.services.postgres_service import PostgresService

logger = logging.getLogger(__name__)


class KnowledgeBaseService:
    def __init__(self, postgres: PostgresService) -> None:
        self.postgres = postgres

    def ingest_text(self, source: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        logger.debug("Ingesting knowledge text from source %s", source)
        self.postgres.insert(
            "INSERT INTO knowledge_documents (source, chunk_index, content, metadata) VALUES (%s, %s, %s, %s)",
            (source, 0, content, metadata or {}),
        )

    def retrieve_relevant_documents(self, query: str, limit: int = 5) -> list[str]:
        logger.debug("Retrieving relevant documents for query: %s", query)
        rows = self.postgres.fetchall(
            "SELECT content FROM knowledge_documents "
            "WHERE to_tsvector('english', content) @@ plainto_tsquery('english', %s) "
            "ORDER BY created_at DESC LIMIT %s",
            (query, limit),
        )
        return [row["content"] for row in rows]
