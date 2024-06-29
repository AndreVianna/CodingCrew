# pylint: disable=import-error
from langgraph.graph import END
# pylint: enable=import-error

from models import AnalysisModel
from nodes import GenerateQuestions

from .base_edge import BaseEdge

class CanAskQuestions(BaseEdge[AnalysisModel, str]):
    @classmethod
    def check(cls, state: AnalysisModel) -> str:
        super().check(state)
        if state.status != "STARTED" or state.counter >= 3:
            return GenerateQuestions.name
        return END
