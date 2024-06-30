from typing import Optional
from dataclasses import dataclass

from pydantic import BaseModel

from utils.common import normalize_text

@dataclass(frozen=True)
class Project(BaseModel):
    def __init__(self, name: str, description: Optional[str] = "") -> None:
        super().__init__()
        if not name:
            raise ValueError("The project name is required.")
        self.name = name
        self.description = description or self.description

    def __str__(self) -> str:
        return normalize_text(f"""\
            ## Project Name:
            {self.name}
            ## Project Description:""") + \
            normalize_text(self.description)
