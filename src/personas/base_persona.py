from typing import ClassVar
from pydantic import BaseModel

class BasePersona(BaseModel):
    profile: ClassVar[str] = ""
