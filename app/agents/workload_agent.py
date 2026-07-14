import logging

from app.models.request import AssessmentRequest
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class WorkloadAgent:
    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def assess(self, request: AssessmentRequest, pillar_summary: str) -> str:
        logger.info("Workload agent evaluating request %s", request.request_id)
        return self.bedrock_service.evaluate_agent(
            "workload",
            request,
            extra_context={"pillar_summary": pillar_summary},
        )
