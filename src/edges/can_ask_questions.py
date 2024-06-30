from langgraph.graph import END

from models import UpdateDescriptionModel
from nodes import GenerateQuestions

from .choice_edge import ChoiceEdge

class CanAskQuestions(ChoiceEdge[UpdateDescriptionModel, str]):
    @classmethod
    def check(cls, state: UpdateDescriptionModel) -> str:
        super().check(state)
        if state.status != "STARTED" or state.counter >= 3:
            return GenerateQuestions.name
        return END
