import os

from datetime import datetime

from pydantic import BaseModel

class Run(BaseModel):
    workspace: str = None
    id: str = str(datetime.now().strftime("%Y%m%dT%H%M%S"))
    step: int = 0
    status: str = "NEW"

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.workspace = data.get("workspace")
        if not self.workspace:
            raise ValueError("The workspace folder is required.")
        if not os.path.isdir(self.workspace):
            raise ValueError("Invalid workspace folder.")

        self.id = data.get("id") or self.id

        self.step = data.get("step") or self.step
        if self.step < 0:
            raise ValueError("The step must be a non-negative integer.")

        self.status = data.get("status") or self.status

    @property
    def folder(self) -> str:
        return os.path.join(self.workspace, self.id)

    @property
    def file(self) -> str:
        return os.path.join(self.folder, f"""{self.step:05d}.{self.status.lower()}.json""")
