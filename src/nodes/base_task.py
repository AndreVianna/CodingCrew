from typing import ClassVar, Generic, Self, TypeVar
from pydantic import BaseModel

from models import BaseState

S = TypeVar("S", bound=BaseState)

class BaseTask(BaseModel, Generic[S]):
    state: S = None
    name: ClassVar[str] = None

    def __init__(self, state: S) -> None:
        super().__init__()
        self.state = state

    @classmethod
    def run(cls, state: S) -> S:
        return cls(state)._execute()

    def _execute(self) -> S:
        return self.state
