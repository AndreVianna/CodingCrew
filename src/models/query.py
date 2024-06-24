import json
from pydantic import BaseModel


class Query(BaseModel):
    question: str
    answer: str
    done: bool = False

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
