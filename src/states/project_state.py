import os

from utils.common import snake_case

from models import Project

from .base_state import BaseState

class ProjectState(BaseState):
    project: Project

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.project = Project(**(data.get("project").__dict__))
        self.run.workspace = os.path.join(self.run.workspace, snake_case(self.project.name))
