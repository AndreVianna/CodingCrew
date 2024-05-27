"""Models for the planning crew."""

import ast
from pydantic import BaseModel
from common import Query, Question

class CrewInput(BaseModel):
    name: str
    description: str
    queries: list[Query]
    finish: bool

class CrewOutput(BaseModel):
    description: str
    questions: list[Question]

    @classmethod
    def from_json(cls, json_data: dict | str) -> 'CrewOutput':
        """Create an InitialAnalysisResult object from JSON data."""
        if isinstance(json_data, str):
            json_data = ast.literal_eval(json_data)
        return cls(**json_data)
