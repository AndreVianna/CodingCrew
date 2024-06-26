import os
from typing import Literal
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel

from utils.common import normalize_text

from .query import Query

@dataclass
class ProjectState(BaseModel):
    project_id: str = datetime.now().strftime("%Y%m%d-%H%M%S")
    name: str = ""
    folder: str = ""
    description: list[str] = []
    queries: list[Query] = []
    counter: int = 0
    status: Literal[
        "CREATED",
        "STARTED",
        "DESCRIPTION_UPDATED",
        "REPORT_GENERATED",
    ] = "CREATED"

    def __init__(self, project_id: str | None = None, name: str | None = None, folder: str | None = None, description: list[str] | None = None, queries: list[Query] | None = None, counter: int | None = None, status: str | None = None) -> None:
        super().__init__()
        self.project_id = project_id or self.project_id
        self.name = name or self.name
        self.folder = folder or self.folder
        self.description = description or self.description
        self.queries = queries or self.queries
        self.counter = counter or self.counter
        self.status = status or self.status


    def describe(self) -> str:
        queries: str = ""
        if self.queries:
            queries = "Questions:" + os.linesep
            for i, query in enumerate(self.queries):
                queries += normalize_text(f"""\
                    Question {i+1}:
                        {normalize_text(query.question, indent_level=6)}
                    Answer:
                        {normalize_text(query.answer, indent_level=6)}

                    """)

        return normalize_text(f"""\
            # Project Name:
            {self.name}
            # Project Description:
            """) + \
            normalize_text(self.description[-1]) + \
            normalize_text(queries)
