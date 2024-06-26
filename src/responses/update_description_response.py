from typing import ClassVar

from utils.common import normalize_text

from .json_response import JsonResponse

class UpdateDescriptionResponse(JsonResponse):
    description: str
    json_schema: ClassVar[str] = normalize_text("""\
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Response schema",
            "type": "object",
            "properties": {
                "description": {
                    "type": "string"
                }
            },
            "required": [
                "description"
            ]
        }
        """)
