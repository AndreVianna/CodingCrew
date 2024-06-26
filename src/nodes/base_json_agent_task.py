import json

from typing import Generic, Type, TypeVar
from pydantic import BaseModel

# pylint: disable=import-error
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import LanguageModelInput
# pylint: enable=import-error

from models.project_state import ProjectState

from .base_agent_task import BaseAgentTask
from .json_response import JsonResponse

S = TypeVar("S", ProjectState, ProjectState)
R = TypeVar("R", BaseModel, BaseModel)

class BaseJsonAgentTask(BaseAgentTask[S], Generic[S, R]):
    response_type: Type[R] | None = None
    json_schema: str = ""

    def __init__(self, agent: str, goal: str, response_type: Type[R], allow_markdown: bool = False) -> None:
        super().__init__(agent, goal, allow_markdown)
        self.response_type = response_type
        self.json_schema = response_type.json_schema

    def execute(self, state: S) -> S:
        messages = [SystemMessage(content=self._get_system_message(self.agent, self.description, self.goal))]
        self._ask_model_to_acknowledge(messages, state.describe())
        response = self._ask_model_for_text(messages, "PROCEED")
        response = self.__ask_model_for_json(messages)
        return self._update_state(response, state)

    def __ask_model_for_json(self,  messages: LanguageModelInput) -> R:
        content="Please, convert the answer to a JSON format."
        messages.append(HumanMessage(content=self._get_user_message(content, JsonResponse(self.json_schema))))
        response_text = self._ask_model(messages)
        response_json = json.loads(response_text)
        return self.response_type(**response_json)
