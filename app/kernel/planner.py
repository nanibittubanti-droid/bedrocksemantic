class Planner:
    def __init__(self) -> None:
        self.tasks = []

    def add_task(self, task: str) -> None:
        self.tasks.append(task)

    def plan(self) -> list[str]:
        return self.tasks
