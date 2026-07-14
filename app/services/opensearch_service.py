import logging

logger = logging.getLogger(__name__)


class OpenSearchService:
    def __init__(self) -> None:
        pass

    def search(self, query: str) -> list[str]:
        logger.debug("Searching OpenSearch for query: %s", query)
        return []
