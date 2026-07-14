import logging
import uuid
from typing import Any

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.bedrock import BedrockTextCompletion

from app.config import Config
from app.models import AssessmentArtifact, AssessmentRequest, AssessmentResponse, Evidence, Recommendation
from app.prompts import AGENT_PROMPTS, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class BedrockAgentCore:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._kernel: Kernel | None = None
        self._completion: BedrockTextCompletion | None = None
        self._agent_functions: dict[str, Any] = {}

    def initialize(self) -> None:
        logger.debug("Initializing Semantic Kernel for AgentCore")
        self._kernel = Kernel()
        self._completion = BedrockTextCompletion(
            model=self._config.model_id,
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
            endpoint=self._config.bedrock_endpoint,
            region=self._config.aws_region,
        )
        self._kernel.add_text_completion("bedrock", self._completion)

        for agent_name, agent_instruction in AGENT_PROMPTS.items():
            prompt_template = (
                f"{SYSTEM_PROMPT}\n\n"
                f"{agent_instruction}\n\n"
                "Context:\n{{context}}\n\n"
                "Artifacts:\n{{artifacts_summary}}\n\n"
                "Provide a concise assessment, list clear recommendations, cite evidence sources, "
                "and include a confidence estimate between 0.0 and 1.0."
            )
            self._agent_functions[agent_name] = self._kernel.create_semantic_function(
                prompt_template,
                skill_name=agent_name,
                description=f"Semantic function for the {agent_name} assessment agent.",
            )

        logger.info("Bedrock AgentCore initialized using model %s", self._config.model_id)

    def assess_artifacts(self, request: AssessmentRequest) -> AssessmentResponse:
        if not self._kernel or not self._completion:
            raise RuntimeError("AgentCore runtime is not initialized")

        artifact_summaries = self._summarize_artifacts(request.artifacts)
        context = self._build_context(request.context or {})
        assessment_output = self._invoke_agent("system", artifact_summaries, context)

        return self._parse_assessment_output(request.request_id, assessment_output)

    def _summarize_artifacts(self, artifacts: list[AssessmentArtifact]) -> str:
        summaries = []
        for artifact in artifacts:
            summaries.append(
                f"- {artifact.artifact_type}: {artifact.name or 'unnamed'}\n{artifact.content.strip()}"
            )
        return "\n\n".join(summaries)

    def _build_context(self, context: dict[str, str]) -> str:
        return "\n".join(f"{key}: {value}" for key, value in context.items()) or "No additional context provided."

    def _invoke_agent(self, agent_name: str, artifacts_summary: str, context: str) -> str:
        agent_function = self._agent_functions.get(agent_name)
        if not agent_function:
            raise RuntimeError(f"No semantic function registered for agent '{agent_name}'")

        prompt_payload = f"Context:\n{context}\n\nArtifacts:\n{artifacts_summary}"
        logger.debug("Invoking Semantic Kernel function for agent %s", agent_name)
        result = self._kernel.run(agent_function, prompt_payload)
        response_text = getattr(result, "output", str(result)).strip()
        logger.info("Semantic Kernel completed for agent %s", agent_name)
        return response_text

    def _parse_assessment_output(self, request_id: str, raw_output: str) -> AssessmentResponse:
        score = self._extract_confidence(raw_output)
        recommendations = [
            Recommendation(
                pillar="Overall",
                title="Enterprise AWS Architecture Assessment",
                detail=raw_output[:512],
                confidence=score,
            )
        ]
        evidence = [
            Evidence(
                source="Bedrock AI",
                description="Generated assessment and recommendations",
                excerpt=raw_output[:256],
            )
        ]

        return AssessmentResponse(
            request_id=request_id,
            assessment_id=str(uuid.uuid4()),
            summary=raw_output.split("\n", 1)[0] if raw_output else "No assessment generated.",
            recommendations=recommendations,
            evidence=evidence,
            confidence_score=score,
            raw_output=raw_output,
        )

    def _extract_confidence(self, raw_output: str) -> float:
        default_score = 0.75
        for line in raw_output.splitlines():
            if "confidence" in line.lower():
                parts = [part.strip() for part in line.split(":", 1)]
                if len(parts) == 2:
                    try:
                        value = float(parts[1].strip().rstrip(".%"))
                        return min(max(value / 100.0 if value > 1 else value, 0.0), 1.0)
                    except ValueError:
                        continue
        return default_score


class SemanticKernelOrchestrator:
    def __init__(self, agent_core: BedrockAgentCore) -> None:
        self.agent_core = agent_core

    def orchestrate_assessment(self, request: AssessmentRequest) -> AssessmentResponse:
        logger.debug("Orchestrating assessment using Semantic Kernel for request %s", request.request_id)
        return self.agent_core.assess_artifacts(request)
