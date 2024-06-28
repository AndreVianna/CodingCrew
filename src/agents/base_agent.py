from pydantic import BaseModel


class BaseAgent(BaseModel):
    def __str__(self) -> str:
        raise NotImplementedError
