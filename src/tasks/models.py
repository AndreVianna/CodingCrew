"""
Represents the models used in the analysis workflow.
"""

from typing import Literal
import uuid
from pydantic import UUID4
from typing_extensions import TypedDict

class Query(TypedDict):
    question: str
    answer: str

class ProjectQuery(Query):
    pending: bool

class ProjectState(TypedDict):
    id:UUID4
    name: str | None
    folder: str | None
    description: list[str]
    queries: list[ProjectQuery]
    report: str | None
    status: Literal[
        "CREATED",
        "STARTED",
        "DESCRIPTION_UPDATED",
        "REPORT_GENERATED",
    ]

    def __init__(self):
        self.id = uuid.uuid4()
        self.name = None
        self.folder = None
        self.description = list[str]()
        self.queries = list[ProjectQuery]()
        self.report = None
        self.status = Literal["CREATED"]
