import os
from typing import ClassVar

from utils.common import normalize_text

from .query_model import Query

from .json_model import JsonModel

class Queries(JsonModel):
    items: list[Query] = list[Query]()

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.items = data.get("items") or self.items

    schema: ClassVar[str] = normalize_text("""\
    {
        "$id": "https://schema.com/queries",
        "title": "List of queries",
        "type": "array",
        "items": {
            "$ref": "https://schema.com/query"
        }
    }
    """) + \
    Query.schema

    def __str__(self) -> str:
        if not self.items:
            return ""
        queries = "## Questions:" + os.linesep
        for query in self.items:
            queries += str(query)
        return queries
