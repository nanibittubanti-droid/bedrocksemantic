import logging

from app.models.assessment import AssessmentRequest, AssessmentResponse
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class CostAgent:
    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def assess(self, request: AssessmentRequest) -> AssessmentResponse:
        logger.info("Cost agent evaluating request %s", request.request_id)
        return self.bedrock_service.evaluate_request(request)
