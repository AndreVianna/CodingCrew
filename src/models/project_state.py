import json
import os
import uuid
from typing import Literal
from pydantic import BaseModel

from src.utils.common import normalize_text

from .query import Query

class ProjectState(BaseModel):
    project_id: str = str(uuid.uuid4()).lower()
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

    def to_json(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def to_user_message(self) -> str:
        queries: str = ""
        if self.queries:
            queries = "Questions:" + os.linesep
            for i, query in enumerate(self.queries):
                queries += normalize_text(f"""\
                    Question {i+1}:
                        {normalize_text(indent_level=6, text=query.question)}
                    Answer:
                        {normalize_text(indent_level=6, text=query.answer)}

                    """)

        return normalize_text(f"""\
            # Project Name:
            {self.name}
            # Project Description:
            """) + \
            normalize_text(self.description[-1]) + \
            normalize_text(queries)
