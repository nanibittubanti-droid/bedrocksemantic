import logging

logger = logging.getLogger(__name__)


class JiraPlugin:
    def fetch_issue(self, issue_id: str) -> dict[str, str]:
        logger.debug("Fetching Jira issue %s", issue_id)
        return {"issue_id": issue_id}
