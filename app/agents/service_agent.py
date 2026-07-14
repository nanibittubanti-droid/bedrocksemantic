import logging

from app.models.request import AssessmentRequest
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class ServiceAgent:
    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def assess(self, request: AssessmentRequest, workload_summary: str) -> str:
        logger.info("Service agent evaluating request %s", request.request_id)
        return self.bedrock_service.evaluate_agent(
            "service",
            request,
            extra_context={"workload_summary": workload_summary},
        )
