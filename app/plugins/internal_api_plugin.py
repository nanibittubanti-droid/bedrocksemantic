import logging

logger = logging.getLogger(__name__)


class InternalAPIPlugin:
    def call_endpoint(self, endpoint: str, payload: dict[str, str]) -> dict[str, str]:
        logger.debug("Calling internal API endpoint %s", endpoint)
        return {"endpoint": endpoint, "payload": payload}
