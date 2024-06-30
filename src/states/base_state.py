import os
import glob
import json

from typing import Optional, Self
from dataclasses import dataclass

from pydantic import BaseModel

from models import Run

@dataclass(frozen=True)
class BaseState(BaseModel):
    def __init__(self, workspace: str) -> None:
        super().__init__()
        self.run = Run(workspace)

    @classmethod
    def create_from_file(cls, state_file: str) -> Self:
        with open(state_file, "r", encoding="utf-8") as file:
            content = json.load(file)
            return cls(**content)

    def load(self, step: Optional[int] = None) -> None:
        if step is None:
            if not os.path.exists(self.run.file):
                raise ValueError(f"No state file found for step {step} of run '{self.run}'.")
            file_path = self.run.file
        else:
            if not os.path.exists(self.run.folder):
                raise ValueError(f"No storage folder found for run '{self.run}'.")
            file_query = os.path.join(self.run.folder, f"{step:05}.*.json")
            files = glob.glob(file_query)
            if not files:
                raise ValueError(f"No state file found for step {step} of run '{self.run}'.")
            if len(files) > 1:
                raise ValueError(f"Multiple state files found for step {step} of run '{self.run}'.")
            file_path = files[0]
        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)
            self.__dict__.update(**content)

    def save(self) -> None:
        os.makedirs(self.run.folder, exist_ok=True)
        with open(self.run.file, "w", encoding="utf-8") as file:
            json.dump(self, file, default=str)
