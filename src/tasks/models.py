"""
Represents the models used in the analysis workflow.
"""

from typing import Literal
from pydantic import UUID4
from typing_extensions import TypedDict

class Query(TypedDict):
    question: str
    answer: str

class ProjectQuery(Query):
    pending: bool

class ProjectState(TypedDict):
    id:UUID4
    name: str
    folder: str
    description: list[str]
    queries: list[ProjectQuery] = []
    report: str | None = None,
    status: Literal[
        "CREATED",
        "STARTED",
        "DESCRIPTION_UPDATED",
        "REPORT_GENERATED",
    ] = "CREATED",
