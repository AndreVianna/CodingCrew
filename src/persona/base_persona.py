from pydantic import BaseModel

class BasePersona(BaseModel):
    @classmethod
    def prompt(cls) -> str:
        raise NotImplementedError
