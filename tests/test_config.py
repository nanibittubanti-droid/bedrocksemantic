import os

import pytest

from app.config import load_config


def test_load_config_raises_when_missing_environment(monkeypatch):
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("MODEL_ID", raising=False)
    with pytest.raises(ValueError, match="AWS_REGION is required"):
        load_config()


def test_load_config_accepts_custom_values(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-2")
    monkeypatch.setenv("MODEL_ID", "amazon.titan-text-bison")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("TEMPERATURE", "0.2")
    monkeypatch.setenv("MAX_TOKENS", "512")
    monkeypatch.setenv("SERVER_HOST", "127.0.0.1")
    monkeypatch.setenv("SERVER_PORT", "9000")
    monkeypatch.setenv("SERVICE_NAME", "waf-assessment-platform")
    monkeypatch.setenv("ENVIRONMENT", "dev")

    config = load_config()

    assert config.aws_region == "us-west-2"
    assert config.model_id == "amazon.titan-text-bison"
    assert config.log_level == "DEBUG"
    assert config.temperature == 0.2
    assert config.max_tokens == 512
    assert config.server_host == "127.0.0.1"
    assert config.server_port == 9000
    assert config.service_name == "waf-assessment-platform"
    assert config.environment == "dev"
