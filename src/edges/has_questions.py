from langgraph.graph import END

from models import UpdateDescriptionModel
from nodes import UpdateDescription

from .choice_edge import ChoiceEdge

class HasQuestions(ChoiceEdge[UpdateDescriptionModel, str]):
    @classmethod
    def check(cls, state: UpdateDescriptionModel) -> str:
        super().check(state)
        if not filter(lambda q: not q.done, state.queries):
            return END
        return UpdateDescription.name
