from typing import ClassVar, TypeVar

from pydantic import BaseModel

from nodes.base_node import BaseNode

S = TypeVar("S", bound=BaseModel)

class SimpleNode[S](BaseNode[S, S]):
    name: ClassVar[str] = "SimpleNode"   # create default state
