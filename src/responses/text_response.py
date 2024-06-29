from typing import Optional
from utils.common import normalize_text

from .base_response import BaseResponse

class TextResponse(BaseResponse):
    @classmethod
    def expected_format(cls, use_markdown: Optional[bool] = False) -> str:
        text_format = "use MARKDOWN syntax" if use_markdown else "be PLAIN TEXT with no formatting"
        return normalize_text(f"""\
            # Expected Response
            IMPORTANT! Your response MUST be a TEXT containing ONLY what was REQUESTED ABOVE.
            IMPORTANT! The text MUST {text_format}.
            IMPORTANT! It MUST NOT contain any preamble, conclusion, or any other text that is not RELEVANT TO THE TASK.
            IMPORTANT! The content MUST use UTF-8 encoding.""")
