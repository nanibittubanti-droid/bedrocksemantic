from app.prompts import AGENT_PROMPTS, build_assessment_prompt


def test_build_assessment_prompt_includes_agent_details():
    artifacts_summary = "- terraform: sample module"
    context = "project: waf-review"

    prompt = build_assessment_prompt("security", artifacts_summary, context)

    assert "Security Agent" in prompt
    assert artifacts_summary in prompt
    assert context in prompt


def test_build_assessment_prompt_defaults_to_system_agent():
    prompt = build_assessment_prompt("unknown", "artifact content", "no context")
    assert "System Assessment Agent" in prompt
    assert "artifact content" in prompt
    assert "no context" in prompt
    assert "confidence estimate" in prompt.lower()
