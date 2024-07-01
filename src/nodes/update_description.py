from typing import ClassVar
from langchain_core.messages import SystemMessage

from utils.common import normalize_text

from states import AnalysisState
from responses import UpdatedDescription

from .simple_analyst_agent_node import SimpleAnalystAgentNode

class UpdateDescription(SimpleAnalystAgentNode[AnalysisState, UpdatedDescription]): # pylint: disable=too-few-public-methods
    name: ClassVar[str] = "update_description"
    def __init__(self, state: AnalysisState) -> None:
        super().__init__(state, goal = normalize_text("""\
            Your goal is to generate an updated description of the project.
            You MUST analyze all the project definition provided by the USER, including the PROJECT DESCRIPTION and the ANSWERS to the previous questions.
            You MUST include in the NEW UPDATED DESCRIPTION all the existing information in the current descripiotn and the new information added through the answers.
            You MUST provide a clear and complete description of the project.
            The description MUST be composed of CHAPTERS, aggregating the main points of the analysis.
            Each CHAPTER MUST HAVE BULLET POINTS representing the main aspects of the application.
            Each BULLET POINT MUST HAVE a TITLE and a short description explaining that topic, how it is related to the project and the solution adopted.
            The description can be as long as necessary. DO NOT WORRY about the length of the chapters or bullet point text.
            """))

    def _execute(self) -> AnalysisState:
        return super()._execute()

    def _create_result(self, response: UpdatedDescription) -> AnalysisState:
        result = AnalysisState(**self.state)
        result.project.description = response.description
        result.counter += 1
        for query in filter(lambda x: not x.is_processed, result.queries):
            query.is_processed = True
        result.save()
        return result
