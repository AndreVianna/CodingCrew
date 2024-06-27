
from typing import Generic, Type, TypeVar

from utils.common import normalize_text

from agents import SystemAnalyst
from models import BaseState
from responses import BaseAgentResponse

from .base_agent_task_with_json_response import BaseJsonAgentTask

S = TypeVar("S", bound=BaseState)
R = TypeVar("R", bound=BaseAgentResponse)

class BaseAnalysisTask(BaseJsonAgentTask[S, R], Generic[S, R]): # pylint: disable=too-few-public-methods
    def __init__(self, goal: str, response_type: Type[R]) -> None:
        agent = SystemAnalyst()
        super().__init__(agent.description, goal, response_type)
        self.description = normalize_text("""
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
            self.description
