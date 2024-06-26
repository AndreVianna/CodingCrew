import os

from dataclasses import dataclass

from utils.common import normalize_text

from .base_state import BaseState

@dataclass
class Project(BaseState):
    name: str = ""
    description: str = ""

    def __init__(self, base: BaseState, name: str, folder: str, description: str) -> None:
        super().__init__(base.workspace, base.run, base.step, base.status)
        self.name = name or self.name
        self.folder = folder or self.folder
        self.description = description or self.description

    def __str__(self) -> str:
        return normalize_text(f"""\
            ## Project Name:
            {self.name}
            ## Project Description:""") + \
            normalize_text(self.description)
