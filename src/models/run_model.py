import os
import glob
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Self
from pydantic import BaseModel

@dataclass
class RunModel(BaseModel):
    workspace: str = ""
    run: str = str(datetime.now().strftime("%Y%m%dT%H%M%S"))
    step: int = 0
    status: str = "NEW"

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.workspace = str(kwargs.get("workspace"))
        if not self.workspace:
            raise ValueError("The workspace folder is required.")
        if not os.path.isdir(self.workspace):
            raise ValueError("Invalid workspace folder.")

        self.run = kwargs.get("run") or self.run
        self.step = kwargs.get("step") or self.step
        self.status = kwargs.get("status") or self.status

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
