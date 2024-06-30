import os

from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

@dataclass
class Run(BaseModel):
    def __init__(self, base_folder: str, run: Optional[str] = None, step: Optional[int] = 0, status: Optional[str] = None) -> None:
        super().__init__()
        if not base_folder:
            raise ValueError("The base folder is required.")
        if not os.path.isdir(base_folder):
            raise ValueError("Invalid base folder.")
        if step < 0:
            raise ValueError("The step must be a non-negative integer.")

        self.base_folder = base_folder
        self.id: str = run or str(datetime.now().strftime("%Y%m%dT%H%M%S"))
        self.step = step
        self.status: str = status or "NEW"

    @property
    def folder(self) -> str:
        return os.path.join(self.base_folder, self.id)

    @property
    def file(self) -> str:
        return os.path.join(self.folder, f"""{self.step:00000}.{self.status.lower()}.json""")
