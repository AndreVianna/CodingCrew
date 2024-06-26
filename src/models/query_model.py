from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class Query(BaseModel):
    question: str
    answer: str
    done: bool = False

    def __init__(self, question: str | None = None, answer: str | None = None, done: bool | None = None) -> None:
        super().__init__()
        self.question = question or self.question
        self.answer = answer or self.answer
        self.done = done or self.done
