from dataclasses import dataclass
import os

from utils.common import normalize_text

from .project_state import Project
from .query_model import Query

@dataclass
class UpdateDescriptionState(Project):
    counter: int = 0
    queries: list[Query] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.counter = kwargs.get("counter") or self.counter
        self.queries = kwargs.get("queries") or self.queries

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
