from pydantic import BaseModel

class BaseResponse(BaseModel):
    @classmethod
    def prompt(cls, **kwargs) -> str:
        raise NotImplementedError
