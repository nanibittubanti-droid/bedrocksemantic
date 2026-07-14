import logging
from typing import Any

from app.config import Config
from app.services.postgres_service import PostgresService

logger = logging.getLogger(__name__)


class SessionService:
    def __init__(self, config: Config, postgres: PostgresService) -> None:
        self.config = config
        self.postgres = postgres

    def create_session(self, user_id: str, metadata: dict[str, Any] | None = None) -> str:
        logger.debug("Creating session for user %s", user_id)
        self.postgres.insert(
            "INSERT INTO sessions (user_id, metadata) VALUES (%s, %s)",
            (user_id, metadata or {},),
        )

        result = self.postgres.fetchone(
            "SELECT session_id FROM sessions WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        )
        return str(result["session_id"])

    def save_chat_message(self, session_id: str, role: str, content: str) -> None:
        logger.debug("Saving chat message for session %s", session_id)
        self.postgres.insert(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (%s, %s, %s)",
            (session_id, role, content),
        )
        self.postgres.execute(
            "UPDATE sessions SET last_activity = NOW() WHERE session_id = %s",
            (session_id,),
        )

    def get_session_history(self, session_id: str) -> list[dict[str, Any]]:
        return self.postgres.fetchall(
            "SELECT role, content, created_at FROM chat_messages WHERE session_id = %s ORDER BY created_at ASC",
            (session_id,),
        )

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        return self.postgres.fetchone(
            "SELECT session_id, user_id, metadata, created_at, last_activity FROM sessions WHERE session_id = %s",
            (session_id,),
        )
