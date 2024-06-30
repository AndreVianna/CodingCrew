from typing import ClassVar

from models import Queries

from .json_response import JsonResponse

class GeneratedQueries(JsonResponse[Queries]):
    schema: ClassVar[str] = Queries.schema
