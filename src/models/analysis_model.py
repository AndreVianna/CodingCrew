import os

from dataclasses import dataclass

from pydantic import BaseModel

from utils.common import normalize_text

from .project_model import Project
from .query_model import Query

@dataclass(frozen=True)
class AnalysisModel(BaseModel):
    project: Project = None
    counter: int = 0
    queries: list[Query] = []

    def __init__(self, project: Project, **kwargs) -> None:
        super().__init__(**kwargs)
        self.project = project

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
