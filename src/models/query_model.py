import os
from typing import ClassVar

from utils.common import normalize_text
from utils.terminal import set_style

from .json_model import JsonModel

class Query(JsonModel):
    number: int = 0
    question: str = None
    answer: str = None
    is_processed: bool = False

    def __init__(self, **data: dict) -> None:
        super().__init__()
        self.number = data.get("number")
        if not self.number:
            raise ValueError("The question number is required.")
        if self.number < 0:
            raise ValueError("The question number must be a non-negative integer.")

        self.question = data.get("question")
        if not self.question:
            raise ValueError("The question is required.")

        self.answer = data.get("answer")
        if not self.answer:
            raise ValueError("The answer is required.")

        self.is_processed = data.get("is_processed") or self.is_processed

    schema: ClassVar[str] = normalize_text("""\
    {
        "$id": "https://schema.com/query",
        "title": "Single query",
        "type": "object",
        "properties": {
            "question": {
                "type": "string"
            },
            "answer": {
                "type": "string"
            }
        },
        "required": [
            "question",
            "answer"
        ]
    }
    """)

    PROCESSED: ClassVar[str] = set_style("processed", "green")
    PENDING: ClassVar[str] = set_style("pending", "yellow", styles=["dim"])

    def __str__(self) -> str:
        status = self.PROCESSED if self.is_processed else self.PENDING
        return normalize_text(f"""\
            Question {self.number} ({status}):
                {normalize_text(self.question, indent_level=4)}
            Answer:
                {normalize_text(self.answer, indent_level=4)}
            """) + os.linesep
