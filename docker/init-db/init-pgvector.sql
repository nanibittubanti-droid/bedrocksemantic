-- Initialize pgvector extension and embeddings table for semantic search
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  doc_id text NOT NULL,
  vector vector(1536) NOT NULL,
  metadata jsonb,
  created_at timestamptz DEFAULT now()
);
