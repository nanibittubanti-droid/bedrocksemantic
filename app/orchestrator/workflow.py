import logging
import uuid
from typing import Dict

from app.agents.pillar_agent import PillarAgent
from app.agents.recommendation_engine import RecommendationEngine
from app.agents.service_agent import ServiceAgent
from app.agents.system_assessment import SystemAssessmentAgent
from app.agents.workload_agent import WorkloadAgent
from app.models.request import AssessmentRequest
from app.models.response import AssessmentResponse, Evidence, Recommendation
from app.services.bedrock_service import BedrockService

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Manage the SOW agent workflow and task handoff."""

    def __init__(self, bedrock_service: BedrockService) -> None:
        self.system_agent = SystemAssessmentAgent(bedrock_service)
        self.pillar_agent = PillarAgent(bedrock_service)
        self.workload_agent = WorkloadAgent(bedrock_service)
        self.service_agent = ServiceAgent(bedrock_service)
        self.recommendation_engine = RecommendationEngine(bedrock_service)

    def _summarize_pillars(self, pillar_results: Dict[str, str]) -> str:
        return "\n".join(
            f"{pillar}: {result.splitlines()[0] if result else 'No output'}"
            for pillar, result in pillar_results.items()
        )

    def orchestrate(self, request: AssessmentRequest) -> AssessmentResponse:
        system_summary = self.system_agent.assess(request)
        pillar_results = self.pillar_agent.assess(request, system_summary)
        pillar_summary = self._summarize_pillars(pillar_results)
        workload_summary = self.workload_agent.assess(request, pillar_summary)
        service_summary = self.service_agent.assess(request, workload_summary)
        recommendation_output = self.recommendation_engine.assess(
            request,
            system_summary,
            pillar_summary,
            workload_summary,
            service_summary,
        )

        recommendations = [
            Recommendation(
                pillar="Service",
                title="AWS service recommendations",
                detail=service_summary[:512],
                confidence=0.75,
            ),
            Recommendation(
                pillar="Pillars",
                title="Well-Architected pillar findings",
                detail=pillar_summary[:512],
                confidence=0.75,
            ),
        ]

        evidence = [
            Evidence(
                source="Bedrock AgentCore",
                description="Generated consolidated assessment output",
                excerpt=recommendation_output[:256],
            )
        ]

        return AssessmentResponse(
            request_id=request.request_id,
            assessment_id=str(uuid.uuid4()),
            summary=recommendation_output.splitlines()[0] if recommendation_output else "Assessment completed.",
            recommendations=recommendations,
            evidence=evidence,
            confidence_score=0.75,
            raw_output=recommendation_output,
        )
