from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class Query(BaseModel):
    question: str
    answer: str
    done: bool

    def __init__(self, question: str, answer: str, done: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.question = question
        self.answer = answer
        self.done = done
