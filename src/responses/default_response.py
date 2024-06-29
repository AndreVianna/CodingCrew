from .base_response import BaseResponse

class DefaultResponse(BaseResponse):
    @classmethod
    def prompt(cls, **kwargs) -> str:
        return ""
