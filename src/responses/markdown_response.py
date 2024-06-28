from utils.common import normalize_text

from .base_response import BaseResponse

class MarkdownResponse(BaseResponse):
    @classmethod
    def get_prompt(cls) -> str:
        return normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST be a TEXT in a MARKDOWN format.
            IMPORTANT! The answer MUST contain ONLY the content of the MARKDOWN. It MUST NOT contain any preamble, conclusion, or any other text that is not part of the markdown content.
            IMPORTANT! The text MUST use UTF-8 encoding.""")
