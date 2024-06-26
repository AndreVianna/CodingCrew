from typing import Literal

from models.project_state import ProjectState

def check(state: ProjectState) -> Literal["FINISH", "CONTINUE"]:
    if not filter(lambda q: not q.done, state.queries):
        return "FINISH"
    return "CONTINUE"
