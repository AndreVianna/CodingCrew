from typing_extensions import TypedDict


class Query(TypedDict):
    question: str
    answer: str
    done: bool | None = None
