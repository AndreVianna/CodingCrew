from pydantic import BaseModel

class BaseResponse(BaseModel):
    @classmethod
    def definition(cls) -> str:
        return ""

    def __init__(self, answer: str) -> None:
        super().__init__()
        self.answer = answer
