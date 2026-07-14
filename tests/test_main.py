import json
from unittest.mock import MagicMock, patch

from app.main import load_assessment_request, run
from app.models.request import AssessmentRequest


def test_load_assessment_request_from_payload(monkeypatch):
    payload = {
        "request_id": "req-001",
        "artifacts": [
            {
                "artifact_type": "terraform",
                "name": "example",
                "content": "resource \"aws_s3_bucket\" \"example\" {}",
            }
        ],
    }
    monkeypatch.setenv("ASSESSMENT_PAYLOAD", json.dumps(payload))
    request = load_assessment_request()

    assert isinstance(request, AssessmentRequest)
    assert request.request_id == "req-001"
    assert request.artifacts[0].artifact_type == "terraform"


@patch("app.main.load_config")
@patch("app.main.WorkflowOrchestrator")
@patch("app.main.BedrockService")
def test_run_initializes_agent_and_assesses(
    mock_bedrock_service,
    mock_workflow_class,
    mock_load_config,
    monkeypatch,
):
    config = mock_load_config.return_value
    config.log_level = "INFO"
    config.aws_region = "us-east-1"
    config.model_id = "amazon.titan-text-bison"
    config.temperature = 0.7
    config.max_tokens = 256
    config.bedrock_endpoint = None
    config.service_name = "waf-assessment-platform"
    config.environment = "test"

    request_payload = {
        "request_id": "req-001",
        "artifacts": [
            {
                "artifact_type": "terraform",
                "name": "example",
                "content": "resource \"aws_s3_bucket\" \"example\" {}",
            }
        ],
    }
    monkeypatch.setenv("ASSESSMENT_PAYLOAD", json.dumps(request_payload))

    mock_service = mock_bedrock_service.return_value
    mock_workflow = mock_workflow_class.return_value
    mock_workflow.orchestrate.return_value = MagicMock(model_dump_json=lambda indent: json.dumps({"request_id": "req-001"}))

    result = run()

    assert result == 0
    mock_service.initialize.assert_called_once()
    mock_workflow.orchestrate.assert_called_once()
