from datetime import datetime

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    pillar: str
    title: str
    detail: str
    confidence: float


class Evidence(BaseModel):
    source: str
    description: str
    excerpt: str | None = None


class AssessmentResponse(BaseModel):
    request_id: str
    assessment_id: str
    summary: str
    recommendations: list[Recommendation]
    evidence: list[Evidence]
    confidence_score: float
    raw_output: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
