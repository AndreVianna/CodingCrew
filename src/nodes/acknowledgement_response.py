from utils.common import normalize_text

from .base_response import BaseResponse

class AcknowledgementResponse(BaseResponse):
    def __str__(self) -> str:
        text: str = normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST be a SINGLE WORD. The word must be 'ACKNOWLEDGE' (all uppercase).
            The answer represents that you received the information in this message ans are ready to proceed.
            The user will respond with the word 'PROCEED' so you can executed the requested task.""")
        return text