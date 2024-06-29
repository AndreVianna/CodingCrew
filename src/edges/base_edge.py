from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

from models.run_model import RunModel

S = TypeVar("S", bound=RunModel)
R = TypeVar("R", Literal, list[Literal])

class BaseEdge(BaseModel, Generic[S, R]):
    @classmethod
    def check(cls, state: S) -> R:
        if not state:
            raise ValueError("State is required!")
