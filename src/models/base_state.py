import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Self
from pydantic import BaseModel

@dataclass
class BaseState(BaseModel):
    type: str = None
    workspace: str = None
    run: str = str(datetime.now().strftime("%Y%m%dT%H%M%S"))
    folder: str = None
    step: int = 0
    status: str = "NEW"

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.type = self.__class__.__name__
        self.workspace = kwargs.get("workspace")
        if not self.workspace:
            raise ValueError("The workspace folder is required.")
        if not os.path.isdir(self.workspace):
            raise ValueError("Invalid workspace folder.")

        self.run = kwargs.get("run") or self.run
        self.folder = os.path.join(self.workspace, self.run)
        self.step = kwargs.get("step") or self.step
        self.status = kwargs.get("status") or self.status

    @classmethod
    def load_from(cls, state_file: str) -> Self:
        with open(state_file, "r", encoding="utf-8") as state_file:
            content = json.load(state_file)
            return cls(**content)

    def save(self) -> None:
        os.makedirs(self.folder, exist_ok=True)
        state_file = f"{self.folder}/{self.step:05}.{self.status}.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            json.dump(self, state_file, default=str)

