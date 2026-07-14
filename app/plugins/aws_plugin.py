import logging

logger = logging.getLogger(__name__)


class AWSPlugin:
    def get_account_info(self) -> dict[str, str]:
        logger.debug("Retrieving AWS account information")
        return {}
