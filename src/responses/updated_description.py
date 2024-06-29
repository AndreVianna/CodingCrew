from .text_response import TextResponse

class UpdatedDescription(TextResponse):
    @classmethod
    def expected_format(cls, use_markdown=True) -> str:
        return super().expected_format(use_markdown)
