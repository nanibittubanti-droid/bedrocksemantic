from typing import Any


class WorkflowManager:
    def __init__(self) -> None:
        self.steps: list[Any] = []

    def add_step(self, step: Any) -> None:
        self.steps.append(step)

    def run(self, input_data: Any) -> Any:
        result = input_data
        for step in self.steps:
            result = step(result)
        return result
