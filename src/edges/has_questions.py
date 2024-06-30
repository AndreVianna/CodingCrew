from langgraph.graph import END

from states import AnalysisState
from nodes import UpdateDescription

from .choice_edge import ChoiceEdge

class HasQuestions(ChoiceEdge[AnalysisState, str]):
    @classmethod
    def check(cls, state: AnalysisState) -> str:
        super().check(state)
        if not filter(lambda q: not q.processed, state.queries):
            return END
        return UpdateDescription.name
