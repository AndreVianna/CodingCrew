from responses.yes_no_response import YesNoResponse
from utils.common import normalize_text

class ConfirmationResponse(YesNoResponse):
    @classmethod
    def definition(cls) -> str:
        return normalize_text("""\
            Before proceeding, please confirm that you understood the instructions.""") + \
            super().definition()
