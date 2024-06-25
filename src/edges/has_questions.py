from typing import Literal

from models.project_state import ProjectState

def create(state: ProjectState) -> Literal["FINISH", "CONTINUE"]:
    pending_queries = filter(lambda q: not q.done, state.queries)
    if state.status != "STARTED" or state.counter >= 3 or not pending_queries:
        return "FINISH"
    return "CONTINUE"
