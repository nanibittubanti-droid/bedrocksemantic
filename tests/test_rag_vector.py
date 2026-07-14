from unittest.mock import MagicMock

from app.services.rag_service import RAGService


def test_retrieve_uses_vector_search_when_available():
    mock_config = MagicMock()
    mock_config.embedding_dim = 8

    mock_postgres = MagicMock()
    # Simulate vector rows returned by PgVectorService
    mock_pgvector = MagicMock()
    mock_pgvector.query_similar.return_value = [{"doc_id": "doc-1"}, {"doc_id": "doc-2"}]

    # Postgres should return document contents when queried by IDs
    mock_postgres.fetchall.return_value = [{"content": "doc1 content"}, {"content": "doc2 content"}]

    mock_embedder = MagicMock()
    mock_embedder.embed.return_value = [0.1] * mock_config.embedding_dim

    rag = RAGService(mock_config, mock_postgres, MagicMock(), pgvector=mock_pgvector, embedder=mock_embedder)

    results = rag.retrieve("some query", limit=2)

    assert mock_pgvector.query_similar.called
    assert results == ["doc1 content", "doc2 content"]


def test_retrieve_falls_back_to_fulltext_on_vector_failure():
    mock_config = MagicMock()
    mock_config.embedding_dim = 8

    mock_postgres = MagicMock()
    # Make pgvector raise an exception
    mock_pgvector = MagicMock()
    mock_pgvector.query_similar.side_effect = Exception("vector backend down")

    # For full-text fallback, postgres.fetchall returns results
    mock_postgres.fetchall.return_value = [{"content": "fulltext match"}]

    mock_embedder = MagicMock()
    mock_embedder.embed.return_value = [0.1] * mock_config.embedding_dim

    rag = RAGService(mock_config, mock_postgres, MagicMock(), pgvector=mock_pgvector, embedder=mock_embedder)

    results = rag.retrieve("some query", limit=2)

    # Should have fallen back and returned full-text result
    assert results == ["fulltext match"]


def test_ingest_document_upserts_embedding():
    mock_config = MagicMock()
    mock_config.embedding_dim = 8

    mock_postgres = MagicMock()
    mock_postgres.generate_uuid.return_value = "uuid-123"

    mock_pgvector = MagicMock()
    mock_embedder = MagicMock()
    mock_embedder.embed.return_value = [0.2] * mock_config.embedding_dim

    rag = RAGService(mock_config, mock_postgres, MagicMock(), pgvector=mock_pgvector, embedder=mock_embedder)

    rag.ingest_document("waf.pdf", "document text", metadata={"source": "waf"})

    # Ensure the document was inserted and embedding upsert was called
    assert mock_postgres.insert.called
    assert mock_pgvector.upsert.called
