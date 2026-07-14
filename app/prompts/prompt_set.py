from pathlib import Path
from typing import Iterable

from app.models.request import AssessmentRequest


class PromptSet:
    def __init__(self, prompt_dir: Path) -> None:
        self.prompt_dir = prompt_dir

    def _load_agent_prompt(self, agent_name: str) -> str:
        prompt_file = self.prompt_dir / f"{agent_name}.txt"
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8").strip()

        if agent_name == "operational_excellence":
            prompt_file = self.prompt_dir / "operational.txt"
            if prompt_file.exists():
                return prompt_file.read_text(encoding="utf-8").strip()

        from .prompts import AGENT_PROMPTS

        return AGENT_PROMPTS.get(agent_name, AGENT_PROMPTS["system"])

    def build_prompt(
        self,
        agent_name: str,
        request: AssessmentRequest,
        extra_context: dict[str, str] | None = None,
        retrieved_documents: Iterable[str] | None = None,
    ) -> str:
        from .prompts import SYSTEM_PROMPT

        agent_prompt = self._load_agent_prompt(agent_name)
        context_text = request.to_prompt_input()
        prompt_sections = [SYSTEM_PROMPT, agent_prompt, context_text]

        if extra_context:
            additional_context = "\n".join(f"{key}: {value}" for key, value in extra_context.items())
            prompt_sections.append(f"Extra Context:\n{additional_context}")

        if retrieved_documents:
            documents = "\n\n".join(retrieved_documents)
            prompt_sections.append(f"Retrieved Knowledge:\n{documents}")

        prompt_sections.append(
            "Provide a concise assessment, list clear recommendations, cite evidence sources, "
            "and include a confidence estimate between 0.0 and 1.0."
        )

        return "\n\n".join(prompt_sections)
