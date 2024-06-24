

import json
import uuid
from typing import Literal
from pydantic import BaseModel

from models.query import Query

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

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)