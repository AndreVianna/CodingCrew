from dataclasses import dataclass
import os

from utils.common import normalize_text, snake_case

from .base_state import BaseState

@dataclass
class ProjectState(BaseState):
    name: str = ""
    description: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = str(kwargs.get("name"))
        if not self.name:
            raise ValueError("The project name is required.")
        self.description = str(kwargs.get("description")) or self.description

    @property
    def folder(self) -> str:
        return os.path.join(self.workspace, snake_case(self.name))

    def __str__(self) -> str:
        return normalize_text(f"""\
            ## Project Name:
            {self.name}
            ## Project Description:""") + \
            normalize_text(self.description)
