

import uuid
from typing import Literal
from typing_extensions import TypedDict
from pydantic import UUID4

from models.query import Query

class ProjectState(TypedDict):
    id:UUID4
    name: str | None
    folder: str | None
    description: list[str]
    queries: list[Query]
    report: str | None
    status: Literal[
        "CREATED",
        "STARTED",
        "DESCRIPTION_UPDATED",
        "REPORT_GENERATED",
    ]
    finish: bool = False

    def __init__(self):
        self.id = uuid.uuid4()
        self.name = None
        self.folder = None
        self.description = list[str]()
        self.queries = list[Query]()
        self.report = None
        self.status = Literal["CREATED"]
