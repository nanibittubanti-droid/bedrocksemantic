import json
import logging
import os
import sys
from pathlib import Path

from app.config import load_config
from app.kernel.kernel import SemanticKernelRuntime
from app.logging_config import configure_logging
from app.models.request import AssessmentRequest
from app.orchestrator.workflow import WorkflowOrchestrator
from app.prompts.prompt_set import PromptSet
from app.services.bedrock_service import BedrockService
from app.services.knowledgebase_service import KnowledgeBaseService
from app.services.memory_service import MemoryService
from app.services.postgres_service import PostgresService
from app.services.rag_service import RAGService
from app.services.session_service import SessionService
from app.services.pgvector_service import PgVectorService
from app.services.embedding_service import EmbeddingService


def load_assessment_request() -> AssessmentRequest:
    payload = os.getenv("ASSESSMENT_PAYLOAD")
    if payload:
        return AssessmentRequest.model_validate_json(payload)

    if len(sys.argv) > 1:
        request_path = Path(sys.argv[1])
        if not request_path.exists():
            raise FileNotFoundError(f"Assessment request file not found: {request_path}")
        return AssessmentRequest.model_validate_file(request_path)

    raise RuntimeError(
        "No assessment request provided. Set ASSESSMENT_PAYLOAD or pass a JSON file path as the first argument."
    )


def run() -> int:
    config = load_config()
    configure_logging(config.log_level)
    logger = logging.getLogger("app.main")

    try:
        logger.info("Initializing Bedrock AgentCore runtime")
        kernel_runtime = SemanticKernelRuntime(config)
        kernel_runtime.initialize()

        prompt_set = PromptSet(Path(__file__).resolve().parent / "prompts")
        postgres_service = PostgresService(config)
        knowledge_service = KnowledgeBaseService(postgres_service)
        pgvector_service = PgVectorService(postgres_service, dim=config.embedding_dim)
        embedding_service = EmbeddingService(config)
        memory_service = MemoryService(config, postgres_service)
        session_service = SessionService(config, postgres_service)
        rag_service = RAGService(config, postgres_service, knowledge_service, pgvector=pgvector_service, embedder=embedding_service)
        bedrock_service = BedrockService(kernel_runtime, prompt_set, knowledge_service=knowledge_service)
        bedrock_service.initialize()
        orchestrator = WorkflowOrchestrator(bedrock_service)

        logger.info("Loading assessment request")
        request = load_assessment_request()

        logger.info("Running assessment workflow for request %s", request.request_id)
        response = orchestrator.orchestrate(request)

        print(response.model_dump_json(indent=2))
        return 0
    except Exception:
        logger.exception("Assessment execution failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
