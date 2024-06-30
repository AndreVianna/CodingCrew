from typing import TypeVar

from pydantic import BaseModel
from nodes import AgentNode
from personas import BasePersona
from responses import BaseResponse

State = TypeVar("State", bound=BaseModel)
AgentPersona = TypeVar("AgentPersona", bound=BasePersona)
AgentResponse = TypeVar("AgentResponse", bound=BaseResponse)

class SimpleAgentNode[State, AgentPersona, AgentResponse](AgentNode[State, AgentPersona, AgentResponse, State]): # pylint: disable=too-few-public-methods
    def _create_result(self, response: AgentResponse) -> State: # pylint: disable=unused-argument
        pass
