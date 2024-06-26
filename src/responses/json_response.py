import os

from utils.common import normalize_text

from .base_agent_response import BaseAgentResponse

class JsonResponse(BaseAgentResponse):
    json_schema: str = ""

    def __init__(self, json_schema: str) -> None:
        super().__init__()
        self.json_schema = json_schema

    def __str__(self) -> str:
        text: str = normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST be in a JSON format.
            IMPORTANT! The answer MUST contain ONLY the JSON object. It MUST NOT contain any title, preamble, conclusion, analysis or any additional information.
            IMPORTANT! All linebreaks within strings must be escaped with the character sequence '\\n'.
            IMPORTANT! All double quotes within strings must be escaped with the character sequence '\\"'.
            IMPORTANT! All strings MUST use UTF-8 encoding.
            Here is the JSON schema for the answer:
            ```json""") + \
            normalize_text(self.json_schema) + \
            "```" + os.linesep
        return text
