from typing import ClassVar

from pydantic import BaseModel

class JsonModel(BaseModel):
    schema: ClassVar[str] = None

    def __init__(self, **data) -> None: # pylint: disable=useless-super-delegation
        super().__init__(**data)
