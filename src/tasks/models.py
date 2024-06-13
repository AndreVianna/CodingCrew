"""
Represents the models used in the analysis workflow.
"""

from typing_extensions import TypedDict

class Query(TypedDict):
    question: str
    answer: str


class Question(TypedDict):
    text: str
    proposed_answer: str


class ProjectState(TypedDict):
    name: str
    folder: str
    original_description: str
    queries: list[Query] | None = None
    questions: list[Question] | None = None
    finish_questions: bool = False
    updated_description: str | None = None
    report: str | None = None
