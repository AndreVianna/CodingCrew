"""State for the planning workflow."""

from typing import TypedDict

from pydantic import BaseModel

class PlanningState(TypedDict):
    """
    Represents the state of a planning workflow.

    Attributes:
        project_name (str): The name of the project.
        project_description (str): The description of the project.
        context (dict): Additional context information for the planning workflow.
    """
    project_name: str
    project_description: str
    context: dict

class InitialAnalysisResult(BaseModel):
    updated_description: str
    additional_questions: list[str]

    @classmethod
    def from_json(cls, json_data: dict) -> 'InitialAnalysisResult':
        """Create an InitialAnalysisResult object from JSON data."""
        return cls(
            updated_description=json_data.get('updated_description'),
            additional_questions=json_data.get('additional_questions')
        )
