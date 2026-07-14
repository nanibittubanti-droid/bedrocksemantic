import json
from unittest.mock import MagicMock, patch

from app.services.embedding_service import EmbeddingService


def make_config():
    cfg = MagicMock()
    cfg.aws_region = "us-east-1"
    cfg.embedding_model_id = "test-embed-model"
    cfg.embedding_dim = 16
    return cfg


def test_embed_parses_body_shape():
    cfg = make_config()
    client = MagicMock()
    body_payload = json.dumps({"embedding": [0.1 * i for i in range(cfg.embedding_dim)]}).encode("utf-8")
    client.invoke_model.return_value = {"body": body_payload}

    with patch("boto3.client", return_value=client):
        svc = EmbeddingService(cfg)
        vec = svc.embed("hello world")
        assert len(vec) == cfg.embedding_dim
        assert all(isinstance(x, float) for x in vec)


def test_embed_parses_readable_response():
    cfg = make_config()
    client = MagicMock()

    class Resp:
        def read(self):
            return json.dumps({"results": [{"embedding": [0.01 * i for i in range(cfg.embedding_dim)]}] }).encode("utf-8")

    client.invoke_model.return_value = Resp()

    with patch("boto3.client", return_value=client):
        svc = EmbeddingService(cfg)
        vec = svc.embed("another text")
        assert len(vec) == cfg.embedding_dim
        assert all(isinstance(x, float) for x in vec)


def test_embed_fallback_when_client_missing():
    cfg = make_config()
    # No boto3 client available
    with patch("boto3.client", side_effect=Exception("no client")):
        svc = EmbeddingService(cfg)
        vec = svc.embed("fallback")
        assert len(vec) == cfg.embedding_dim
        assert all(isinstance(x, float) for x in vec)
