from typing import List, Any, Dict, Optional

from app.services.postgres_service import PostgresService


class PgVectorService:
    """Lightweight wrapper to store and query embeddings using Postgres + pgvector.

    This is a scaffold: it expects the Postgres instance to have the `vector` extension
    available (pgvector). The embedding dimension is configurable.
    """

    def __init__(self, postgres: PostgresService, dim: int = 1536):
        self.pg = postgres
        self.dim = dim

    def init_schema(self) -> None:
        sql = f"""
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE TABLE IF NOT EXISTS embeddings (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            doc_id text NOT NULL,
            vector vector({self.dim}) NOT NULL,
            metadata jsonb,
            created_at timestamptz DEFAULT now()
        );
        """
        self.pg.execute(sql)

    def upsert(self, doc_id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        # pgvector input format: array of floats
        sql = "INSERT INTO embeddings (doc_id, vector, metadata) VALUES (%s, %s, %s);"
        self.pg.execute(sql, (doc_id, vector, metadata))

    def query_similar(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        sql = (
            "SELECT doc_id, metadata, vector FROM embeddings ORDER BY vector <-> %s LIMIT %s"
        )
        rows = self.pg.query(sql, (vector, top_k))
        return [dict(r) for r in rows]
