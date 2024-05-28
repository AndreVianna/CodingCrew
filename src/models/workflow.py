"""
Represents the models used in the analysis workflow.
"""

from typing_extensions import TypedDict

from models.common import Query, Question

class AnalysisState(TypedDict):
    """
    Represents the state of a analysis workflow.

    Attributes:
        project_name (str): The name of the project.
        project_description (str): The description of the project.
        queries (list[Query]): The queries already answered by the user.
        questions (list[Question] | None): The addtional questions to ask the user.
        finish (bool): The flag to finish the workflow.
        report (str | None): The final report of the analysis.
    """
    project_name: str
    project_description: str
    queries: list[Query]
    questions: list[Question] | None
    finish: bool
    report: str | None
