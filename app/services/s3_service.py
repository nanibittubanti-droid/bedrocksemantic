import logging

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self) -> None:
        pass

    def upload_artifact(self, key: str, content: str) -> str:
        logger.debug("Uploading artifact %s", key)
        return key
