from dataclasses import dataclass

from utils.common import normalize_text

from .base_state import BaseState

@dataclass
class Project(BaseState):
    name: str = None
    description: str = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = kwargs.get("name")
        if not self.name:
            raise ValueError("The project name is required.")
        self.description = kwargs.get("description")

    def __str__(self) -> str:
        return normalize_text(f"""\
            ## Project Name:
            {self.name}
            ## Project Description:""") + \
            normalize_text(self.description)
