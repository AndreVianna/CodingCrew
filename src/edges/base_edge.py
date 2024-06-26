from typing import Generic, Hashable, TypeVar

from pydantic import BaseModel

from models.base_state import BaseState

S = TypeVar("S", bound=BaseState)
R = TypeVar("R", Hashable, list[Hashable])

class BaseEdge(BaseModel, Generic[S, R]):
    @classmethod
    def check(cls, state: S) -> R:
        if not state:
            raise ValueError("State is required!")
