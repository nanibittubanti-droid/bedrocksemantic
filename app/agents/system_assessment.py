import logging

from app.models.request import AssessmentRequest
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class SystemAssessmentAgent:
    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def assess(self, request: AssessmentRequest) -> str:
        logger.info("System assessment agent evaluating request %s", request.request_id)
        return self.bedrock_service.evaluate_agent("system", request)
