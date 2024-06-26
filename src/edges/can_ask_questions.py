from typing import Literal

from models.project_state import ProjectState

def check(state: ProjectState) -> Literal["FINISH", "CONTINUE"]:
    if state.status != "STARTED" or state.counter >= 3:
        return "FINISH"
    return "CONTINUE"
