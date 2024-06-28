from pydantic import BaseModel

class BaseResponse(BaseModel):
    @classmethod
    def get_prompt(cls) -> str:
        return ""
