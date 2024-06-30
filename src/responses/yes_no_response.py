from utils.common import normalize_text

from .base_response import BaseResponse

class YesNoResponse(BaseResponse):
    @classmethod
    def definition(cls) -> str:
        return normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST BE: 'YES' or 'NO' (without the quotes).
            IMPORTANT! If your answer is 'YES', you MUST NOT use any other word or add any additional text to the answer.
            IMPORTANT! If your answer is 'NO', place the NO in the first line and an explanation for the negative stating on the next line.""")
