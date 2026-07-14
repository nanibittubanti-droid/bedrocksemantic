from pydantic import BaseModel


class AssessmentArtifact(BaseModel):
    artifact_type: str
    name: str | None = None
    content: str


class AssessmentRequest(BaseModel):
    request_id: str
    artifacts: list[AssessmentArtifact]
    context: dict[str, str] | None = {}

    def to_prompt_input(self) -> str:
        artifact_text = "\n\n".join(
            f"{artifact.artifact_type}: {artifact.name or 'unnamed'}\n{artifact.content.strip()}"
            for artifact in self.artifacts
        )
        context_text = "\n".join(f"{key}: {value}" for key, value in (self.context or {}).items())
        return f"Context:\n{context_text}\n\nArtifacts:\n{artifact_text}"
