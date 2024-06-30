import os

from dataclasses import dataclass

from utils.common import snake_case

from models import Project

from .base_state import BaseState

@dataclass(frozen=True)
class ProjectState(BaseState):
    def __init__(self, previous: BaseState, project: Project) -> None:
        base_folder = os.path.join(previous.run.base_folder, snake_case(project.name))
        super().__init__(base_folder)
        self.project = project
