import logging

from app.models.assessment import AssessmentRequest, AssessmentResponse
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def run_assessment(self, request: AssessmentRequest) -> AssessmentResponse:
        logger.info("Running assessment orchestrator for request %s", request.request_id)
        return self.bedrock_service.evaluate_request(request)
