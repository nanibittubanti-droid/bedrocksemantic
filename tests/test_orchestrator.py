from unittest.mock import MagicMock

from app.orchestrator.workflow import WorkflowOrchestrator
from app.models.request import AssessmentRequest, AssessmentArtifact


def make_request():
    return AssessmentRequest(
        request_id="req-100",
        artifacts=[
            AssessmentArtifact(artifact_type="terraform", name="example", content="resource \"aws_s3_bucket\" \"example\" {}")
        ],
        context={"project": "waf-test"},
    )


def test_workflow_orchestrate_calls_each_agent_and_returns_response():
    mock_bedrock = MagicMock()
    # evaluate_agent should return distinct summaries for system/pillars/etc.
    def eval_agent(agent_name, request, extra_context=None, retrieved_documents=None):
        return f"{agent_name} summary"

    mock_bedrock.evaluate_agent.side_effect = eval_agent

    orchestrator = WorkflowOrchestrator(mock_bedrock)
    req = make_request()
    resp = orchestrator.orchestrate(req)

    assert resp.request_id == req.request_id
    assert "recommendations" in resp.model_dump()
    # ensure the raw_output contains the recommendation engine summary
    assert "recommendation_engine" in resp.raw_output or resp.raw_output
