import os
import json

from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel

# pylint: disable=import-error
from langchain.chat_models import init_chat_model
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
# pylint: enable=import-error

from models.project_state import ProjectState
from utils.common import normalize_text

from .base_task import BaseTask
from .common import JsonResponseFormat, get_system_message

S = TypeVar("S", ProjectState, ProjectState)
R = TypeVar("R", BaseModel, BaseModel)

class BaseAgentTask(BaseTask[S], Generic[S, R]):
    agent: str = ""
    goal: str = ""
    description: str = ""
    response_format: JsonResponseFormat | None = None
    response_type: Type[R] | None = None

    def __init__(self, agent: str, goal: str, response_type: Type[R], response_format: JsonResponseFormat | None = None) -> None:
        super().__init__()
        self.agent = agent
        self.goal = goal
        self.description = normalize_text("""
            IMPORTANT! This taks is complex let's do it step-by step to arrive the best answer.
            """)
        self.response_type = response_type
        self.response_format = response_format

    def execute(self, state: S) -> S:
        messages = [
            SystemMessage(content=get_system_message(self.agent, self.description, self.goal, self.response_format)),
            HumanMessage(content=state.to_user_message())
        ]

        response = self.__ask_model(messages)
        return self._update_state(response, state)

    def __ask_model(self,
            messages: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[list[str]] = None,
    ) -> R:
        model_response = self.__get_model().invoke(input=messages, config=config, stop=stop)
        response_text = StrOutputParser().invoke(model_response)
        response_json = json.loads(response_text)
        return self.response_type(**response_json)

    def __get_model(self):
        model_provider = os.environ["MODEL_PROVIDER"]
        model_name = os.environ[f"{model_provider.upper()}_MODEL"]
        return init_chat_model(model_name, model_provider=model_provider, temperature=0)

    def _update_state(self, response: R, state: S) -> S: # pylint: disable=unused-argument
        return state
