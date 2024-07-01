from typing import ClassVar
from utils.common import normalize_text

from .base_persona import BasePersona

class DefaultPersona(BasePersona):
    profile: ClassVar[str] = normalize_text("""\
        You are a helpful assistant.
        You are able to understand and respond to user requests.
        You enjoy helping the user to achieve the best answer.
        """)