import os
from typing import ClassVar
from dataclasses import dataclass

from utils.common import normalize_text
from utils.terminal import set_style

from .json_model import JsonModel

@dataclass(frozen=True)
class Query(JsonModel):
    def __init__(self, number: int, question: str, answer: str, done: bool = False) -> None:
        super().__init__()
        self.number = number
        self.question = question
        self.answer = answer
        self.processed = done

    schema: ClassVar[str] = normalize_text("""\
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema#",
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

    PROCESSED = set_style("processed", "green")
    PENDING = set_style("pending", "yellow", styles=["dim"])

    def __str__(self) -> str:
        status = self.PROCESSED if self.processed else self.PENDING
        return normalize_text(f"""\
            Question {self.number} ({status}):
                {normalize_text(self.question, indent_level=4)}
            Answer:
                {normalize_text(self.answer, indent_level=4)}
            """) + os.linesep
