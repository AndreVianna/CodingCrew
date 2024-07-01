from pydantic import BaseModel

class BaseResponse(BaseModel):
    value: str

    @classmethod
    def definition(cls) -> str:
        return ""

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value
