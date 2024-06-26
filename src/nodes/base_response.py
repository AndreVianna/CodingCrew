from pydantic import BaseModel

class BaseResponse(BaseModel):
    def __str__(self) -> str:
        return ""
