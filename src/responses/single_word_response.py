from typing import ClassVar

from utils.common import normalize_text

from .base_response import BaseResponse

class SingleWordResponse(BaseResponse):
    word: ClassVar[str] = "OK"
    @classmethod
    def prompt(cls, **kwargs) -> str:
        return normalize_text(f"""\
            # Expected Response
            IMPORTANT! Your answer MUST be a SINGLE WORD. The word must be '{cls.word}' (case sensitive).
            The answer represents a signal to the use and MUST NOT be changed.
            You MUST NOT change the word or add any additional text to the answer.""")
