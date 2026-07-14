import logging
from typing import Any, Iterable

from app.kernel.kernel import SemanticKernelRuntime
from app.models.request import AssessmentRequest
from app.observability import tracer
from app.prompts.prompt_set import PromptSet
from app.services.knowledgebase_service import KnowledgeBaseService

logger = logging.getLogger(__name__)


class BedrockService:
    AGENT_NAMES = [
        "system",
        "security",
        "reliability",
        "performance",
        "cost",
        "operational_excellence",
        "workload",
        "service",
        "recommendation_engine",
    ]

    def __init__(
        self,
        kernel_runtime: SemanticKernelRuntime,
        prompt_set: PromptSet,
        knowledge_service: KnowledgeBaseService | None = None,
    ) -> None:
        self.kernel_runtime = kernel_runtime
        self.prompt_set = prompt_set
        self.knowledge_service = knowledge_service
        if self.knowledge_service is None:
            raise ValueError("KnowledgeBaseService is required for RAG-enabled BedrockService")
        self._kernel: Any | None = None
        self._agent_functions: dict[str, Any] = {}

    def initialize(self) -> None:
        self._kernel = self.kernel_runtime.get_kernel()
        self._register_agent_functions()

    def _register_agent_functions(self) -> None:
        if self._kernel is None:
            raise RuntimeError("Kernel runtime must be initialized before registering agents")

        for agent_name in self.AGENT_NAMES:
            prompt_template = "{input}"
            self._agent_functions[agent_name] = self._kernel.create_semantic_function(
                prompt_template,
                skill_name=agent_name,
                description=f"Semantic assessment function for the {agent_name} agent.",
            )
            logger.debug("Registered semantic function for %s", agent_name)

    def _build_knowledge_query(
        self,
        agent_name: str,
        request: AssessmentRequest,
        extra_context: dict[str, str] | None = None,
    ) -> str:
        if extra_context:
            return " \n".join(extra_context.values())
        return request.request_id

    def evaluate_agent(
        self,
        agent_name: str,
        request: AssessmentRequest,
        extra_context: dict[str, str] | None = None,
        retrieved_documents: Iterable[str] | None = None,
    ) -> str:
        if self._kernel is None:
            raise RuntimeError("Kernel runtime must be initialized before evaluating requests")

        agent_function = self._agent_functions.get(agent_name)
        if agent_function is None:
            raise ValueError(f"Unknown agent name: {agent_name}")

        knowledge_documents = retrieved_documents
        if agent_name in {"service", "recommendation_engine"}:
            query = self._build_knowledge_query(agent_name, request, extra_context)
            knowledge_documents = self.knowledge_service.retrieve_relevant_documents(query)

        prompt = self.prompt_set.build_prompt(
            agent_name,
            request,
            extra_context=extra_context,
            retrieved_documents=knowledge_documents,
        )
        logger.info("Evaluating %s agent for request %s", agent_name, request.request_id)
        with tracer.start_as_current_span(
            f"agent.evaluate.{agent_name}",
            attributes={
                "agent.name": agent_name,
                "request.id": request.request_id,
                "service.name": self.kernel_runtime.config.service_name,
            },
        ):
            result = self._kernel.run(agent_function, prompt)
            output = getattr(result, "output", str(result)).strip()

        logger.debug("Agent %s evaluation complete", agent_name)
        return output

    def evaluate_request(self, request: AssessmentRequest) -> str:
        return self.evaluate_agent("system", request)
