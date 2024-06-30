from typing import ClassVar

from pydantic import BaseModel

class JsonModel(BaseModel):
    schema: ClassVar[str] = ""
