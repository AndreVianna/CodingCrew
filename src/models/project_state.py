

import uuid
from typing import Literal

from models.query import Query

class ProjectState():
    project_id: str
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

    def __init__(self, project_id: str | None = None, name: str | None = None, folder: str | None = None, description: list[str] | None = None, queries: list[Query] | None = None, report: str | None = None, status: Literal["CREATED"] = "CREATED", finish: bool = False):
        self.project_id = project_id if project_id else str(uuid.uuid4()).lower()
        self.name = name
        self.folder = folder
        self.description = description if description else list[str]()
        self.queries = queries if queries else list[Query]()
        self.report = report
        self.status = status
        self.finish = finish
