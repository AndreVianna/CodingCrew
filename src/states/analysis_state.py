from dataclasses import dataclass
from typing import Optional

from models import Query

from .project_state import ProjectState

@dataclass(frozen=True)
class AnalysisState(ProjectState):
    def __init__(self, previous: ProjectState, queries: Optional[list[Query]] = None, counter: Optional[int] = 0) -> None:
        super().__init__(previous, previous.project)
        self.counter = counter
        self.queries = queries
