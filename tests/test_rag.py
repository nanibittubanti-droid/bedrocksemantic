from unittest.mock import MagicMock

from app.services.rag_service import RAGService


def test_rag_retrieve_calls_postgres_and_returns_content():
    mock_postgres = MagicMock()
    mock_postgres.fetchall.return_value = [{"content": "doc1"}, {"content": "doc2"}]

    rag = RAGService(config=MagicMock(), postgres=mock_postgres, knowledge_service=MagicMock())
    results = rag.retrieve("waf rule")

    assert results == ["doc1", "doc2"]
    mock_postgres.fetchall.assert_called_once()


def test_enrich_prompt_returns_documents():
    mock_postgres = MagicMock()
    mock_postgres.fetchall.return_value = [{"content": "docA"}]
    rag = RAGService(config=MagicMock(), postgres=mock_postgres, knowledge_service=MagicMock())

    class DummyRequest:
        request_id = "req-1"

    docs = rag.enrich_prompt("service", DummyRequest())
    assert isinstance(docs, list)
    assert docs[0] == "docA"
