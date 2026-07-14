import logging
from typing import Any

from app.config import Config
from app.services.postgres_service import PostgresService

logger = logging.getLogger(__name__)


class MemoryService:
    def __init__(self, config: Config, postgres: PostgresService) -> None:
        self.config = config
        self.postgres = postgres

    def save_memory(self, session_id: str, key: str, value: Any) -> None:
        logger.debug("Saving memory %s for session %s", key, session_id)
        self.postgres.insert(
            "INSERT INTO memory_entries (session_id, memory_key, memory_value) VALUES (%s, %s, %s)",
            (session_id, key, str(value),),
        )

    def load_memory(self, session_id: str, key: str) -> str | None:
        result = self.postgres.fetchone(
            "SELECT memory_value FROM memory_entries WHERE session_id = %s AND memory_key = %s ORDER BY created_at DESC LIMIT 1",
            (session_id, key),
        )
        return result["memory_value"] if result else None

    def list_memory(self, session_id: str) -> list[dict[str, str]]:
        return self.postgres.fetchall(
            "SELECT memory_key, memory_value, created_at FROM memory_entries WHERE session_id = %s ORDER BY created_at DESC",
            (session_id,),
        )
