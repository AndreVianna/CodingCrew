from utils.common import normalize_text

from .base_response import BaseResponse

class YesNoResponse(BaseResponse):
    @classmethod
    def expected_format(cls) -> str:
        return normalize_text("""\
            # Expected Response
            IMPORTANT! Your answer MUST BE: 'Yes' or 'No' (without the quotes).
            IMPORTANT! You MUST NOT use any other word or add any additional text to the answer.""")
