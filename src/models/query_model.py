from typing import ClassVar
from dataclasses import dataclass

from utils.common import normalize_text

from .json_model import JsonModel

@dataclass(frozen=True)
class Query(JsonModel):
    question: str
    answer: str
    done: bool = False

    def __init__(self, question: str, answer: str, done: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.question = question
        self.answer = answer
        self.done = done

    schema: ClassVar[str] = normalize_text("""\
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema#",
        "$id": "https://schema.com/query",
        "title": "Generated queries",
        "type": "array",
        "items": {
            "$ref": "https://schema.com/query.json"
        }
    }
    """)
