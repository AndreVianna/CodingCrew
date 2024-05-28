"""
Represents the common models used in the analysis workflow.
"""

from typing_extensions import TypedDict

class Query(TypedDict):
    """
    Represents a query with a question and its corresponding answer.

    Attributes:
        question (str): The text of the question.
        answer (str): The answer to the question.
    """
    question: str
    answer: str


class Question(TypedDict):
    """
    Represents a question with its text and proposed answer.

    Attributes:
        text (str): The text of the question.
        proposed_answer (str): The proposed answer to the question.
    """
    text: str
    proposed_answer: str
