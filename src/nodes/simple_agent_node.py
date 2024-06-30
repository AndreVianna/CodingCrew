from typing import TypeVar

from pydantic import BaseModel
from personas import BasePersona
from responses import BaseResponse

from .agent_node import AgentNode

State = TypeVar("State", bound=BaseModel)
AgentPersona = TypeVar("AgentPersona", bound=BasePersona)
AgentResponse = TypeVar("AgentResponse", bound=BaseResponse)

class SimpleAgentNode[State, AgentPersona, AgentResponse](AgentNode[State, AgentPersona, AgentResponse, State]): # pylint: disable=too-few-public-methods
    def _create_result(self, response: AgentResponse) -> State: # pylint: disable=unused-argument
        pass
