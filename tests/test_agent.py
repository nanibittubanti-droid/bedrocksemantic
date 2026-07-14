from unittest.mock import MagicMock

from app.agent import BedrockAgentCore
from app.config import Config
from app.models import AssessmentArtifact, AssessmentRequest


def make_config() -> Config:
    return Config(
        aws_region="us-east-1",
        model_id="amazon.titan-text-bison",
        log_level="INFO",
        temperature=0.5,
        max_tokens=256,
        server_host="0.0.0.0",
        server_port=8080,
        bedrock_endpoint="https://bedrock.us-east-1.amazonaws.com",
        service_name="waf-assessment-platform",
        environment="test",
    )


def test_assess_artifacts_parses_confidence_from_response():
    config = make_config()
    agent = BedrockAgentCore(config)
    agent._kernel = object()
    dummy_response = MagicMock()
    dummy_response.text = "Overall assessment complete. Confidence: 88%"
    agent._completion = MagicMock()
    agent._completion.complete.return_value = dummy_response

    request = AssessmentRequest(
        request_id="req-001",
        artifacts=[
            AssessmentArtifact(
                artifact_type="terraform",
                name="example",
                content="resource \"aws_s3_bucket\" \"example\" {}",
            )
        ],
        context={"project": "waf-review"},
    )

    response = agent.assess_artifacts(request)

    assert response.request_id == "req-001"
    assert response.confidence_score == 0.88
    assert response.assessment_id
    assert response.summary.startswith("Overall assessment complete")
    agent._completion.complete.assert_called_once()
