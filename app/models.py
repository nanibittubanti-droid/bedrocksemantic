from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AssessmentArtifact(BaseModel):
    artifact_type: str
    name: str | None = None
    content: str


class Recommendation(BaseModel):
    pillar: str
    title: str
    detail: str
    confidence: float


class Evidence(BaseModel):
    source: str
    description: str
    excerpt: str | None = None


class AssessmentRequest(BaseModel):
    request_id: str
    artifacts: list[AssessmentArtifact]
    context: dict[str, str] | None = {}


class AssessmentResponse(BaseModel):
    request_id: str
    assessment_id: str
    summary: str
    recommendations: list[Recommendation]
    evidence: list[Evidence]
    confidence_score: float
    raw_output: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
