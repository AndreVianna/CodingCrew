from typing import ClassVar, TypeVar
from pydantic import BaseModel

IS = TypeVar("IS", bound=BaseModel)
FS = TypeVar("FS", bound=BaseModel)

class BaseNode[IS, FS](BaseModel):
    name: ClassVar[str] = "BaseNode"   # create default state

    def __init__(self, state: IS) -> None:
        super().__init__()
        self.initial_state = state
        self.final_state: FS = None

    @classmethod
    def run(cls, state: IS) -> FS:
        return cls(state)._execute()

    def _execute(self) -> FS:
        raise NotImplementedError
