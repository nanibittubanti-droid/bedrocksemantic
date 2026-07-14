import logging

from app.models.request import AssessmentRequest
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class RecommendationEngine:
    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def assess(
        self,
        request: AssessmentRequest,
        system_summary: str,
        pillar_summary: str,
        workload_summary: str,
        service_summary: str,
    ) -> str:
        logger.info("Recommendation engine evaluating request %s", request.request_id)
        return self.bedrock_service.evaluate_agent(
            "recommendation_engine",
            request,
            extra_context={
                "system_summary": system_summary,
                "pillar_summary": pillar_summary,
                "workload_summary": workload_summary,
                "service_summary": service_summary,
            },
        )
