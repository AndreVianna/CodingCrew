from typing import ClassVar

from utils.common import normalize_text

from models import Query

from .json_response import JsonResponse

class GeneratesQuestions(JsonResponse):
    queries: list[Query]
    _schema: ClassVar[str] = normalize_text("""\
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Generated schema for Root",
        "type": "object",
        "properties": {
            "queries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string"
                        },
                        "answer": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "question",
                        "answer"
                    ]
                }
            }
        },
        "required": [
            "queries"
        ]
    }
    """)
