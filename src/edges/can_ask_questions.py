from langgraph.graph import END

from states import AnalysisState
from nodes import GenerateQueries

from .choice_edge import ChoiceEdge

class CanAskQuestions(ChoiceEdge[AnalysisState, str]):
    @classmethod
    def check(cls, state: AnalysisState) -> str:
        super().check(state)
        if state.status != "STARTED" or state.counter >= 3:
            return GenerateQueries.name
        return END
