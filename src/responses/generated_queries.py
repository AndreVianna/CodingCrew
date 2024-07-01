from typing import ClassVar

from models import Queries
from utils.common import normalize_text

from .json_response import JsonResponse

class GeneratedQueries(JsonResponse[Queries]):
    schema: ClassVar[str] = normalize_text("""\
    {
        "$schema": "https://json-schema.org/draft/2020-12/schema#",
        "$id": "https://schema.com/response",
        "$ref": "https://schema.com/query"
    }
    """) + \
    Queries.schema
