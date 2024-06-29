from typing import ClassVar
from utils.common import normalize_text

from .base_response import BaseResponse

class TextResponse(BaseResponse):
    _use_markdown: ClassVar[bool] = False
    @classmethod
    def prompt(cls, **kwargs) -> str:
        text_format = "formatted using the MARKDOWN syntax" if cls._use_markdown else "in PLAIN TEXT with no formatting"
        return normalize_text(f"""\
            # Expected Response
            IMPORTANT! Your response MUST be a TEXT containing ONLY what was REQUESTED ABOVE.
            IMPORTANT! Your response MUST be {text_format}.
            IMPORTANT! It MUST NOT contain any preamble, conclusion, or any other text that is not RELEVANT TO THE TASK.
            IMPORTANT! The content MUST use UTF-8 encoding.""")
