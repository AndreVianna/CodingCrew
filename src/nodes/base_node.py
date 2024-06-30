from typing import ClassVar, TypeVar
from pydantic import BaseModel

InitialState = TypeVar("InitialState", bound=BaseModel)
ResultState = TypeVar("ResultState", bound=BaseModel)

class BaseNode[InitialState, ResultState](BaseModel):
    name: ClassVar[str] = "BaseNode"   # create default state

    def __init__(self, state: InitialState) -> None:
        super().__init__()
        self.state = state

    @classmethod
    def run(cls, state: InitialState) -> ResultState:
        return cls(state)._execute()

    def _execute(self) -> ResultState:
        raise NotImplementedError
