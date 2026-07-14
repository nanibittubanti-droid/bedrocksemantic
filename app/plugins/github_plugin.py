import logging

logger = logging.getLogger(__name__)


class GitHubPlugin:
    def fetch_repository(self, repo: str) -> dict[str, str]:
        logger.debug("Fetching repository %s from GitHub", repo)
        return {"repo": repo}
