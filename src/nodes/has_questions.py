"""
represents the first node of the analysis, where the user is prompted to enter the project name and description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    Literal["FINISH"] | Literal["CONTINUE"]: "FINISH" if there are no questions or "CONTINUE" if there are unanswered questions.
"""

from typing import Literal
from models.project_state import ProjectState

def create(state: ProjectState) -> Literal["FINISH"] | Literal["CONTINUE"]:
    """
    Checks if there are any unanswered questions in the given state.

    Args:
        state (AnalysisState): The state containing the questions.

    Returns:
        str: "FINISH" if there are no questions or "CONTINUE" if there are unanswered questions.
    """
    pending_queries = filter(lambda q: not q.done, state.queries)
    if state.status != "STARTED" or state.counter >= 3 or not pending_queries:
        return "FINISH"
    return "CONTINUE"
