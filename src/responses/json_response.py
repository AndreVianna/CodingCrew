import os
from typing import ClassVar

from utils.common import normalize_text

from .base_response import BaseResponse

class JsonResponse(BaseResponse):
    _schema: ClassVar[str] = ""

    @classmethod
    def prompt(cls, **kwargs) -> str:
        prompt = normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST be in a JSON format.
            IMPORTANT! The answer MUST contain ONLY the JSON object. It MUST NOT contain any title, preamble, conclusion, analysis or any additional information.
            IMPORTANT! All linebreaks within strings must be escaped with the character sequence '\\n'.
            IMPORTANT! All double quotes within strings must be escaped with the character sequence '\\"'.
            IMPORTANT! All strings MUST use UTF-8 encoding.""")
        if not cls._schema:
            return prompt
        return prompt + normalize_text("""\
            Here is the JSON schema for the answer:
            ```json""") + \
            normalize_text(cls._schema) + \
            "```" + os.linesep
