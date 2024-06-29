from typing import ClassVar

from pydantic import BaseModel

from utils.common import normalize_text

class JsonModel(BaseModel):
    _schema: ClassVar[str] = ""
    schema: ClassVar[str] = normalize_text(_schema)
