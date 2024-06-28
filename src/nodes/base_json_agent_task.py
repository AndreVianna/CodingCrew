import json

from typing import Generic, Type, TypeVar
from pydantic import BaseModel

# pylint: disable=import-error
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import LanguageModelInput
# pylint: enable=import-error

from models import BaseState
from responses import JsonResponse

from .base_agent_task import BaseAgentTask

S = TypeVar("S", bound=BaseState)
R = TypeVar("R", bound=JsonResponse)

class BaseJsonAgentTask(BaseAgentTask[S], Generic[S, R]): # pylint: disable=too-few-public-methods
    response_type: R

    def __init__(self, goal: str, response_type: Type[R]) -> None:
        super().__init__(goal=goal)
        self.response_type = response_type

    def _execute(self, state: S) -> S:
        messages = [SystemMessage(content=self._get_system_message(self.agent, self.instructions, self.goal))]
        self._ask_model_to_acknowledge(messages, state.describe())
        response = self._ask_model_for_text(messages, "PROCEED")
        response = self.__ask_model_for_json(messages)
        return self._update_state(state, response)

    def __ask_model_for_json(self,  messages: LanguageModelInput) -> R:
        content="Please, convert the answer to a JSON format."
        messages.append(HumanMessage(content=self._get_user_message(content, JsonResponse(self.json_schema))))
        response_text = self._ask_model(messages)
        response_json = json.loads(response_text)
        return self.response_type(**response_json)
