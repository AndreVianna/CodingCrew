# pylint: disable=import-error
from langgraph.graph import END
# pylint: enable=import-error

from models import UpdateDescriptionState
from nodes import UpdateDescription

from .base_edge import BaseEdge

class HasQuestions(BaseEdge[UpdateDescriptionState, str]):
    @classmethod
    def check(cls, state: UpdateDescriptionState) -> str:
        super().check(state)
        if not filter(lambda q: not q.done, state.queries):
            return END
        return UpdateDescription.name
