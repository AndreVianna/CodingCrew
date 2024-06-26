import os
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

@dataclass
class BaseState(BaseModel):
    workspace: str = ""
    run: str = str(datetime.now().strftime("%Y%m%d%TH%M%S"))
    folder: str = ""
    step: int = 0
    status: str = "CREATED"

    def __init__(self, workspace: str, run: str | None = None, step: int | None = None, status: str | None = None) -> None:
        super().__init__()
        if not workspace or not os.path.isdir(workspace):
            raise Exception("Invalid workspace folder.")
        self.workspace = workspace
        self.run = run or self.run
        self.folder = os.path.join(workspace, run)
        self.step = step or self.step
        self.status = status or self.status
