
from typing import Optional, TypeVar

from pydantic import BaseModel

from utils.common import normalize_text

from personas import SystemAnalyst
from responses import BaseResponse

from .agent_node import AgentNode

InitialState = TypeVar("InitialState", bound=BaseModel)
ResultState = TypeVar("ResultState", bound=BaseModel)
AgentResponse = TypeVar("AgentResponse", bound=BaseResponse)

class AnalysisNode[InitialState, AgentResponse, ResultState](AgentNode[InitialState, SystemAnalyst, AgentResponse, ResultState]): # pylint: disable=too-few-public-methods
    def __init__(self, state: InitialState, goal: Optional[str] = None) -> None:
        super().__init__(state, SystemAnalyst(), goal)
        self.preamble = normalize_text("""
            Use your expertise in system analysis assess the validity, reliability and completude of the information.
            Be attentive to details and identify inconsistencies in the information provided.
            Make sure to consider all the important aspects of a software project, including but not limited to:
                - Major components, like a console application, API, library, web application, mobile application, desktop application, or background service;
                - OS and Platform of the project, like Windows, Linux, macOS, Android, iOS, or web;
                - Programming Languages, Frameworks, and/or Tools;
                - Professional Resources Required, like developers, designers, testers, and project managers;
                - Goals and Objectives;
                - Major Features;
                - Constraints, Assumptions, and Risks;
                - Target Audience;
                - System architecture, like layers, components, services, and data flows;
                - Security Requirements, like authentication, authorization, and data protection;
                - Data Management like data storage, or external data sources;
                - Externat Resources like services or APIs;
                - Design preferences, like colors, fonts, themes, layouts, navigation;
                - UI requiremtns, like pages, components, and navigation;
                - and more.
            """) + \
            self.preamble

    def _create_result(self, response: AgentResponse) -> ResultState: # pylint: disable=unused-argument
        pass
