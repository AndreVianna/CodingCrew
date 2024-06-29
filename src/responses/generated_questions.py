from typing import ClassVar

from utils.common import normalize_text

from models import Query

from .json_response import JsonResponse

class GeneratedQueries(JsonResponse):
    schema: ClassVar[str] = normalize_text("""\
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema#",
        "$id": "https://schema.com/queries.json",
        "title": "Generated queries",
        "type": "array",
        "items": {
            "$ref": "https://schema.com/query.json"
        }
    }
    """) + \
    Query.schema
