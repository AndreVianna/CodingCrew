import os
from typing import Optional
from dataclasses import dataclass

from pydantic import BaseModel

from utils.common import normalize_text, snake_case

from .run_model import RunModel

@dataclass(frozen=True)
class Project(BaseModel):
    run: RunModel
    name: str
    description: Optional[str] = None

    def __init__(self, run: RunModel, name: str, description: Optional[str] = "") -> None:
        super().__init__()
        if not run:
            raise ValueError("The current run is required.")
        if not name:
            raise ValueError("The project name is required.")
        self.run = run
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
