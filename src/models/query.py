from .serializable import Serializable

class Query(Serializable):
    question: str
    answer: str
    done: bool = False
