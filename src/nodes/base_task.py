from typing import Generic, TypeVar
from pydantic import BaseModel

from models.project_state import ProjectState

S = TypeVar("S", ProjectState, ProjectState)

class BaseTask(BaseModel, Generic[S]):
    def execute(self, state: S) -> S:
        return state
