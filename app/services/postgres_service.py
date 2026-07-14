import json
import logging
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.config import Config

logger = logging.getLogger(__name__)


class PostgresService:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._connection = self._connect()
        self._ensure_schema()

    def _connect(self) -> psycopg.Connection:
        if not self.config.database_url:
            raise ValueError("DATABASE_URL is required for PostgreSQL persistence")

        logger.debug("Connecting to PostgreSQL: %s", self.config.database_url)
        return psycopg.connect(self.config.database_url, row_factory=dict_row, autocommit=True)

    def _ensure_schema(self) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_documents (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    source TEXT NOT NULL,
                    chunk_index INT NOT NULL,
                    content TEXT NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_knowledge_documents_source ON knowledge_documents(source);
                CREATE INDEX IF NOT EXISTS idx_knowledge_documents_content ON knowledge_documents USING GIN (to_tsvector('english', content));

                CREATE TABLE IF NOT EXISTS sessions (
                    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id TEXT NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    last_activity TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    session_id UUID NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);

                CREATE TABLE IF NOT EXISTS memory_entries (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    session_id UUID NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    memory_key TEXT NOT NULL,
                    memory_value TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_memory_entries_session_key ON memory_entries(session_id, memory_key);
                """
            )
            logger.debug("PostgreSQL schema verified")

    def generate_uuid(self) -> str:
        row = self.fetchone("SELECT gen_random_uuid() AS uuid")
        return str(row["uuid"])

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(query, params or ())

    def fetchone(self, query: str, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        with self._connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def fetchall(self, query: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        with self._connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def insert(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        self.execute(query, params)

    def close(self) -> None:
        self._connection.close()
