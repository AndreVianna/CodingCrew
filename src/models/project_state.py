import os
import uuid
from typing import Literal

from utils.common import normalize_text

from .serializable import Serializable
from .query import Query

class ProjectState(Serializable):
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

    def to_user_message(self) -> str:
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
