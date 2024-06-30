import os

from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

from utils.common import normalize_text

from .project_model import Project
from .query_model import Query

@dataclass(frozen=True)
class UpdateDescriptionModel(BaseModel):
    def __init__(self, project: Project, counter: Optional[int] = 0, queries: Optional[list[Query]] = None) -> None:
        super().__init__()
        self.project = project
        self.counter = counter
        self.queries = queries or list[Query]()

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
