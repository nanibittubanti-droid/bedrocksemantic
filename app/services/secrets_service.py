import logging

logger = logging.getLogger(__name__)


class SecretsService:
    def __init__(self) -> None:
        pass

    def get_secret(self, name: str) -> str:
        logger.debug("Retrieving secret %s", name)
        return ""
