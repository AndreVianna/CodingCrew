from typing import Optional

from pydantic import BaseModel

from utils.common import normalize_text

class Project(BaseModel):
    name: str = None
    description: Optional[str] = None

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.name = data.get("name")
        if not self.name:
            raise ValueError("The project name is required.")

        self.description = data.get("description") or self.description

    def __str__(self) -> str:
        return normalize_text(f"""\
            ## Project Name:
            {self.name}
            ## Project Description:""") + \
            normalize_text(self.description)
