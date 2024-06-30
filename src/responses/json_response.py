import os
import json
from typing import ClassVar, Optional, TypeVar

import jsonschema
from pydantic import BaseModel

from utils.common import normalize_text

from .base_response import BaseResponse

J = TypeVar("J", bound=BaseModel)

class JsonResponse[J](BaseResponse):
    schema: ClassVar[str] = ""
    @classmethod
    def definition(cls, schema: Optional[str] = None) -> str:
        schema = schema or cls.schema
        if not schema:
            raise ValueError("JSON schema is required for JSON response format.")
        cls.__ensure_is_json(schema)
        prompt = normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST be in a JSON format.
            IMPORTANT! The answer MUST contain ONLY the JSON object. It MUST NOT contain any title, preamble, conclusion, analysis or any additional information.
            IMPORTANT! All linebreaks within strings must be escaped with the character sequence "\\n".
            IMPORTANT! All double quotes within strings must be escaped with the character sequence "\\"".
            IMPORTANT! All strings MUST use UTF-8 encoding.""")
        if not cls.schema:
            raise ValueError("JSON schema is required for JSON response format.")
        return prompt + normalize_text("""\
            Here is the JSON schema for the answer:
            ```json""") + \
            normalize_text(cls.schema) + \
            "```" + os.linesep

    @classmethod
    def __ensure_is_json(cls, schema):
        required_draft = "https://json-schema.org/draft/2020-12/schema#"
        try:
            value = json.loads(schema)
            if "$schema" not in value or value["$schema"] != required_draft:
                raise ValueError(f"""The JSON schema must reference "$schema": "{required_draft}" """)
        except Exception as exc:
            raise ValueError("The JSON schema is invalid.") from exc

    def __init__(self, answer: str) -> None:
        super().__init__(answer)
        schema = getattr(self, "schema")
        if not schema:
            raise ValueError("JSON schema is required for JSON response format.")
        try:
            self.value = json.loads(answer())
            jsonschema.validate(self.value, json.loads(self._schema))
        except jsonschema.ValidationError as exc:
            raise ValueError("The answer does not match the defined schema.") from exc
