from utils.common import normalize_text

from .base_agent import BaseAgent

class DefaultAgent(BaseAgent):
    def __str__(self) -> str:
        return  normalize_text("""\
            You are a helpful assistant.
            You are able to understand and respond to user requests.
            You enjoy helping the user to achieve the best answer.
            """)
