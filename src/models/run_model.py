import os
import glob
import json

from typing import Self, Optional
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

@dataclass
class RunModel(BaseModel):
    def __init__(self, workspace: str, run: Optional[str] = None, step: Optional[int] = 0, status: Optional[str] = None) -> None:
        super().__init__()
        if not workspace:
            raise ValueError("The workspace folder is required.")
        if not os.path.isdir(workspace):
            raise ValueError("Invalid workspace folder.")
        if step < 0:
            raise ValueError("The step must be a non-negative integer.")

        self.workspace = workspace
        self.run: str = run or str(datetime.now().strftime("%Y%m%dT%H%M%S"))
        self.step = step
        self.status: str = status or "NEW"

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def folder(self) -> str:
        return os.path.join(self.workspace)

    @classmethod
    def create_from_file(cls, state_file: str) -> Self:
        with open(state_file, "r", encoding="utf-8") as file:
            content = json.load(file)
            return cls(**content)

    def reload_step(self, step: int) -> None:
        file_query = os.path.join(self.folder, self.run, f"{step:05}.*.json")
        files = glob.glob(file_query)
        if not files or len(files) > 1:
            raise ValueError(f"No state file found for step {step}.")
        file_name = files[0]
        with open(file_name, "r", encoding="utf-8") as file:
            content = json.load(file)
            self.__dict__.update(**content)

    def save(self) -> None:
        run_folder = os.path.join(self.folder, self.run)
        os.makedirs(run_folder, exist_ok=True)
        file_name = os.path.join(run_folder, f"{self.step:05}.{self.status}.json")
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(self, file, default=str)
