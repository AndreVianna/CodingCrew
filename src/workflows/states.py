"""State for the planning workflow."""

from typing_extensions import TypedDict
from common import Query, Question

class AnalysisState(TypedDict):
    """
    Represents the state of a analysis workflow.

    Attributes:
        project_name (str): The name of the project.
        project_description (str): The description of the project.
        queries (list[Query]): The queries already answered by the user.
        questions (list[Question]): The addtional questions to ask the user.
    """
    project_name: str
    project_description: str
    queries: list[Query]
    questions: list[Question] | None
    finish: bool
    final_report: str | None
