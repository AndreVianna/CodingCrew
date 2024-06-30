from typing import TypeVar

from pydantic import BaseModel
from nodes import AnalysisNode
from responses import BaseResponse

State = TypeVar("State", bound=BaseModel)
AgentResponse = TypeVar("AgentResponse", bound=BaseResponse)

class SimpleAnalysisNode[State, AgentResponse](AnalysisNode[State, AgentResponse, State]): # pylint: disable=too-few-public-methods
    def _create_result(self, response: AgentResponse) -> State: # pylint: disable=unused-argument
        pass
