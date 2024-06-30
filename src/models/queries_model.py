from typing import ClassVar
from dataclasses import dataclass

from pydantic import BaseModel

from utils.common import normalize_text

from .query_model import Query

@dataclass(frozen=True)
class Queries(BaseModel):
    def __init__(self, queries: list[Query]) -> None:
        super().__init__()
        self.queries = queries

    schema: ClassVar[str] = normalize_text("""\
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema#",
        "$id": "https://schema.com/queries",
        "title": "List of queries",
        "type": "array",
        "items": {
            "$ref": "https://schema.com/query"
        }
    }
    """) + \
    Query.schema
