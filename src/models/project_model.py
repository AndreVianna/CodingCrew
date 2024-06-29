from dataclasses import dataclass
import os
from typing import Optional

from utils.common import normalize_text, snake_case

from .run_model import RunModel

@dataclass
class Project(RunModel):
    name: str = None
    description: str = None

    def __init__(self, name: str, description: Optional[str] = "", **kwargs) -> None:
        super().__init__(**kwargs)
        if not name:
            raise ValueError("The project name is required.")
        self.name = name
        self.description = description or self.description

    @property
    def folder(self) -> str:
        return os.path.join(self.workspace, snake_case(self.name))

    def __str__(self) -> str:
        return normalize_text(f"""\
            ## Project Name:
            {self.name}
            ## Project Description:""") + \
            normalize_text(self.description)
