import logging
from typing import Dict

from app.models.request import AssessmentRequest
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class PillarAgent:
    PILLAR_NAMES = [
        "security",
        "reliability",
        "performance",
        "cost",
        "operational_excellence",
    ]

    def __init__(self, bedrock_service: BedrockService) -> None:
        self.bedrock_service = bedrock_service

    def assess(self, request: AssessmentRequest, system_summary: str) -> Dict[str, str]:
        logger.info("Pillar agent evaluating request %s", request.request_id)
        pillar_results: Dict[str, str] = {}

        for pillar in self.PILLAR_NAMES:
            pillar_results[pillar] = self.bedrock_service.evaluate_agent(
                pillar,
                request,
                extra_context={"system_summary": system_summary},
            )

        return pillar_results
