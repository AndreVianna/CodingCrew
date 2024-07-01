from models import Query

from .project_state import ProjectState

class AnalysisState(ProjectState):
    counter: int = 0
    queries: list[Query] = list[Query]()

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.counter = data.get("counter") or self.counter
        self.queries = list[Query](data.get("queries")) if data.get("queries") else self.queries
