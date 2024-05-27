"""Global models."""

from typing_extensions import TypedDict

class Query(TypedDict):
    question: str
    answer: str

class Question(TypedDict):
    text: str
    proposal: str
