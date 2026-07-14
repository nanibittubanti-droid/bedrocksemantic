"""Simple PDF ingestion runner for the knowledge base.

Usage:
    python scripts/ingest_pdf.py path/to/waf.pdf

This script loads configuration, connects to Postgres, and ingests the PDF into the
knowledge base using `PDFIngestService`.
"""
import sys
from pathlib import Path
import logging

from app.config import load_config
from app.services.postgres_service import PostgresService
from app.services.knowledgebase_service import KnowledgeBaseService
from app.services.pdf_ingest_service import PDFIngestService


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_pdf.py path/to/file.pdf")
        return 2

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print("PDF file not found:", pdf_path)
        return 2

    config = load_config()
    pg = PostgresService(config)
    kb = KnowledgeBaseService(pg)
    ingestor = PDFIngestService(kb)

    ingestor.ingest_pdf(pdf_path, source=pdf_path.name)
    print("Ingestion completed for", pdf_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
