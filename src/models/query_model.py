from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class Query(BaseModel):
    question: str
    answer: str
    done: bool = False

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.question = str(kwargs.get("question"))
        self.answer = str(kwargs.get("answwer"))
        self.done = bool(kwargs.get("done")) or self.done
