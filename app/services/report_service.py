import logging

from app.models.assessment import AssessmentResponse

logger = logging.getLogger(__name__)


class ReportService:
    def generate_report(self, response: AssessmentResponse) -> dict[str, str]:
        logger.info("Generating report for assessment %s", response.assessment_id)
        return {
            "assessment_id": response.assessment_id,
            "summary": response.summary,
            "confidence": f"{response.confidence_score:.2f}",
        }
