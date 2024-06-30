from .text_response import TextResponse

class UpdatedDescription(TextResponse):
    @classmethod
    def definition(cls, use_markdown=True) -> str:
        return super().definition(use_markdown)
