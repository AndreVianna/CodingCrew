from dataclasses import dataclass
import os
from typing import Optional

from utils.common import normalize_text

from .project_model import Project
from .run_model import RunModel
from .query_model import Query

@dataclass
class AnalysisModel(RunModel):
    project: Project = None
    counter: int = 0
    queries: list[Query] = []

    def __init__(self, project: Project, counter: Optional[int] = 0, queries: Optional[list[Query]] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.project = project
        self.counter = counter or self.counter
        self.queries = queries or self.queries

    def __str__(self) -> str:
        queries: str = ""
        if self.queries:
            queries = "## Questions:" + os.linesep
            for i, query in enumerate(self.queries):
                queries += normalize_text(f"""\
                    Question {i+1}:
                        {normalize_text(query.question, indent_level=6)}
                    Answer:
                        {normalize_text(query.answer, indent_level=6)}

                    """)
        return super().__str__() + queries
