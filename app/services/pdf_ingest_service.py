import logging
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

from app.services.knowledgebase_service import KnowledgeBaseService

logger = logging.getLogger(__name__)


class PDFIngestService:
    def __init__(self, knowledge_service: KnowledgeBaseService) -> None:
        self.knowledge_service = knowledge_service

    def _chunk_text(self, text: str, chunk_size: int = 1200) -> Iterable[str]:
        words = text.split()
        for start in range(0, len(words), chunk_size):
            yield " ".join(words[start : start + chunk_size])

    def ingest_pdf(self, path: Path, source: str | None = None) -> None:
        logger.info("Ingesting PDF %s into knowledge base", path)
        reader = PdfReader(path)
        content = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text:
                content.append(text)

        document_text = "\n\n".join(content)
        source_name = source or path.name
        for index, chunk in enumerate(self._chunk_text(document_text)):
            self.knowledge_service.ingest_text(
                source=source_name,
                content=chunk,
                metadata={"page_chunk": index, "source": source_name},
            )
        logger.info("Ingested %d PDF chunks from %s", len(content), path)
