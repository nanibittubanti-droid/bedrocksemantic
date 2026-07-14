import json
import hashlib
import logging
from typing import Any, List, Optional

import boto3

from app.config import Config

logger = logging.getLogger(__name__)


def _extract_embedding(obj: Any) -> Optional[List[float]]:
    """Recursively search parsed JSON for a list of floats representing an embedding."""
    if isinstance(obj, list):
        # check if this is a list of numbers
        if obj and all(isinstance(x, (int, float)) for x in obj):
            return [float(x) for x in obj]
        for item in obj:
            found = _extract_embedding(item)
            if found:
                return found
    elif isinstance(obj, dict):
        # common keys used by models
        for key in ("embedding", "embeddings", "vector", "vectors", "results", "output", "outputs"):
            if key in obj:
                found = _extract_embedding(obj[key])
                if found:
                    return found
        for _, v in obj.items():
            found = _extract_embedding(v)
            if found:
                return found
    return None


class EmbeddingService:
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        try:
            self.client = boto3.client("bedrock-runtime", region_name=self.config.aws_region)
        except Exception:
            logger.debug("Bedrock client unavailable; falling back to local embedder")

    def embed(self, text: str, dim: Optional[int] = None) -> List[float]:
        dim = dim or self.config.embedding_dim
        # Try Bedrock runtime if available
        if self.client and self.config.embedding_model_id:
            try:
                body = json.dumps({"input": text}).encode("utf-8")
                resp = self.client.invoke_model(modelId=self.config.embedding_model_id, contentType="application/json", body=body)
                # Response parsing depends on model - try best-effort
                if hasattr(resp, "read"):
                    raw = resp.read()
                else:
                    raw = resp.get("body") or resp
                payload = raw
                if isinstance(payload, (bytes, bytearray)):
                    payload = payload.decode("utf-8")
                data = json.loads(payload)
                vec = _extract_embedding(data)
                if vec:
                    # trim or pad
                    if len(vec) >= dim:
                        return vec[:dim]
                    # pad with zeros if too short
                    return (vec + [0.0] * dim)[:dim]
            except Exception:
                logger.debug("Bedrock embedding call failed; falling back to local embedder", exc_info=True)

        # Deterministic local embedder fallback
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        vec: List[float] = []
        i = 0
        while len(vec) < dim:
            b = digest[i % len(digest)]
            vec.append((b / 255.0) * 2.0 - 1.0)
            i += 1
        return vec[:dim]
