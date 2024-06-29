from typing import Generic, Hashable, TypeVar

from pydantic import BaseModel

from models.run_model import RunModel

S = TypeVar("S", bound=RunModel)
R = TypeVar("R", Hashable, list[Hashable])

class BaseEdge(BaseModel, Generic[S, R]):
    @classmethod
    def check(cls, state: S) -> R:
        if not state:
            raise ValueError("State is required!")
