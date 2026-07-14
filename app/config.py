import os
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    aws_region: str
    model_id: str
    log_level: str
    temperature: float
    max_tokens: int
    server_host: str
    server_port: int
    bedrock_endpoint: str | None
    service_name: str
    environment: str
    database_url: str
    embedding_model_id: str | None
    embedding_dim: int
    otel_exporter_endpoint: str | None
    otel_service_name: str
    otel_environment: str
    log_format: str


def load_config() -> Config:
    aws_region = os.getenv("AWS_REGION", "us-east-1").strip()
    model_id = os.getenv("MODEL_ID", "amazon.titan-text-bison").strip()
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()
    log_format = os.getenv("LOG_FORMAT", "plain").strip().lower()
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("MAX_TOKENS", "1024"))
    server_host = os.getenv("SERVER_HOST", "0.0.0.0").strip()
    server_port = int(os.getenv("SERVER_PORT", "8080"))
    bedrock_endpoint = os.getenv("BEDROCK_ENDPOINT", "").strip() or None
    service_name = os.getenv("SERVICE_NAME", "waf-assessment-platform").strip()
    environment = os.getenv("ENVIRONMENT", "production").strip().lower()
    otel_exporter_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip() or None
    otel_service_name = os.getenv("OTEL_SERVICE_NAME", service_name).strip() or service_name
    otel_environment = os.getenv("OTEL_ENVIRONMENT", environment).strip() or environment
    database_url = os.getenv("DATABASE_URL", "").strip()
    embedding_model_id = os.getenv("EMBEDDING_MODEL_ID", "").strip() or None
    embedding_dim = int(os.getenv("EMBEDDING_DIM", "1536"))

    if not aws_region:
        raise ValueError("AWS_REGION is required")
    if not model_id:
        raise ValueError("MODEL_ID is required")
    if not database_url:
        raise ValueError("DATABASE_URL is required for PostgreSQL-backed RAG and session persistence")
    if embedding_dim <= 0:
        raise ValueError("EMBEDDING_DIM must be a positive integer")
    if temperature < 0.0 or temperature > 2.0:
        raise ValueError("TEMPERATURE must be between 0.0 and 2.0")
    if max_tokens <= 0:
        raise ValueError("MAX_TOKENS must be a positive integer")
    if server_port <= 0 or server_port > 65535:
        raise ValueError("SERVER_PORT must be a valid port number")
    if log_format not in {"plain", "json"}:
        raise ValueError('LOG_FORMAT must be either "plain" or "json"')

    return Config(
        aws_region=aws_region,
        model_id=model_id,
        log_level=log_level,
        temperature=temperature,
        max_tokens=max_tokens,
        server_host=server_host,
        server_port=server_port,
        bedrock_endpoint=bedrock_endpoint,
        service_name=service_name,
        environment=environment,
        database_url=database_url,
        embedding_model_id=embedding_model_id,
        embedding_dim=embedding_dim,
        otel_exporter_endpoint=otel_exporter_endpoint,
        otel_service_name=otel_service_name,
        otel_environment=otel_environment,
        log_format=log_format,
    )
