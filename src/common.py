"""Global models."""

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
    Represents a question with its text and proposal.

    Attributes:
        text (str): The text of the question.
        proposal (str): The proposed answer to the question.
    """
    text: str
    proposal: str
