"""Models for the planning crew."""

import ast
from pydantic import BaseModel
from common import Query, Question

class CrewInput(BaseModel):
    """
    Represents the input data for a crew.

    Attributes:
        name (str): The name of the crew.
        description (str): The description of the crew.
        queries (list[Query]): The list of queries associated with the crew.
        finish (bool): Indicates whether the crew has finished or not.
    """
    name: str
    description: str
    queries: list[Query]
    finish: bool

class CrewOutput(BaseModel):
    """Represents the output of a crew."""

    description: str
    questions: list[Question]

    @classmethod
    def from_json(cls, json_data: dict | str) -> 'CrewOutput':
        """Create a CrewOutput object from JSON data.

        Args:
            json_data (dict | str): The JSON data representing the crew output.

        Returns:
            CrewOutput: The created CrewOutput object.
        """
        if isinstance(json_data, str):
            json_data = ast.literal_eval(json_data)
        return cls(**json_data)
