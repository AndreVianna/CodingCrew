from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

from models.run_model import Run

State = TypeVar("State", bound=Run)
Result = TypeVar("Result", Literal, list[Literal])

class ChoiceEdge(BaseModel, Generic[State, Result]):
    @classmethod
    def check(cls, state: State) -> Result:
        if not state:
            raise ValueError("State is required!")
