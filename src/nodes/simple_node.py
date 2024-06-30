from typing import ClassVar, TypeVar

from pydantic import BaseModel

from .base_node import BaseNode

State = TypeVar("State", bound=BaseModel)

class SimpleNode[State](BaseNode[State, State]):
    name: ClassVar[str] = "SimpleNode"   # create default state

    @classmethod
    def run(cls, state: State) -> State:
        return cls(state)._execute()

    def _execute(self) -> State:
        pass
