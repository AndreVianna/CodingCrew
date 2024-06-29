from typing import ClassVar, Generic, TypeVar
from pydantic import BaseModel

from models import RunModel

S = TypeVar("S", bound=RunModel)

class BaseNode(BaseModel, Generic[S]):
    state: S = S()                     # create default state
    name: ClassVar[str] = "BaseNode"   # create default state

    def __init__(self, state: S, **kwargs) -> None:
        super().__init__(**kwargs)
        self.state = state

    @classmethod
    def run(cls, state: S) -> S:
        instance = cls(state)
        return instance._execute()

    def _execute(self) -> S:
        return self.state
