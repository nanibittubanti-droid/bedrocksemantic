from unittest.mock import MagicMock

from app.services.session_service import SessionService
from app.services.memory_service import MemoryService


def test_session_create_and_history_calls_postgres():
    mock_postgres = MagicMock()
    mock_postgres.fetchone.return_value = {"session_id": "session-123"}
    session = SessionService(config=MagicMock(), postgres=mock_postgres)
    sid = session.create_session("user-1")
    assert sid == "session-123"
    mock_postgres.insert.assert_called()


def test_memory_save_and_load_calls_postgres():
    mock_postgres = MagicMock()
    mock_postgres.fetchone.return_value = {"memory_value": "value1"}
    mem = MemoryService(config=MagicMock(), postgres=mock_postgres)
    mem.save_memory("session-123", "k", "v")
    val = mem.load_memory("session-123", "k")
    assert val == "value1"
    mock_postgres.insert.assert_called()
