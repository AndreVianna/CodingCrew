from typing import TypeVar

from pydantic import BaseModel
from responses import BaseResponse

from .analysis_node import AnalysisNode

State = TypeVar("State", bound=BaseModel)
AgentResponse = TypeVar("AgentResponse", bound=BaseResponse)

class SimpleAnalystAgentNode[State, AgentResponse](AnalysisNode[State, AgentResponse, State]): # pylint: disable=too-few-public-methods
    def _create_result(self, response: AgentResponse) -> State: # pylint: disable=unused-argument
        pass
