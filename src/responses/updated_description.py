from typing import ClassVar

from .text_response import TextResponse

class UpdatedDescription(TextResponse):
    _use_markdown: ClassVar[bool] = True
