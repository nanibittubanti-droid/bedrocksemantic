from pydantic import BaseModel

from app.models.request import AssessmentRequest
from app.models.response import AssessmentResponse


class AssessmentPackage(BaseModel):
    request: AssessmentRequest
    response: AssessmentResponse | None = None
